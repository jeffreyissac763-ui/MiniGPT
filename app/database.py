from app.chroma_store import ChromaVectorStore


def get_vector_store():
    return ChromaVectorStore(
        path="data/chroma",
        collection_name="minigpt",
    )
