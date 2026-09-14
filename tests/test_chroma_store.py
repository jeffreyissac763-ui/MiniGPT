from app.chroma_store import ChromaVectorStore


store = ChromaVectorStore(
    path="data/test_chroma",
    collection_name="test_collection",
)

store.clear()

embedding = [0.1, 0.2, 0.3]

store.add(
    text="This is a test document.",
    embedding=embedding,
    document_id="test_001",
    metadata={
        "source": "test",
    },
)

print("Document added successfully!")

results = store.search(
    query_embedding=embedding,
    top_k=1,
)

print("Search results:", results)

print("Document count:", store.count())

store.clear()

print("ChromaDB test completed successfully!")
