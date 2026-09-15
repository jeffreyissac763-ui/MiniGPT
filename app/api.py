from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, StringConstraints

from app.database_memory import (
    get_messages,
    initialize_database,
    save_message,
)
from app.rag import answer_with_rag


app = FastAPI(
    title="MiniGPT API",
    description="API for the MiniGPT AI assistant.",
    version="1.0.0",
)


initialize_database()


class ChatRequest(BaseModel):
    session_id: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
        ),
    ]

    message: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
        ),
    ]


class Source(BaseModel):
    source: str
    page: int | str
    chunk: int | str
    evidence: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MiniGPT API",
    }


@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    conversation_history = get_messages(
        request.session_id,
        limit=10,
    )

    result = answer_with_rag(
        question=request.message,
        conversation_history=conversation_history,
        top_k=3,
    )

    save_message(
        request.session_id,
        "user",
        request.message,
    )

    save_message(
        request.session_id,
        "assistant",
        result["answer"],
    )

    return result
