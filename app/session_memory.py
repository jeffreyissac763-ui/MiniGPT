from app.memory import ConversationMemory


class SessionMemoryStore:
    def __init__(self, max_messages=10):
        self.max_messages = max_messages
        self.sessions = {}

    def get_memory(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationMemory(
                max_messages=self.max_messages
            )

        return self.sessions[session_id]

    def clear_session(self, session_id):
        self.sessions.pop(
            session_id,
            None,
        )

    def session_exists(self, session_id):
        return session_id in self.sessions
