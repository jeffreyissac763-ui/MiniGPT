from app.pdf_loader import load_pdf


def test_load_pdf():
    pages = load_pdf(
        "data/sample.pdf"
    )

    assert isinstance(pages, list)
    assert len(pages) > 0

    for page in pages:
        assert isinstance(page, dict)
        assert "page" in page
        assert "text" in page

        assert isinstance(page["page"], int)
        assert isinstance(page["text"], str)
        assert page["text"].strip()

    assert len(pages) == 10
