from app.loader import load_document


def test_load_text_document():
    document = load_document(
        "data/knowledge.txt"
    )

    assert isinstance(document, str)
    assert document.strip()
    assert len(document) > 0

    assert "Artificial Intelligence" in document
    assert "Machine Learning" in document


def test_load_pdf_document():
    document = load_document(
        "data/sample.pdf"
    )

    assert isinstance(document, list)
    assert len(document) > 0

    for page in document:
        assert isinstance(page, dict)
        assert "page" in page
        assert "text" in page

        assert isinstance(page["page"], int)
        assert isinstance(page["text"], str)

        assert page["text"].strip()

    assert len(document) == 10
