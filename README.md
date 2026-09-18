# MiniGPT

A production-style AI assistant built from scratch using Python, Ollama, ChromaDB, FastAPI, and a modern web interface.

MiniGPT combines Retrieval-Augmented Generation (RAG), persistent conversation memory, document ingestion, semantic retrieval, query rewriting, and source attribution into a complete end-to-end local AI application.

## Features

- Local LLM inference using Ollama
- Retrieval-Augmented Generation (RAG)
- PDF and TXT document ingestion
- PDF page-aware processing
- Document chunking
- Ollama embeddings
- Persistent ChromaDB vector storage
- Semantic + keyword hybrid retrieval
- Conversational query rewriting
- Grounded responses
- Source attribution
- Expandable source evidence
- Persistent SQLite conversation memory
- Multiple chat sessions
- Recent chat history
- FastAPI REST API
- Interactive web interface
- Input validation
- Automated pytest test suite

## Architecture

Web Frontend
    |
    v
FastAPI API
    |
    v
RAG Engine
    |
    +------------------+
    |                  |
    v                  v
Query Rewriter     Retriever
    |                  |
    v                  v
Ollama             ChromaDB
    |                  ^
    |                  |
    |               Indexer
    |               /     \
    |              v       v
    |         PDF Loader  TXT Loader
    |
    v
Grounded Answer
    |
    v
Sources + Evidence

FastAPI
    |
    v
SQLite Conversation Memory

## RAG Pipeline

PDF / TXT
   |
   v
Document Loader
   |
   v
Text Extraction
   |
   v
Chunking
   |
   v
Ollama Embeddings
   |
   v
ChromaDB
   |
   | User Question
   v
Query Rewriting
   |
   v
Hybrid Retrieval
   |
   +-- Semantic Similarity
   |
   +-- Keyword Overlap
   |
   v
Relevant Context
   |
   v
Ollama LLM
   |
   v
Grounded Answer
   |
   v
Sources + Evidence

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| LLM | Ollama |
| Model | llama3.2:3b |
| Embeddings | nomic-embed-text |
| Vector Database | ChromaDB |
| Backend | FastAPI |
| API Server | Uvicorn |
| Database | SQLite |
| PDF Processing | PyMuPDF |
| Validation | Pydantic |
| Configuration | python-dotenv |
| Frontend | HTML, CSS, JavaScript |
| Testing | Pytest |

## Requirements

- Python 3.14
- Ollama
- Git
- 16 GB RAM recommended for the local setup

## Installation

### 1. Clone the repository

    git clone <your-repository-url>
    cd MiniGPT

### 2. Create a virtual environment

Windows PowerShell:

    python -m venv .venv

Activate:

    .\.venv\Scripts\Activate.ps1

### 3. Install dependencies

    python -m pip install -r requirements.txt

### 4. Configure environment variables

    Copy-Item .env.example .env

Default configuration:

    MODEL_NAME=llama3.2:3b
    EMBEDDING_MODEL=nomic-embed-text

### 5. Install Ollama models

    ollama pull llama3.2:3b
    ollama pull nomic-embed-text

Verify:

    ollama --version

## Index Documents

TXT:

    python -m app.ingest data/knowledge.txt

PDF:

    python -m app.ingest data/sample.pdf

Documents are extracted, split into chunks, embedded, and stored in ChromaDB.

## Run the API

    python -m uvicorn app.api:app --reload

API:

    http://127.0.0.1:8000

Swagger documentation:

    http://127.0.0.1:8000/docs

Health endpoint:

    GET /health

## Run the Frontend

Open another PowerShell terminal in the project directory:

    python -m http.server 5500 --directory frontend

Open:

    http://127.0.0.1:5500

## API Endpoints

### Health

    GET /health

### List Sessions

    GET /sessions

### Get Session Messages

    GET /sessions/{session_id}/messages

### Chat

    POST /chat

Example request:

    {
        "session_id": "demo-session",
        "message": "What is Retrieval-Augmented Generation?"
    }

## Testing

Run the complete test suite:

    pytest -q

Current development checkpoint:

    27 passed

The tests cover API endpoints, ChromaDB, SQLite memory, document loading, embeddings, indexing, PDF processing, query rewriting, RAG, retrieval, and retrieval quality.

## Design Principles

### Grounded Generation

The RAG pipeline instructs the LLM to use retrieved knowledge when generating answers.

### Source Attribution

Responses can include the source document, page number, chunk number, and evidence preview.

### Persistent Conversation Memory

Web conversations are stored in SQLite so sessions can survive browser refreshes and application restarts.

### Hybrid Retrieval

Retrieval combines semantic similarity with lexical keyword overlap.

### Query Rewriting

Conversational follow-up questions can be rewritten into standalone search queries before retrieval.

## Future Improvements

- Authentication and authorization
- Streaming LLM responses
- Improved chunk overlap handling
- Retrieval reranking
- Evaluation dashboards
- Background document ingestion
- Docker deployment
- CI/CD pipeline
- Production database
- Observability and monitoring
- Additional security controls
- Automated retrieval evaluation

## Project Status

MiniGPT is a functional end-to-end local AI assistant featuring RAG, local LLM inference, embeddings, vector search, persistent chat memory, FastAPI, a web frontend, source attribution, and automated testing.

The project is being developed as an AI/ML engineering portfolio project.