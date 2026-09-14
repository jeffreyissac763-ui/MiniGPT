from pathlib import Path

from app.pdf_loader import load_pdf


def load_document(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension == ".txt":
        return path.read_text(
            encoding="utf-8"
        )

    if extension == ".pdf":
        return load_pdf(file_path)

    raise ValueError(
        f"Unsupported document type: {extension}"
    )
