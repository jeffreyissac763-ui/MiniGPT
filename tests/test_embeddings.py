from app.embeddings import create_embedding


text = "Machine learning learns patterns from data."

vector = create_embedding(text)

print("Embedding created successfully!")
print("Vector type:", type(vector))
print("Vector dimensions:", len(vector))
print("First 10 values:", vector[:10])
