from app.rag import answer_with_rag


def test_rag_returns_grounded_answer():
    question = "What is Retrieval-Augmented Generation?"

    answer = answer_with_rag(
        question,
    )

    assert isinstance(answer, str)
    assert answer.strip()

    assert "retrieval" in answer.lower()
    assert "generation" in answer.lower()

    assert "Sources:" in answer
    assert "knowledge.txt" in answer
