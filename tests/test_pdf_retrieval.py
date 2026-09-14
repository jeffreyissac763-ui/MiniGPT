from app.retriever import retrieve


question = "What is production Retrieval-Augmented Generation?"

results = retrieve(
    question,
    top_k=5,
    max_distance=1.5,
)

print("Question:")
print(question)
print()

for index, result in enumerate(results, start=1):
    metadata = result.get("metadata", {})

    print("=" * 70)
    print(f"RESULT {index}")
    print("=" * 70)

    print("Source:", metadata.get("source"))
    print("Page:", metadata.get("page"))
    print("Chunk:", metadata.get("chunk"))
    print("Distance:", result["distance"])

    print()
    print("TEXT:")
    print(result["text"])
    print()
