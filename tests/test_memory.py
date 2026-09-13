from app.memory import ConversationMemory


memory = ConversationMemory(max_messages=3)

memory.add_message("user", "Message 1")
memory.add_message("assistant", "Response 1")
memory.add_message("user", "Message 2")
memory.add_message("assistant", "Response 2")

print("Current memory:")
print(memory.get_history())

print()
print("Number of messages:", len(memory.get_history()))
