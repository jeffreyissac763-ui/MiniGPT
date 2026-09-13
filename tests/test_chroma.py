import chromadb


client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_or_create_collection(
    name="minigpt"
)

print("ChromaDB connected successfully!")
print("Collection:", collection.name)
print("Documents:", collection.count())
