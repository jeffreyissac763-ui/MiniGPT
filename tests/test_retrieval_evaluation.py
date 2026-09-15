
from app.retriever import retrieve


QUESTIONS = [
    "What is Retrieval-Augmented Generation?",
    "What is production Retrieval-Augmented Generation?",
    "What are advanced chunking strategies?",
    "What is hybrid retrieval?",
    "What are vector databases?",
    "What is prompt injection?",
    "What is Kubernetes?",
]


def test_retrieval_evaluation():
    for question in QUESTIONS:
        results = retrieve(
            question,
            top_k=3,
        )

        assert isinstance(results, list)
        assert len(results) > 0
        assert len(results) <= 3

        for result in results:
            assert "text" in result
            assert "distance" in result
            assert "semantic_score" in result
            assert "keyword_score" in result
            assert "combined_score" in result
            assert "metadata" in result

            assert result["text"].strip()

            metadata = result["metadata"]

            assert "source" in metadata
            assert "page" in metadata
            assert "chunk" in metadata

        scores = [
            result["combined_score"]
            for result in results
        ]

        assert scores == sorted(
            scores,
            reverse=True,
        )
