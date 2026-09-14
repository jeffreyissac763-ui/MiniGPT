from app.loader import load_document


files = [
    "data/knowledge.txt",
    "data/sample.pdf",
]


for file_path in files:
    print("=" * 60)
    print("Testing:", file_path)

    text = load_document(file_path)

    print("Loaded successfully!")
    print("Characters:", len(text))
    print("Preview:")
    print(text[:300])
    print()
