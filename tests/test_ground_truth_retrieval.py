import pytest

pytestmark = pytest.mark.integration

from app.retriever import retrieve


EVALUATION_CASES = [
    {
        "question": "What is Artificial Intelligence?",
        "expected_source": "knowledge.txt",
        "expected_text": "Artificial Intelligence",
    },
    {
        "question": "What is Machine Learning?",
        "expected_source": "knowledge.txt",
        "expected_text": "Machine Learning",
    },
    {
        "question": "What is Deep Learning?",
        "expected_source": "knowledge.txt",
        "expected_text": "Deep Learning",
    },
    {
        "question": "What are Large Language Models?",
        "expected_source": "knowledge.txt",
        "expected_text": "Large Language Models",
    },
    {
        "question": "What is Retrieval-Augmented Generation?",
        "expected_source": "knowledge.txt",
        "expected_text": "Retrieval-Augmented Generation",
    },
    {
        "question": "What are embeddings?",
        "expected_source": "knowledge.txt",
        "expected_text": "Embeddings",
    },
    {
        "question": "What are vector databases?",
        "expected_source": "knowledge.txt",
        "expected_text": "Vector Databases",
    },
]


def test_ground_truth_retrieval():
    for case in EVALUATION_CASES:
        results = retrieve(
            case["question"],
            top_k=3,
        )

        assert results, (
            f"No retrieval results for: "
            f"{case['question']}"
        )

        top_result = results[0]

        assert (
            top_result["metadata"]["source"]
            == case["expected_source"]
        ), (
            f"Unexpected source for: "
            f"{case['question']}"
        )

        assert (
            case["expected_text"].lower()
            in top_result["text"].lower()
        ), (
            f"Expected topic "
            f"'{case['expected_text']}' "
            f"was not found in the top result for: "
            f"{case['question']}"
        )


def test_recall_at_3():
    hits = 0

    for case in EVALUATION_CASES:
        results = retrieve(
            case["question"],
            top_k=3,
        )

        assert results, (
            f"No retrieval results for: "
            f"{case['question']}"
        )

        found = any(
            case["expected_source"]
            == result["metadata"]["source"]
            and case["expected_text"].lower()
            in result["text"].lower()
            for result in results
        )

        if found:
            hits += 1

    recall_at_3 = (
        hits / len(EVALUATION_CASES)
    )

    assert recall_at_3 == 1.0
