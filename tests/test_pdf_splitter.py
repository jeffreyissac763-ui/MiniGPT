from app.pdf_loader import load_pdf
from app.pdf_splitter import split_pdf_text


def test_pdf_splitter_creates_chunks():
    pages = load_pdf(
        "data/sample.pdf"
    )

    assert isinstance(pages, list)
    assert len(pages) > 0

    total_chunks = 0

    for page in pages:
        chunks = split_pdf_text(
            page["text"],
            chunk_size=500,
            overlap=100,
        )

        assert isinstance(chunks, list)
        assert len(chunks) > 0

        assert all(
            isinstance(chunk, str)
            and chunk.strip()
            for chunk in chunks
        )

        total_chunks += len(chunks)

    assert total_chunks > 1
