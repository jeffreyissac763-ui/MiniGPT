from ollama import Client

from app.config import MODEL_NAME, OLLAMA_HOST, SYSTEM_PROMPT


client = Client(
    host=OLLAMA_HOST,
)


def generate_response(messages):
    messages_with_system_prompt = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ] + messages

    response = client.chat(
        model=MODEL_NAME,
        messages=messages_with_system_prompt,
    )

    return response.message.content
