from app.chroma_store import ChromaVectorStore


store = ChromaVectorStore()

results = store.collection.get(
    where={"source": "sample.pdf"},
    include=["documents", "metadatas"],
)

documents = results["documents"]
metadatas = results["metadatas"]

print("PDF chunks:", len(documents))
print()

for index, (document, metadata) in enumerate(
    zip(documents, metadatas),
    start=1,
):
    print("=" * 60)
    print(f"Chunk {index}")
    print("Page:", metadata.get("page"))
    print("Characters:", len(document))
    print("Preview:")
    print(document[:250].replace("\n", " "))
    print()
