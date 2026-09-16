import chromadb

from google import genai
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def ingest_document(pdf_path, file_name):

    # --------------------------------------------------
    # 1. Load PDF
    # --------------------------------------------------

    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()

    print("Number of pages:", len(documents))


    # --------------------------------------------------
    # 2. Split PDF into chunks
    # --------------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print("Number of chunks:", len(chunks))


    # --------------------------------------------------
    # 3. Connect to ChromaDB
    # --------------------------------------------------

    chroma_client = chromadb.PersistentClient(
        path="./chroma_db"
    )


    # --------------------------------------------------
    # 4. Get or create collection
    # --------------------------------------------------

    try:

        collection = chroma_client.get_collection(
            name="documents"
        )

        print("Existing document collection found.")

    except Exception:

        collection = chroma_client.create_collection(
            name="documents"
        )

        print("New document collection created.")


    # --------------------------------------------------
    # 5. Remove old chunks of the same PDF
    # --------------------------------------------------

    existing = collection.get(
        where={
            "source": file_name
        }
    )

    if existing["ids"]:

        collection.delete(
            ids=existing["ids"]
        )

        print(
            f"Removed {len(existing['ids'])} old chunks "
            f"for {file_name}"
        )


    # --------------------------------------------------
    # 6. Gemini client
    # --------------------------------------------------

    client = genai.Client()


    # --------------------------------------------------
    # 7. Create embeddings and store chunks
    # --------------------------------------------------

    for i, chunk in enumerate(chunks):

        text = chunk.page_content

        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        embedding = response.embeddings[0].values


        collection.add(
            ids=[
                f"{file_name}_chunk_{i}"
            ],

            documents=[
                text
            ],

            embeddings=[
                embedding
            ],

            metadatas=[
                {
                    "page": chunk.metadata.get(
                        "page",
                        0
                    ) + 1,

                    "source": file_name
                }
            ]
        )


    # --------------------------------------------------
    # 8. Final information
    # --------------------------------------------------

    print(
        f"Successfully stored {file_name}"
    )

    print(
        "Total documents in ChromaDB:",
        collection.count()
    )


def clear_documents():

    chroma_client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    try:

        chroma_client.delete_collection(
            name="documents"
        )

        print(
            "All documents deleted from ChromaDB."
        )

    except Exception:

        print(
            "No document collection found."
        )