from ollama import Client

from app.config import EMBEDDING_MODEL, OLLAMA_HOST


client = Client(
    host=OLLAMA_HOST,
)


def create_embedding(text):
    response = client.embed(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response["embeddings"][0]
