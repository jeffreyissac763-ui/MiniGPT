import chromadb


def test_chromadb_connection():
    client = chromadb.PersistentClient(
        path="data/chroma"
    )

    collection = client.get_or_create_collection(
        name="minigpt"
    )

    assert client is not None
    assert collection is not None
    assert collection.name == "minigpt"
    assert collection.count() > 0
