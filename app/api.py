from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, StringConstraints

from app.rag import answer_with_rag
from app.session_memory import SessionMemoryStore


app = FastAPI(
    title="MiniGPT API",
    description="API for the MiniGPT AI assistant.",
    version="1.0.0",
)


session_store = SessionMemoryStore(
    max_messages=10
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


class ChatResponse(BaseModel):
    answer: str


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
    memory = session_store.get_memory(
        request.session_id
    )

    conversation_history = memory.get_history()

    answer = answer_with_rag(
        question=request.message,
        conversation_history=conversation_history,
        top_k=3,
    )

    memory.add_message(
        "user",
        request.message,
    )

    memory.add_message(
        "assistant",
        answer,
    )

    return {
        "answer": answer,
    }
