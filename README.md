# Document Chat Starter

This is a starter repo designed to be cloned & modified by you to be the base of an AI-powered app on [Coherence](withcoherence.com). Using [OpenAI](https://openai.com/), [LangChain](https://langchain.com), and [Pinecone](https://www.pinecone.io). Using [Firebase](https://firebase.google.com) for real-time chat storage and SQLite stored in the repo itself for metadata.

This is the foundation for the [Cloud Whitepaper Index](https://cloudwhitepapers.withcoherence.com/) where you can chat with an AI Cloud Architect refrencing over 500 AWS & GCP Whitepapers. It should be very easy (and fun!) to modify this into a "chat with your own docs" app. Even if you're not building a chat app, it's an easy way to get started with these amazing technologies and build the app you're excited about. 

# How it works

Documents are placed into the `files` firectory. `PDF` and `HTML` files are supported. Metadata is placed in a CSV file called `metadata.csv` in the `files` directory. The indexing process runs locally (or using a Coherence [Workspace](https://docs.withcoherence.com/docs/reference/workspace)) and it:
- parses each file
- links it to the metadata row (based on the filename == the `Name` column of the CSV)
- breaks it into chunks to be embedded and stored in Pinecone (using `PyPDFLoader` or `UnstructuredHTMLLoader` from LangChain)
- embeds the chunks (using `vectorstore.add_documents` from LangChain)
- saves a row in sqlite with the document and metadata, along with additional AI-augmented metadata such as a description, keywords, etc...
- the docs are now available to chat with! (the prompts in `app.py` will customize the responses you can get based on your document types)

The reason we are using an in-repo SQLite file for the database is to keep the lifecycle of the data here to one DB and one Pinecone index. This allows us to keep to the free tier on Pinecone and is also just simple to reason about. Since there are no user-generated uploads here, it also "just works." You could certainly modify it to use a "real" DB like Postgres and Coherence would make that easy, too - your app would just need to do some logic to find the right Pinecone index for each database instance.

# Using this repo

- Clone the repo
    - Authenticate Firebase by adding your `firebase .json` to the `backend` directory and push to a private repo in github (or modify the code to load from an env var or other source of auth for more security)
- [Onboard](app.withcoherence.com) the app into Coherence by installing the github app and authorizing your cloud (AWS or GCP)
- Add the required env vars
    - OPENAI_API_KEY
    - PINECONE_API_KEY
    - FIREBASE_URL
- Lanch a [Workspace](https://docs.withcoherence.com/docs/reference/workspace) on your first feature
- Upload some docs to the `files` directory, and add the corresponding metadata to `metadata.csv`
- Run `cocli exec api python cli.py --parse_all`
- Use the `Dev Preview` in the Workspace to test out the app
- Deploy to your cloud by using the Workspace to push to github
- Create as many full-stack branch environments as you want by adding new [Features](https://docs.withcoherence.com/docs/reference/feature)
- Modify the app to fulfill your dreams!
    - Tweak the frontend to add your own branding & prompts
    - Modify the prompts in `app.py` to get better responses
    - Share your work with the community!