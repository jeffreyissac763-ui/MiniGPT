from app.database import get_vector_store
from app.embeddings import create_embedding


def retrieve(query, top_k=3):
    vector_store = get_vector_store()

    query_embedding = create_embedding(query)

    return vector_store.search(
        query_embedding=query_embedding,
        top_k=top_k,
    )
