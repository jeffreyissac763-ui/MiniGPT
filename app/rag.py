from app.llm import generate_response
from app.retriever import retrieve


def answer_with_rag(question, top_k=3):
    results = retrieve(
        question,
        top_k=top_k,
    )

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    prompt = f"""
Answer the user's question using the provided context.

Context:
{context}

User question:
{question}

If the answer cannot be found in the context, say that the information is not available in the provided knowledge.
"""

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    return generate_response(messages)
