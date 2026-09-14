from app.memory import ConversationMemory


def test_memory_keeps_only_recent_messages():
    memory = ConversationMemory(max_messages=3)

    memory.add_message("user", "Message 1")
    memory.add_message("assistant", "Response 1")
    memory.add_message("user", "Message 2")
    memory.add_message("assistant", "Response 2")

    history = memory.get_history()

    assert len(history) == 3

    assert history[0]["content"] == "Response 1"
    assert history[1]["content"] == "Message 2"
    assert history[2]["content"] == "Response 2"
