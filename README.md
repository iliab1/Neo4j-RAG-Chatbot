# Neo4j-RAG-Chatbot

This is a conversational agent that is built on the 
[neo4j-advanced-rag](https://github.com/langchain-ai/langchain/tree/master/templates/neo4j-advanced-rag) 
template from Langchain for the purposes of testing retrieval strategies directly from the UI.

## Usage

To start the project, run the following command:

```
docker-compose up
```
Open `http://localhost:8501` in your browser to interact with a conversational agent.

## Features

The Streamlit UI offers the following capabilities:

- Chat with the conversational agent.
- Maintain context using conversation memory.
- Compare different retrieval strategies for the same query.
- Upload and store data from PDF documents.

## Environment Setup

You need to define the following environment variables in the `.env` file.

```
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```
If you are using LangSmith, you can set the following variables:
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=<YOUR_LANGCHAIN_API_KEY>
LANGCHAIN_PROJECT=<YOUR_LANGCHAIN_PROJECT_NAME>
```

## Docker Containers
This project contains the following services wrapped as docker containers
1. **Neo4j**:
   - Neo4j, a graph database, is used to store the documents and embeddings.
2. **Langserve_API**:
   - Uses LangChain's `neo4j-advanced-rag` template to implement the OpenAI LLM and RAG capabilities.
3. **UI**:
   - Simple streamlit chat user interface. Available on `localhost:8501`.
