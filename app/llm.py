from ollama import chat
from app.config import MODEL_NAME, SYSTEM_PROMPT


def generate_response(messages):
    messages_with_system_prompt = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ] + messages

    response = chat(
        model=MODEL_NAME,
        messages=messages_with_system_prompt,
    )

    return response.message.content
