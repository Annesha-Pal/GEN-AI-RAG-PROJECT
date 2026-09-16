import os

from dotenv import load_dotenv
from google import genai
import chromadb


# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Connect to existing ChromaDB
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_collection(
    name="documents"
)


# --------------------------------------------------
# Retrieval function
# --------------------------------------------------

def get_relevant_chunks(question, k=3):

    # Convert the question into an embedding
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    question_embedding = response.embeddings[0].values

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=k
    )

    return results["documents"][0]


# --------------------------------------------------
# Test retrieval
# --------------------------------------------------

question = input("Ask a question about your document: ")

chunks = get_relevant_chunks(question)

print("\nRelevant chunks:\n")

for i, chunk in enumerate(chunks, start=1):

    print(f"--- Chunk {i} ---")
    print(chunk)
    print()