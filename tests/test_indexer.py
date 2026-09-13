from app.indexer import build_index


vector_store = build_index("data/knowledge.txt")

print("Index built successfully!")
print("Number of stored chunks:", len(vector_store.items))
