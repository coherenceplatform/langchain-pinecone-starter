# Document Chat Starter

This is a starter repo designed to be cloned & modified by you to be the base of an AI-powered app on [Coherence](withcoherence.com).

Using [OpenAI](https://openai.com/), [LangChain](https://langchain.com/), and [Pinecone](https://www.pinecone.io/). SQLite stored in the repo itself for metadata.

# How it works

- Clone the repo
    - add your firebase .json to the `backend` directory and push to github (or modify the code to use from an env var or other source of auth for more security)
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