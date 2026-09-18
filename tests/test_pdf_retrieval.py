import pytest

pytestmark = pytest.mark.integration

from app.retriever import retrieve


def test_pdf_retrieval_returns_relevant_result():
    question = "What is production Retrieval-Augmented Generation?"

    results = retrieve(
        question,
        top_k=5,
    )

    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) <= 5

    pdf_results = [
        result
        for result in results
        if result.get("metadata", {}).get("source")
        == "sample.pdf"
    ]

    assert len(pdf_results) > 0

    top_pdf_result = pdf_results[0]

    metadata = top_pdf_result["metadata"]

    assert metadata["source"] == "sample.pdf"
    assert isinstance(metadata["page"], int)
    assert isinstance(metadata["chunk"], int)

    assert top_pdf_result["text"].strip()

    assert (
        "retrieval" in top_pdf_result["text"].lower()
        or "rag" in top_pdf_result["text"].lower()
    )

    assert "distance" in top_pdf_result
    assert "semantic_score" in top_pdf_result
    assert "keyword_score" in top_pdf_result
    assert "combined_score" in top_pdf_result
