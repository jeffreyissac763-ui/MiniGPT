from app.retriever import retrieve


QUESTIONS = [
    "What is machine learning?",
    "What is RAG?",
    "What are embeddings?",
    "What is a vector database?",
    "What are large language models?",
]


def test_retrieval_quality():
    for question in QUESTIONS:
        results = retrieve(
            question,
            top_k=2,
        )

        assert isinstance(results, list)
        assert len(results) > 0
        assert len(results) <= 2

        for result in results:
            assert result["text"].strip()
            assert result["distance"] >= 0
            assert result["semantic_score"] >= 0
            assert result["keyword_score"] >= 0
            assert result["combined_score"] >= 0

            assert isinstance(
                result["metadata"],
                dict,
            )

            assert "source" in result["metadata"]
            assert "page" in result["metadata"]
            assert "chunk" in result["metadata"]

        scores = [
            result["combined_score"]
            for result in results
        ]

        assert scores == sorted(
            scores,
            reverse=True,
        )
