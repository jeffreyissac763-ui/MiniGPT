from app.indexer import build_index


def main():
    print("Starting document indexing...")

    vector_store = build_index(
        "data/knowledge.txt"
    )

    print("Indexing complete!")
    print(
        "Documents in ChromaDB:",
        vector_store.count()
    )


if __name__ == "__main__":
    main()
