from app.loader import load_document
from app.splitter import split_text
from app.embeddings import create_embedding
from app.vector_store import VectorStore


def build_index(file_path):
    document = load_document(file_path)

    chunks = split_text(document, chunk_size=200)

    vector_store = VectorStore()

    for chunk in chunks:
        embedding = create_embedding(chunk)

        vector_store.add(
            text=chunk,
            embedding=embedding,
        )

    return vector_store
