import pytest

pytestmark = pytest.mark.integration

from app.query_rewriter import rewrite_query


def test_query_rewriter_resolves_follow_up():
    conversation_history = [
        {
            "role": "user",
            "content": "What is Retrieval-Augmented Generation?",
        },
        {
            "role": "assistant",
            "content": (
                "Retrieval-Augmented Generation combines "
                "information retrieval with text generation."
            ),
        },
    ]

    question = "Why is it useful?"

    rewritten = rewrite_query(
        question,
        conversation_history,
    )

    assert rewritten
    assert "retrieval" in rewritten.lower()
    assert "generation" in rewritten.lower()
