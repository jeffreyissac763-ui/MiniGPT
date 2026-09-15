from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "MiniGPT API"


def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={
            "session_id": "test-session",
            "message": "What is RAG?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert data["answer"].strip()


def test_chat_rejects_empty_message():
    response = client.post(
        "/chat",
        json={
            "session_id": "test-session",
            "message": "",
        },
    )

    assert response.status_code == 422


def test_chat_remembers_session_context():
    session_id = "memory-test-session"

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
