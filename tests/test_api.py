from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "MiniGPT API"


def test_chat_endpoint(monkeypatch):
    def fake_answer_with_rag(
        question,
        conversation_history=None,
        top_k=3,
    ):
        return {
            "answer": "RAG combines information retrieval with text generation.",
            "sources": [
                {
                    "source": "knowledge.txt",
                    "page": 1,
                    "chunk": 4,
                    "evidence": (
                        "RAG combines information retrieval "
                        "with text generation."
                    ),
                }
            ],
        }

    monkeypatch.setattr(
        "app.api.answer_with_rag",
        fake_answer_with_rag,
    )

    session_id = f"test-chat-{uuid4()}"

    response = client.post(
        "/chat",
        json={
            "session_id": session_id,
            "message": "What is RAG?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "RAG combines information retrieval with text generation."
    )

    assert "sources" in data
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) == 1

    source = data["sources"][0]

    assert source["source"] == "knowledge.txt"
    assert source["page"] == 1
    assert source["chunk"] == 4
    assert source["evidence"]


def test_chat_rejects_empty_message():
    session_id = f"test-empty-{uuid4()}"

    response = client.post(
        "/chat",
        json={
            "session_id": session_id,
            "message": "",
        },
    )

    assert response.status_code == 422


def test_chat_remembers_session_context():
    session_id = f"memory-test-{uuid4()}"

    first_response = client.post(
        "/chat",
        json={
            "session_id": session_id,
            "message": "What is Retrieval-Augmented Generation?",
        },
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/chat",
        json={
            "session_id": session_id,
            "message": "What does it combine?",
        },
    )

    assert second_response.status_code == 200

    data = second_response.json()

    assert "answer" in data

    answer = data["answer"].lower()

    assert "retrieval" in answer
    assert "generation" in answer
