import pytest

pytestmark = pytest.mark.integration

from app.retriever import retrieve


def test_retriever_returns_relevant_results():
    question = "What is Retrieval-Augmented Generation?"

    results = retrieve(
        question,
        top_k=2,
    )

    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) <= 2

    top_result = results[0]

    assert "id" in top_result
    assert "text" in top_result
    assert "distance" in top_result
    assert "metadata" in top_result
    assert "semantic_score" in top_result
    assert "keyword_score" in top_result
    assert "combined_score" in top_result

    assert "Retrieval-Augmented Generation" in (
        top_result["text"]
    )

    assert top_result["metadata"]["source"] in [
        "knowledge.txt",
        "sample.pdf",
    ]

    for first, second in zip(
        results,
        results[1:],
    ):
        assert (
            first["combined_score"]
            >= second["combined_score"]
        )
