from ollama import embed


EMBEDDING_MODEL = "nomic-embed-text"


def create_embedding(text):
    response = embed(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response["embeddings"][0]
