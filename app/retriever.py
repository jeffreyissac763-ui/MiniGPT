from app.database import get_vector_store
from app.embeddings import create_embedding


def retrieve(query, top_k=3, max_distance=0.8):
    vector_store = get_vector_store()

    query_embedding = create_embedding(query)

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    relevant_results = [
        result
        for result in results
        if result["distance"] <= max_distance
    ]

    return relevant_results
