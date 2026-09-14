from app.llm import generate_response
from app.retriever import retrieve
from app.query_rewriter import rewrite_query


MIN_COMBINED_SCORE = 0.55


def answer_with_rag(question, conversation_history=None, top_k=3):
    # Rewrite the question into a standalone search query
    # when conversation history is available.
    search_query = rewrite_query(
        question,
        conversation_history,
    )

    results = retrieve(
        search_query,
        top_k=top_k,
    )

    # Keep only results that pass the hybrid relevance threshold.
    results = [
        result
        for result in results
        if result.get("combined_score", 0.0)
        >= MIN_COMBINED_SCORE
    ]

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
   respond exactly with:
   The information is not available in the provided knowledge.
6. Do not mention Source 1, Source 2, etc.
7. Answer clearly and directly.
"""

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    answer = generate_response(messages)

    unavailable_patterns = [
        "information is not available",
        "information isn't available",
        "information is unavailable",
        "don't have information",
        "do not have information",
        "couldn't find any information",
        "could not find any information",
        "no information",
        "not found in the provided knowledge",
        "not available in the retrieved knowledge",
        "not in the provided knowledge",
    ]

    answer_lower = answer.lower()

    if any(
        pattern in answer_lower
        for pattern in unavailable_patterns
    ):
        return (
            "The information is not available in the "
            "provided knowledge."
        )

    sources = []

    for index, result in enumerate(results, start=1):
        metadata = result.get("metadata", {})

        source = metadata.get(
            "source",
            "Unknown source",
        )

        page = metadata.get(
            "page",
            "Unknown",
        )

        chunk = metadata.get(
            "chunk",
            "Unknown",
        )

        evidence = result["text"].replace(
            "\n",
            " ",
        ).strip()

        if len(evidence) > 300:
            evidence = evidence[:300] + "..."

        sources.append(
            f"[{index}] {source} "
            f"(page {page}, chunk {chunk})\n"
            f"    Evidence: {evidence}"
        )

    if sources:
        answer += "\n\nSources:\n" + "\n".join(sources)

    return answer
