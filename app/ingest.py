import sys

from app.indexer import build_index


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python -m app.ingest <file_path>")
        print()
        print("Examples:")
        print("  python -m app.ingest data/knowledge.txt")
        print("  python -m app.ingest data/sample.pdf")
        return

    file_path = sys.argv[1]

    print("=" * 60)
    print("MiniGPT Document Ingestion")
    print("=" * 60)
    print("Document:", file_path)
    print()
    print("Starting document indexing...")

    vector_store = build_index(file_path)

    print()
    print("Indexing complete!")
    print(
        "Total documents/chunks in ChromaDB:",
        vector_store.count()
    )


if __name__ == "__main__":
    main()
