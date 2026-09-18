import pytest

pytestmark = pytest.mark.integration

from app.chroma_store import ChromaVectorStore


def test_page5_chunks_exist():
    store = ChromaVectorStore()

    results = store.collection.get(
        where={
            "$and": [
                {
                    "source": "sample.pdf"
                },
                {
                    "page": 5
                },
            ]
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
        assert metadata["page"] == 5
        assert "chunk" in metadata
