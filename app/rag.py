from app.llm import generate_response
from app.retriever import retrieve


def answer_with_rag(question, conversation_history=None, top_k=3):
    results = retrieve(
        question,
        top_k=top_k,
    )

    # Hard grounding gate:
    # If no relevant knowledge was retrieved,
    # do not ask the LLM to answer from its own knowledge.
    if not results:
        return (
            "The information is not available in the "
            "provided knowledge."
        )

    context_parts = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"[Source {index}]\n"
            f"{result['text']}"
        )

    context = "\n\n".join(context_parts)

    history_text = ""

    if conversation_history:
        history_text = "\n\n".join(
            f"{message['role'].capitalize()}: {message['content']}"
            for message in conversation_history
        )

    prompt = f"""
You are MiniGPT, a grounded AI assistant.

Answer the user's question using ONLY the retrieved knowledge
and relevant conversation history.

RETRIEVED KNOWLEDGE:
{context}

CONVERSATION HISTORY:
{history_text}

CURRENT USER QUESTION:
{question}

RULES:
1. Use the retrieved knowledge when answering.
2. Use conversation history only to understand follow-up questions.
3. Do not use outside knowledge.
4. Do not invent or guess facts.
5. If the retrieved knowledge does not contain the answer,
   say that the information is not available in the provided knowledge.
6. Do not mention Source 1, Source 2, etc. in the natural answer.
7. Answer clearly and directly.
"""

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    answer = generate_response(messages)

    sources = []

    for index, result in enumerate(results, start=1):
        metadata = result.get("metadata", {})

        sources.append(
            f"[{index}] {metadata.get('source', 'Unknown source')} "
            f"(chunk {metadata.get('chunk', 'Unknown')})"
        )

    if sources:
        answer += "\n\nSources:\n" + "\n".join(sources)

    return answer
