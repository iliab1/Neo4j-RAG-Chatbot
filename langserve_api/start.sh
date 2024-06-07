#!/bin/sh

# Run the ingestion script
python packages/neo4j-advanced-rag/ingest.py

# Start the FastAPI application
uvicorn app.server:app --host 0.0.0.0 --port 8080