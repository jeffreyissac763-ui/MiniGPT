from typing import Annotated

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, StringConstraints

from app.database_memory import (
    get_messages,
    get_sessions,
    initialize_database,
    save_message,
)
from app.rag import answer_with_rag


app = FastAPI(
    title="MiniGPT API",
    description="API for the MiniGPT AI assistant.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


initialize_database()


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error.",
            "message": (
                "MiniGPT could not complete the request."
            ),
        },
    )


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


class Message(BaseModel):
    role: str
    content: str


class Session(BaseModel):
    session_id: str
    created_at: str
    first_message: str | None
    last_message_at: str | None


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MiniGPT API",
    }


@app.get(
    "/sessions",
    response_model=list[Session],
)
def list_sessions():
    return get_sessions(limit=20)


@app.get(
    "/sessions/{session_id}/messages",
    response_model=list[Message],
)
def get_session_messages(session_id: str):
    return get_messages(
        session_id,
        limit=10,
    )


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
