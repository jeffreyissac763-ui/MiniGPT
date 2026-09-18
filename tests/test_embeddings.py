import pytest

pytestmark = pytest.mark.integration

from app.embeddings import create_embedding


def test_create_embedding():
    text = "Machine learning learns patterns from data."

    vector = create_embedding(text)

    assert vector is not None
    assert isinstance(vector, list)
    assert len(vector) > 0
    assert all(
        isinstance(value, (int, float))
        for value in vector
    )
