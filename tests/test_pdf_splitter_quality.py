from app.pdf_loader import load_pdf
from app.pdf_splitter import split_pdf_text


def test_pdf_splitter_quality():
    pages = load_pdf(
        "data/sample.pdf"
    )

    assert len(pages) >= 5

    page = pages[4]

    chunks = split_pdf_text(
        page["text"],
        chunk_size=500,
        overlap=100,
    )

    assert isinstance(chunks, list)
    assert len(chunks) > 1

    for chunk in chunks:
        assert isinstance(chunk, str)
        assert chunk.strip()

        # Chunks should contain meaningful content.
        assert len(chunk) >= 20

    # The splitter should preserve the important page content.
    combined_text = " ".join(chunks).lower()

    assert "retrieval" in combined_text
    assert "generation" in combined_text
