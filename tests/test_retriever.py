from app.indexer import build_index
from app.retriever import retrieve


vector_store = build_index("data/knowledge.txt")

results = retrieve(
    vector_store,
    "What is Retrieval-Augmented Generation?"
)

print("Retrieved results:")
print()

for index, result in enumerate(results, start=1):
    print(f"--- Result {index} ---")
    print("Similarity:", result["similarity"])
    print("Text:", result["text"])
    print()
