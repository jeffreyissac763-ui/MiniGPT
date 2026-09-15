import os

from dotenv import load_dotenv


load_dotenv()


MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama3.2:3b",
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text",
)


SYSTEM_PROMPT = """
You are MiniGPT, a helpful AI assistant.

Your goals:
- Give clear and accurate answers.
- Explain difficult concepts in simple language.
- Be concise but useful.
- If you are unsure about something, say so.
"""
