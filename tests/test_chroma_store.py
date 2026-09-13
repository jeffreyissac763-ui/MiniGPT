from app.chroma_store import ChromaVectorStore


store = ChromaVectorStore(
    path="data/test_chroma",
    collection_name="test_collection",
)

embedding = [0.1, 0.2, 0.3]

store.add(
    text="This is a test document.",
    embedding=embedding,
    document_id="test_001",
)

print("Document stored successfully!")
print("Documents in database:", store.count())
