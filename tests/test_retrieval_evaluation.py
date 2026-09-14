from app.retriever import retrieve


questions = [
    "What is Retrieval-Augmented Generation?",
    "What is production Retrieval-Augmented Generation?",
    "What are advanced chunking strategies?",
    "What is hybrid retrieval?",
    "What are vector databases?",
    "What is prompt injection?",
    "What is Kubernetes?",
]


for question in questions:

    print("=" * 80)
    print("QUESTION:", question)
    print("=" * 80)

    results = retrieve(
        question,
        top_k=3,
    )

    for index, result in enumerate(
        results,
        start=1,
    ):
        metadata = result.get(
            "metadata",
            {},
        )

        print(
            f"{index}. "
            f"Source={metadata.get('source')} | "
            f"Page={metadata.get('page')} | "
            f"Chunk={metadata.get('chunk')} | "
            f"Distance={result['distance']:.4f} | "
            f"Semantic={result['semantic_score']:.4f} | "
            f"Keyword={result['keyword_score']:.4f} | "
            f"Combined={result['combined_score']:.4f}"
        )

    print()
