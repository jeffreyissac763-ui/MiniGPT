from app.indexer import build_index
from app.rag import answer_with_rag


vector_store = build_index("data/knowledge.txt")

question = "What is Retrieval-Augmented Generation?"

answer = answer_with_rag(
    vector_store,
    question,
)

print("Question:")
print(question)
print()

print("MiniGPT RAG Answer:")
print(answer)
