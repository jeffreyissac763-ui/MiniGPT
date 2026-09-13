import math


class VectorStore:
    def __init__(self):
        self.items = []

    def add(self, text, embedding):
        self.items.append({
            "text": text,
            "embedding": embedding,
        })

    def search(self, query_embedding, top_k=3):
        results = []

        for item in self.items:
            similarity = cosine_similarity(
                query_embedding,
                item["embedding"]
            )

            results.append({
                "text": item["text"],
                "similarity": similarity,
            })

        results.sort(
            key=lambda item: item["similarity"],
            reverse=True,
        )

        return results[:top_k]


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)
