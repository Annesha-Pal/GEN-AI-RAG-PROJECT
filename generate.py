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


# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_collection(
    name="documents"
)


# --------------------------------------------------
# Retrieve relevant chunks
# --------------------------------------------------

def get_relevant_chunks(question, k=3):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    question_embedding = response.embeddings[0].values

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=k
    )

    return results["documents"][0]


# --------------------------------------------------
# Generate answer
# --------------------------------------------------

def answer_question(question):

    chunks = get_relevant_chunks(question)

    context = "\n\n".join(chunks)

    prompt = f"""
Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context,
say: "I could not find the answer in the document."

Do not use outside knowledge.

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# --------------------------------------------------
# Test
# --------------------------------------------------

question = input("Ask a question about your document: ")

answer = answer_question(question)

print("\nAnswer:")
print(answer)