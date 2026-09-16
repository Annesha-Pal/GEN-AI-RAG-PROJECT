import os

from dotenv import load_dotenv
from google import genai
import chromadb

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Load environment variables
load_dotenv()


# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# --------------------------------------------------
# 1. Load PDF
# --------------------------------------------------

loader = PyMuPDFLoader(
    "data/document.pdf"
)

documents = loader.load()

print(
    "Number of pages:",
    len(documents)
)


# --------------------------------------------------
# 2. Split PDF into chunks
# --------------------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(
    documents
)

print(
    "Number of chunks:",
    len(chunks)
)


# --------------------------------------------------
# 3. Preview chunks
# --------------------------------------------------

print("\n-----------------------------")
print("CHUNK PREVIEW")
print("-----------------------------")

for i, chunk in enumerate(chunks[:5]):

    print(
        f"\nChunk {i + 1}"
    )

    print(
        "-----------------------------"
    )

    print(
        chunk.page_content
    )


# --------------------------------------------------
# 4. Create ChromaDB
# --------------------------------------------------

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="documents"
)


# --------------------------------------------------
# 5. Generate embeddings and store chunks
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
            f"chunk_{i}"
        ],
        documents=[
            text
        ],
        embeddings=[
            embedding
        ]
    )


print(
    "All chunks stored successfully!"
)

print(
    "Total documents in ChromaDB:",
    collection.count()
)