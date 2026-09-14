from app.loader import load_document


def test_load_text_document():
    document = load_document(
        "data/knowledge.txt"
    )

    assert isinstance(document, str)
    assert len(document) > 0
    assert "Artificial Intelligence" in document
    assert "Machine Learning" in document
