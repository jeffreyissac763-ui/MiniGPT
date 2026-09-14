from app.chroma_store import ChromaVectorStore


def test_chroma_store_add_and_search():
    store = ChromaVectorStore(
        path="data/test_chroma",
        collection_name="test_collection",
    )

    store.clear()

    try:
        embedding = [0.1, 0.2, 0.3]

        store.add(
            text="This is a test document.",
            embedding=embedding,
            document_id="test_001",
            metadata={
                "source": "test",
            },
        )

        assert store.count() == 1

        results = store.search(
            query_embedding=embedding,
            top_k=1,
        )

        assert len(results) == 1

        result = results[0]

        assert result["id"] == "test_001"
        assert result["text"] == "This is a test document."
        assert result["distance"] == 0.0
        assert result["metadata"]["source"] == "test"

    finally:
        store.clear()
