from pathlib import Path

from app.loader import load_document
from app.splitter import split_text
from app.embeddings import create_embedding
from app.chroma_store import ChromaVectorStore


def build_index(file_path):
    document = load_document(file_path)

    chunks = split_text(
        document,
        chunk_size=500,
        overlap=100,
    )

    vector_store = ChromaVectorStore()

    # Rebuild the collection so stale chunks cannot remain.
    vector_store.clear()

    source_name = Path(file_path).name

    for index, chunk in enumerate(chunks):
        embedding = create_embedding(chunk)

        vector_store.add(
            text=chunk,
            embedding=embedding,
            document_id=f"chunk_{index}",
            metadata={
                "source": source_name,
                "chunk": index,
            },
        )

    return vector_store
