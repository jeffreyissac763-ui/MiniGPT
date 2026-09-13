from app.rag import answer_with_rag


question = "What is Retrieval-Augmented Generation?"

answer = answer_with_rag(question)

print("Question:")
print(question)
print()

print("MiniGPT RAG Answer:")
print(answer)
