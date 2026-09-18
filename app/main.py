from app.rag import answer_with_rag
from app.memory import ConversationMemory


def main():
    memory = ConversationMemory(max_messages=10)

    print("================================")
    print("      MiniGPT RAG Chatbot")
    print("================================")
    print("Ask questions about your knowledge base.")
    print("MiniGPT now remembers recent conversation.")
    print("Type 'exit' to quit.")
    print()

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("MiniGPT: Goodbye!")
            break

        conversation_history = memory.get_history()

        result = answer_with_rag(
            question=user_input,
            conversation_history=conversation_history,
            top_k=3,
        )

        answer = result["answer"]

        memory.add_message(
            "user",
            user_input,
        )

        memory.add_message(
            "assistant",
            answer,
        )

        print("MiniGPT:", answer)

        if result["sources"]:
            print()
            print("Sources:")

            for source in result["sources"]:
                location = (
                    f"{source['source']} "
                    f"| Page {source['page']} "
                    f"| Chunk {source['chunk']}"
                )

                print(f"- {location}")

            print()

        print()


if __name__ == "__main__":
    main()
