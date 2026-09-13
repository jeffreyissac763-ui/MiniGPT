from app.llm import generate_response
from app.memory import ConversationMemory


def main():
    memory = ConversationMemory(max_messages=10)

    print("================================")
    print("        MiniGPT Chatbot")
    print("================================")
    print("Type 'exit' to quit.")
    print()

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("MiniGPT: Goodbye!")
            break

        memory.add_message("user", user_input)

        assistant_response = generate_response(
            memory.get_history()
        )

        memory.add_message("assistant", assistant_response)

        print("MiniGPT:", assistant_response)
        print()


if __name__ == "__main__":
    main()
