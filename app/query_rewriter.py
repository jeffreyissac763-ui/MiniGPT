from app.llm import generate_response


def rewrite_query(question, conversation_history=None):
    """
    Convert a follow-up question into a standalone
    search query using the previous conversation.
    """

    if not conversation_history:
        return question

    history_text = "\n\n".join(
        f"{message['role'].capitalize()}: {message['content']}"
        for message in conversation_history
    )

    prompt = f"""
You are a search query rewriting system.

Your job is to rewrite the user's current question
into a standalone question that can be searched
in a knowledge base.

CONVERSATION HISTORY:
{history_text}

CURRENT USER QUESTION:
{question}

RULES:
1. Resolve references such as "it", "this", "that",
   "they", and "them" using the conversation history.
2. Preserve the user's original meaning.
3. Do not answer the question.
4. Do not add information that is not present
   in the conversation.
5. If the current question is already standalone,
   return it unchanged.
6. Return ONLY the rewritten question.
7. Do not use quotes.
8. Do not add explanations.

REWRITTEN QUESTION:
"""

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    rewritten_query = generate_response(messages)

    rewritten_query = rewritten_query.strip()

    if not rewritten_query:
        return question

    return rewritten_query
