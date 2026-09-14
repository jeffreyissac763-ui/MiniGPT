from app.pdf_loader import load_pdf
from app.pdf_splitter import split_pdf_text

pages = load_pdf("data/sample.pdf")

page = pages[4]

chunks = split_pdf_text(
    page["text"],
    chunk_size=500,
    overlap=100,
)

print("Page 5 chunks:", len(chunks))
print()

for index, chunk in enumerate(chunks, start=1):
    preview = chunk[:120].replace("\n", " ")

    print(
        f"Chunk {index}: "
        f"{len(chunk)} chars | "
        f"{preview}"
    )
