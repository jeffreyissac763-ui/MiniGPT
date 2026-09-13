from app.retriever import retrieve


questions = [
    "What is machine learning?",
    "What is RAG?",
    "What are embeddings?",
    "What is a vector database?",
    "What are large language models?",
]


for question in questions:
    print("=" * 60)
    print("Question:", question)
    print()

    results = retrieve(
        question,
        top_k=2,
    )

    for index, result in enumerate(results, start=1):
        print(f"--- Result {index} ---")
        print("Distance:", result["distance"])
        print("Text:")
        print(result["text"])
        print()
