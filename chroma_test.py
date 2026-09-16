import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)

collection.add(
    documents=[
        "Artificial intelligence allows computers to perform tasks that normally require human intelligence.",
        "Machine learning is a subset of artificial intelligence that allows systems to learn from data.",
        "Deep learning uses neural networks with multiple layers."
    ],
    ids=[
        "doc1",
        "doc2",
        "doc3"
    ]
)

print("Documents stored successfully!")

print("Number of documents:",
      collection.count())