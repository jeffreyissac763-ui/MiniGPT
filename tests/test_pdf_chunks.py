from app.chroma_store import ChromaVectorStore


def test_pdf_chunks_exist():
    store = ChromaVectorStore()

    results = store.collection.get(
        where={
            "source": "sample.pdf"
        },
        include=[
            "documents",
            "metadatas",
        ],
    )

    documents = results["documents"]
    metadatas = results["metadatas"]

    assert len(documents) > 0
    assert len(documents) == len(metadatas)

    for document, metadata in zip(
        documents,
        metadatas,
    ):
        assert isinstance(document, str)
        assert document.strip()

        assert isinstance(metadata, dict)
        assert metadata["source"] == "sample.pdf"
        assert "page" in metadata
        assert "chunk" in metadata

        assert isinstance(metadata["page"], int)
        assert isinstance(metadata["chunk"], int)
