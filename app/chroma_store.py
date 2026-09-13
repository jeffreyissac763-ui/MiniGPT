import chromadb


class ChromaVectorStore:
    def __init__(self, path="data/chroma", collection_name="minigpt"):
        self.client = chromadb.PersistentClient(path=path)

        self.collection_name = collection_name

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(
        self,
        text,
        embedding,
        document_id,
        metadata=None,
    ):
        self.collection.upsert(
            ids=[document_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata or {}],
        )

    def search(self, query_embedding, top_k=3):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        matches = []

        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        ids = results.get("ids", [[]])[0]

        for document_id, text, distance, metadata in zip(
            ids,
            documents,
            distances,
            metadatas,
        ):
            matches.append({
                "id": document_id,
                "text": text,
                "distance": distance,
                "metadata": metadata,
            })

        return matches

    def count(self):
        return self.collection.count()

    def clear(self):
        self.client.delete_collection(
            name=self.collection_name
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )
