from app.retriever import retrieve


question = "What is Retrieval-Augmented Generation?"

results = retrieve(
    question,
    top_k=2,
)

print("Question:")
print(question)
print()

for index, result in enumerate(results, start=1):
    print(f"--- Result {index} ---")
    print("ID:", result["id"])
    print("Distance:", result["distance"])
    print("Source:", result["metadata"].get("source"))
    print("Chunk:", result["metadata"].get("chunk"))
    print("Text:")
    print(result["text"])
    print()
