import argparse
import os
import json
import csv
import time

# to make config easy in one place
from app import openai, vectorstore, chat_model, HumanMessage, reset_pinecone
from models import Document, session, reset_db

from langchain.document_loaders import PyPDFLoader, UnstructuredHTMLLoader


RESET_TOKEN = "YES"


def csv_metadata(filename):
    print(f"Looking for metadata for {filename}")
    with open("files/metadata.csv") as csv_file:
        # reading the csv file using DictReader
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            if row.get("Name") == filename:
                return row
    print(f"No metadata found for {filename}!")


def make_id(raw_name):
    return (
        raw_name.rstrip(".html")
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


def title_case(input_string):
    # Replace hyphens and underscores with spaces
    modified_string = input_string.replace("-", " ").replace("_", " ")

    # Title case the modified string
    titlecased_string = modified_string.title()

    return titlecased_string


def index_directory(args):
    print(f"Calling index_directory with args: {args}")
    filenames = os.listdir(args.dir)
    print(f"Got {len(filenames)} files to index")
    for i, filename in enumerate(filenames):
        index_doc(filename)

        # should never hit this?
        if i > 1000:
            print(f"End of test ({i})...")
            return

    print(f"All set indexing docs for {args.dir}!")


def index_doc(file_path, directory="files"):
    loader_map = {
        "pdf": PyPDFLoader,
        "html": UnstructuredHTMLLoader,
    }

    loader_kls = loader_map.get(file_path.split(".")[-1])
    if not loader_kls:
        print(f"No loader to match for {file_path}")
        return

    print(
        f"Calling index_doc ({loader_kls.__name__}) with path: {directory}/{file_path}"
    )

    full_file_path = f"{directory}/{file_path}"
    if not full_file_path:
        raise ValueError("Need to supply file_path!")
    file_id = make_id(file_path)

    if session.query(Document).filter(Document.id == file_id).first():
        print(f"{file_id} Document already exists...")
        return

    metadata = csv_metadata(file_path)
    if not metadata:
        print(f"No metadata avail for {file_path}")
        return

    metadata["Title"] = title = title_case(metadata["Title"] or file_path)
    print(f"Going to index {file_path} ({title}) into pinecone and save to DB")

    # Load and split PDF file into pages using PyPDFLoader
    print(f"Parsing {full_file_path}")
    loader = loader_kls(full_file_path)
    pages = loader.load_and_split()
    print(f"Got {len(pages)} pages for {full_file_path}")

    index_docs(file_id, pages, metadata)


def index_docs(doc_id, docs, metadata):
    print(f"Going to index {len(docs)} docs for {doc_id} | {metadata}")

    for page_num, page in enumerate(docs):
        # was getting rate limited by pinecone API
        time.sleep(1)

        page_id = f"{doc_id}-{page_num}"
        print(f"Going to add {page_id} to pinecone")
        vectorstore.add_documents([page])
        print(f"Added {page_id} to pinecone")
    print(f"All set indexing for {doc_id}")

    data = {}
    data.update(metadata or {})
    to_summarize = [p.page_content for p in docs[0:4]]

    try:
        message = f"generate a human-readable, accurate SEO title for the following text (filename {doc_id}): {to_summarize}"
        response = chat_model([HumanMessage(content=message)])
        data["seo_title"] = response.content
    except Exception as e:
        print(f"Cannot generate seo_title for {doc_id}: {e}")

    try:
        message = f"summarize the following text, don't reference it as 'the text': {to_summarize}"
        response = chat_model([HumanMessage(content=message)])
        data["description"] = response.content
    except Exception as e:
        print(f"Cannot generate description for {doc_id}: {e}")

    try:
        message = f"reply with ONLY a comma-seperated list of up to 10 SEO keywords for the following text (no other tokens in response for example a good response is: keyword1,keyword2): {to_summarize}"
        response = chat_model([HumanMessage(content=message)])
        data["keywords"] = [k for k in response.content.split(",")]
    except Exception as e:
        print(f"Cannot generate keywords for {doc_id}: {e}")

    # Add to SQLite database
    pdf_metadata = Document(
        id=doc_id,
        title=metadata["Title"],
        data=json.dumps(data or {}),
        provider=metadata.get("Provider"),
    )
    session.add(pdf_metadata)
    session.commit()
    print(f"Added {doc_id} to database")

    return docs


def reset_all(args):
    print(f"Calling reset_all with {args}")
    if args.token != RESET_TOKEN:
        print("NOT RESETTING - no match with key!")
        return

    reset_db()
    reset_pinecone()


def main():
    parser = argparse.ArgumentParser(prog="doc_index_chatter")
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    parse_file_parser = subparsers.add_parser("parse_file")
    parse_file_parser.add_argument("--file_path", help="filename")
    parse_file_parser.add_argument(
        "--dir", help="Directory to parse from", default="files"
    )

    parse_directory_parser = subparsers.add_parser("parse_all")
    parse_directory_parser.add_argument(
        "--dir", help="Directory to parse", default="files"
    )

    reset_parser = subparsers.add_parser("reset")
    reset_parser.add_argument(
        "--token", help=f"Supply the token. token is: {RESET_TOKEN}"
    )

    args = parser.parse_args()

    if args.command == "parse_file":
        index_doc(args.file_path, directory=args.dir)
    elif args.command == "parse_all":
        index_directory(args)
    elif args.command == "reset":
        reset_all(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
