import os
import time
import logging

from flask import Flask, request, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import pinecone
import openai
import tiktoken
import firebase_admin
from firebase_admin import db  # noqa

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain


from models import Document, session

# TODO: make this better than keeping in the repo
cred = firebase_admin.credentials.Certificate("firebase_key.json")
database_url = os.environ["FIREBASE_URL"]
firebase_admin.initialize_app(cred, {"databaseURL": database_url})

logging.getLogger("socketio").setLevel(logging.INFO)
logging.getLogger("engineio").setLevel(logging.WARNING)


openai.api_key = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "some random string")
admin = Admin(app, name="document_indexer", template_mode="bootstrap3", url="/api/admin/")


cache = {}


class PDFModelView(ModelView):
    def is_accessible(self):
        # only avail on workspaces on Coherence
        return "coherencedev" in request.base_url


# Admin
admin.add_view(ModelView(Document, session))

# initialize pinecone
# you can change the 
pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="us-west4-gcp-free")

index_name = "documents"
embeddings = OpenAIEmbeddings()
vectorstore = Pinecone.from_existing_index(index_name, embeddings)

if index_name not in pinecone.list_indexes():
    print(f"Creating pinecone index: {index_name}")
    pinecone.create_index(
        name=index_name,
        metric="dotproduct",
        dimension=1536,  # 1536 dim of text-embedding-ada-002
    )


OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

llm = ChatOpenAI(
    temperature=0,
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model_name=OPENAI_MODEL,
    verbose=True,
)
encoding = tiktoken.encoding_for_model(OPENAI_MODEL)


def make_id(raw_name):
    return (
        raw_name.lstrip("files/")
        .rstrip(".html")
        .rstrip(".pdf")
        .replace(" ", "-")
        .replace("/", "-")
        .replace("_", "-")
        .replace(".", "-")
        .replace("(", "-")
        .replace(")", "-")
        .replace(":", "-")
        .replace("--", "-")
        .lower()
    )


@app.route("/api/index", methods=["GET"])
def index():
    docs = session.query(Document).all()
    return jsonify([d.to_dict() for d in docs])


@app.route("/api/detail/<doc_id>", methods=["GET"])
def detail(doc_id):
    doc = session.query(Document).filter(Document.id == doc_id).one()
    return jsonify(doc.to_dict())


@app.route("/api/chats/<chat_id>", methods=["POST"])
def chat_message(chat_id):
    ref = firebase_admin.db.reference(f"/chats/{chat_id}/messages")
    msg = request.json
    history = ref.get() or []
    history = chat_with_history(msg, history)
    ref.set(history)
    return "OK"


@app.route("/api/chats/<chat_id>", methods=["DELETE"])
def delete_chat(chat_id):
    ref = firebase_admin.db.reference(f"/chats/{chat_id}/messages")
    ref.delete()
    return "OK"


def conversation_for_serialized_history(history=None):
    """history is an array of dicts with {"role": "foo", "content": "bar"}"""
    history = history or []
    print(f"History len in chat is: {len(history)}")

    condense_prompt = PromptTemplate.from_template(
        (
            "Given the following user-supplied question and chat history, produce a single question output. \n"
            "Your question should incude relevant terms, facts, and information from the chat history, and it should preserve the main line of reasoning of the user-supplied question. \n"
            "user-supplied question: {question} \nchat history: {chat_history} \nyour question:"
        )
    )

    combine_docs_custom_prompt = PromptTemplate.from_template(
        (
            "You are a devops, platform engineering, SDLC, and cloudcoc architecture expert. "
            "Use the following context from cloud whitepaper documents, along with your existing knowledge, to answer to question that follows. "
            "If in doubt about something specific, better to not answer and say you don't know than to provide an incorrect answer. "
            "Don't start your answer with \"finally\" or refer to \"the context\". "
            "context: {context} \n question: {question}"
        )
    )

    chat_history = ChatMessageHistory()
    for m in history:
        if m.get("role") == "ai":
            chat_history.add_ai_message(m["content"])
        elif m.get("role") == "human":
            chat_history.add_user_message(m["content"])
        else:
            print(f"Unknown msg history role for {m}")

    memory = ConversationSummaryMemory.from_messages(
        llm=llm,
        chat_memory=chat_history,
        return_messages=True,
        memory_key="chat_history",
        input_key="question",
        output_key="answer",
    )

    # do we need this?
    memory.load_memory_variables({})

    retriever = vectorstore.as_retriever()
    conversation = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        memory=memory,
        condense_question_prompt=condense_prompt,
        combine_docs_chain_kwargs={"prompt": combine_docs_custom_prompt},
        return_source_documents=True,
        # verbose=True,
    )

    return conversation


def chat_with_history(msg, history=None):
    """msg is a dict with {"content": "foo", "doc_id": "bar"}"""

    if request:
        chat_id = request.cookies.get("cowp_chat_id", "No chat ID!")
    else:
        chat_id = "No chat ID!"

    if not history:
        if msg["content"] in cache:
            print(f"Using cache for chat ({chat_id})...")
            # for UX so it isn't too fast
            time.sleep(1)
            history = [
                {"role": "human", "content": msg["content"]},
                cache[msg["content"]],
            ]
            return history

    conversation = conversation_for_serialized_history(history)

    start_time = time.time()
    print(f"Going to chat ({chat_id})...")
    response = conversation({"question": msg["content"]})
    end_time = time.time()
    print(f"Done with chat ({chat_id}) in {int(end_time - start_time)} seconds...")
    # print(f"Done with chat: {response}")

    answer = {
        "role": "ai",
        "content": response["answer"],
        "sources": list(
            set(
                [
                    make_id(doc.metadata["source"])
                    for doc in response["source_documents"]
                ]
            )
        ),
    }

    if not history:
        # max cache size
        if len(cache) < 64:
            cache[msg["content"]] = answer

    history.append({"role": "human", "content": msg["content"]})
    history.append(answer)

    # print(f"History before return is: {history}")
    return history


def reset_pinecone():
    # Clear the index
    print(f"Going to clear index: {index_name}")
    pinecone.delete_index(index_name)
    print(f"Done clearing index: {index_name}")


if __name__ == "__main__":
    # Run the Flask app
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        debug=(os.environ.get("COHERENCE_DEV", "").lower() == "true"),
    )
