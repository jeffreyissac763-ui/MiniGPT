from app import database_memory


def test_database_memory_round_trip(tmp_path, monkeypatch):
    database_path = tmp_path / "test_memory.db"

    monkeypatch.setattr(
        database_memory,
        "DATABASE_PATH",
        database_path,
    )

    database_memory.initialize_database()

    session_id = "test-session"

    database_memory.create_session(
        session_id
    )

    database_memory.save_message(
        session_id,
        "user",
        "Hello",
    )

    database_memory.save_message(
        session_id,
        "assistant",
        "Hello! How can I help?",
    )

    messages = database_memory.get_messages(
        session_id
    )

    assert messages == [
        {
            "role": "user",
            "content": "Hello",
        },
        {
            "role": "assistant",
            "content": "Hello! How can I help?",
        },
    ]


def test_database_memory_respects_limit(
    tmp_path,
    monkeypatch,
):
    database_path = tmp_path / "test_memory.db"

    monkeypatch.setattr(
        database_memory,
        "DATABASE_PATH",
        database_path,
    )

    database_memory.initialize_database()

    session_id = "limit-session"

    for number in range(5):
        database_memory.save_message(
            session_id,
            "user",
            f"Message {number}",
        )

    messages = database_memory.get_messages(
        session_id,
        limit=3,
    )

    assert len(messages) == 3

    assert messages[0]["content"] == "Message 2"
    assert messages[1]["content"] == "Message 3"
    assert messages[2]["content"] == "Message 4"


def test_database_memory_deletes_session(
    tmp_path,
    monkeypatch,
):
    database_path = tmp_path / "test_memory.db"

    monkeypatch.setattr(
        database_memory,
        "DATABASE_PATH",
        database_path,
    )

    database_memory.initialize_database()

    session_id = "delete-session"

    database_memory.save_message(
        session_id,
        "user",
        "This should be deleted.",
    )

    assert database_memory.get_messages(
        session_id
    )

    database_memory.delete_session(
        session_id
    )

    assert database_memory.get_messages(
        session_id
    ) == []
