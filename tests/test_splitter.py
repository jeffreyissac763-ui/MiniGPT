from app.loader import load_document
from app.splitter import split_text


def test_text_splitter_creates_chunks():
    document = load_document(
        "data/knowledge.txt"
    )

    chunks = split_text(
        document,
        chunk_size=200,
    )

    assert isinstance(chunks, list)
    assert len(chunks) > 1

    assert all(
        isinstance(chunk, str)
        and chunk.strip()
        for chunk in chunks
    )

    combined_text = "\n".join(chunks)

    assert "Artificial Intelligence" in combined_text
    assert "Machine Learning" in combined_text
    assert "Retrieval-Augmented Generation" in combined_text
    assert "Vector Databases" in combined_text
