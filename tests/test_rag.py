from app.rag import answer_with_rag


def test_rag_returns_grounded_answer():
    question = "What is Retrieval-Augmented Generation?"

    result = answer_with_rag(
        question,
    )

    assert isinstance(result, dict)

    assert "answer" in result
    assert "sources" in result

    answer = result["answer"]

    assert isinstance(answer, str)
    assert answer.strip()

    assert "retrieval" in answer.lower()
    assert "generation" in answer.lower()

    sources = result["sources"]

    assert isinstance(sources, list)
    assert sources

    source = sources[0]

    assert source["source"] == "knowledge.txt"
    assert source["page"] == 1
    assert source["chunk"] == 4
    assert source["evidence"]


def test_rag_refuses_unknown_information():
    question = (
        "What is the capital city of Mars?"
    )

    result = answer_with_rag(
        question,
    )

    assert isinstance(result, dict)

    assert result["answer"] == (
        "The information is not available "
        "in the provided knowledge."
    )

    assert result["sources"] == []
