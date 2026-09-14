import re

from app.database import get_vector_store
from app.embeddings import create_embedding


STOP_WORDS = {
    "a",
    "an",
    "the",
    "is",
    "are",
    "what",
    "how",
    "why",
    "of",
    "to",
    "in",
    "on",
    "for",
    "and",
    "with",
}


def tokenize(text):
    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower(),
    )

    return {
        word
        for word in words
        if word not in STOP_WORDS
    }


def keyword_score(query, text):
    query_words = tokenize(query)
    text_words = tokenize(text)

    if not query_words:
        return 0.0

    overlap = query_words.intersection(
        text_words
    )

    score = len(overlap) / len(query_words)

    normalized_query = " ".join(
        query.lower().split()
    )

    normalized_text = " ".join(
        text.lower().split()
    )

    if normalized_query in normalized_text:
        score += 0.5

    return min(score, 1.0)


def retrieve(
    query,
    top_k=3,
    max_distance=0.95,
):
    vector_store = get_vector_store()

    query_embedding = create_embedding(query)

    candidates = vector_store.search(
        query_embedding=query_embedding,
        top_k=20,
    )

    relevant_results = []

    for result in candidates:
        distance = result["distance"]

        if distance > max_distance:
            continue

        semantic_score = 1 / (
            1 + distance
        )

        lexical_score = keyword_score(
            query,
            result["text"],
        )

        combined_score = (
            0.6 * semantic_score
            + 0.4 * lexical_score
        )

        result["semantic_score"] = semantic_score
        result["keyword_score"] = lexical_score
        result["combined_score"] = combined_score

        relevant_results.append(result)

    relevant_results.sort(
        key=lambda item: item["combined_score"],
        reverse=True,
    )

    return relevant_results[:top_k]

