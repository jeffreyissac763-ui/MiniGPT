from app.pdf_loader import load_pdf
from app.pdf_splitter import split_pdf_text


pages = load_pdf(
    "data/sample.pdf"
)

total_chunks = 0

for page in pages:
    chunks = split_pdf_text(
        page["text"],
        chunk_size=500,
        overlap=100,
    )

    total_chunks += len(chunks)

    print(
        f"Page {page['page']}: "
        f"{len(chunks)} chunks"
    )

    if chunks:
        print(
            "First chunk characters:",
            len(chunks[0])
        )

print()
print("Total PDF chunks:", total_chunks)
