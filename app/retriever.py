from app.embeddings import create_embedding


def retrieve(vector_store, query, top_k=3):
    query_embedding = create_embedding(query)

    return vector_store.search(
        query_embedding=query_embedding,
        top_k=top_k,
    )
