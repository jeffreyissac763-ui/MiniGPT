from app.chroma_store import ChromaVectorStore


store = ChromaVectorStore()

results = store.collection.get(
    where={
        "$and": [
            {
                "source": "sample.pdf"
            },
            {
                "page": 5
            },
        ]
    },
    include=[
        "documents",
        "metadatas",
    ],
)

print("Page 5 chunks:", len(results["documents"]))
print()

for index, (document, metadata) in enumerate(
    zip(
        results["documents"],
        results["metadatas"],
    ),
    start=1,
):
    print("=" * 70)
    print(f"CHUNK {index}")
    print("Chunk ID:", metadata.get("chunk"))
    print("Characters:", len(document))
    print()
    print(document)
    print()
