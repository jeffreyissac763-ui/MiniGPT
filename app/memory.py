class ConversationMemory:
    def __init__(self, max_messages=10):
        self.max_messages = max_messages
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content,
        })

        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def get_history(self):
        return self.messages

    def clear(self):
        self.messages.clear()
