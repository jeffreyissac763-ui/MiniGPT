from app.loader import load_document
from app.splitter import split_text


document = load_document("data/knowledge.txt")
chunks = split_text(document, chunk_size=200)

print("Document length:", len(document))
print("Number of chunks:", len(chunks))
print()

for index, chunk in enumerate(chunks, start=1):
    print(f"--- Chunk {index} ---")
    print(chunk)
    print()
