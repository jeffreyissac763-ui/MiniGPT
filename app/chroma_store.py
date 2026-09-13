import chromadb


class ChromaVectorStore:
    def __init__(self, path="data/chroma", collection_name="minigpt"):
        self.client = chromadb.PersistentClient(path=path)

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(self, text, embedding, document_id):
        self.collection.upsert(
            ids=[document_id],
            documents=[text],
            embeddings=[embedding],
        )

    def search(self, query_embedding, top_k=3):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        matches = []

        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for text, distance in zip(documents, distances):
            matches.append({
                "text": text,
                "distance": distance,
            })

        return matches

    def count(self):
        return self.collection.count()
