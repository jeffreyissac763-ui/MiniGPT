from pathlib import Path

from app.loader import load_document
from app.pdf_loader import load_pdf
from app.splitter import split_text
from app.pdf_splitter import split_pdf_text
from app.embeddings import create_embedding
from app.chroma_store import ChromaVectorStore


def build_index(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    vector_store = ChromaVectorStore()

    source_name = path.name

    # Remove only the previous version of this source.
    vector_store.delete_source(source_name)

    # --------------------------------------------------
    # PDF
    # --------------------------------------------------
    if path.suffix.lower() == ".pdf":
        pages = load_pdf(file_path)

        for page_data in pages:
            page_number = page_data["page"]
            page_text = page_data["text"]

            chunks = split_pdf_text(
                page_text,
                chunk_size=500,
                overlap=100,
            )

            for chunk_index, chunk in enumerate(chunks):
                embedding = create_embedding(chunk)

                document_id = (
                    f"{source_name}_"
                    f"page_{page_number}_"
                    f"chunk_{chunk_index}"
                )

                vector_store.add(
                    text=chunk,
                    embedding=embedding,
                    document_id=document_id,
                    metadata={
                        "source": source_name,
                        "page": page_number,
                        "chunk": chunk_index,
                        "file_type": "pdf",
                    },
                )

    # --------------------------------------------------
    # TXT
    # --------------------------------------------------
    elif path.suffix.lower() == ".txt":
        document = load_document(file_path)

        chunks = split_text(
            document,
            chunk_size=500,
            overlap=100,
        )

        for chunk_index, chunk in enumerate(chunks):
            embedding = create_embedding(chunk)

            document_id = (
                f"{source_name}_"
                f"chunk_{chunk_index}"
            )

            vector_store.add(
                text=chunk,
                embedding=embedding,
                document_id=document_id,
                metadata={
                    "source": source_name,
                    "page": 1,
                    "chunk": chunk_index,
                    "file_type": "txt",
                },
            )

    else:
        raise ValueError(
            f"Unsupported document type: {path.suffix}"
        )

    return vector_store
