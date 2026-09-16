import os

from dotenv import load_dotenv
from google import genai
import chromadb


load_dotenv()


# --------------------------------------------------
# Gemini client
# --------------------------------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# --------------------------------------------------
# ChromaDB client
# --------------------------------------------------

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)


# --------------------------------------------------
# Retrieve relevant chunks
# --------------------------------------------------

def get_relevant_chunks(
    question,
    active_documents,
    k=5
):

    collection = chroma_client.get_collection(
        name="documents"
    )


    # --------------------------------------------------
    # Create question embedding
    # --------------------------------------------------

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    question_embedding = response.embeddings[0].values


    # --------------------------------------------------
    # Search only active documents
    # --------------------------------------------------

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=k,
        where={
            "source": {
                "$in": active_documents
            }
        },
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )


    # --------------------------------------------------
    # Extract results
    # --------------------------------------------------

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    relevant_chunks = []


    # --------------------------------------------------
    # Build relevant chunks
    # --------------------------------------------------

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        print(
            f"\nChunk {len(relevant_chunks) + 1}"
        )

        print(
            f"Source: "
            f"{metadata.get('source', 'Unknown')}"
        )

        print(
            f"Page: "
            f"{metadata.get('page', 'Unknown')}"
        )

        print(
            f"Distance: "
            f"{distance:.4f}"
        )

        print(
            "Text:"
        )

        print(
            document
        )

        print(
            "-----------------------------"
        )


        relevant_chunks.append(
            {
                "text": document,
                "page": metadata.get(
                    "page",
                    "Unknown"
                ),
                "source": metadata.get(
                    "source",
                    "Unknown"
                ),
                "distance": distance
            }
        )


    # --------------------------------------------------
    # Display retrieval results
    # --------------------------------------------------

    print("\n-----------------------------")
    print("RETRIEVAL RESULTS")
    print("-----------------------------")


    for i, chunk in enumerate(
        relevant_chunks
    ):

        print(
            f"Chunk {i + 1} | "
            f"Distance: {chunk['distance']:.4f} | "
            f"Source: {chunk['source']} | "
            f"Page: {chunk['page']}"
        )


    print(
        f"Relevant chunks: "
        f"{len(relevant_chunks)}"
    )

    print(
        "-----------------------------\n"
    )


    return relevant_chunks