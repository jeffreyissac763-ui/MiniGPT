from app.indexer import build_index


def test_indexer_builds_text_index():
    vector_store = build_index(
        "data/knowledge.txt"
    )

    assert vector_store is not None
    assert vector_store.count() > 0
