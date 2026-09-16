# 🤖 GenAI RAG PDF Assistant

A **Retrieval-Augmented Generation (RAG) based PDF question-answering application** built with Python, Streamlit, ChromaDB, and Google Gemini.

The application allows users to upload PDF documents and ask questions about their content. Relevant sections are retrieved from the uploaded documents using semantic search and then provided to a Gemini language model to generate an answer grounded in the retrieved information.

---

## 📌 Features

*  Upload one or multiple PDF documents
*  Split documents into smaller text chunks
*  Generate semantic embeddings using Gemini
*  Retrieve the most relevant document chunks using vector similarity search
*  Generate answers using Gemini
*  Restrict answers to information available in the uploaded documents
*  Display source document and page information
*  Prevent duplicate ingestion of the same document
*  Clear stored documents from the vector database
*  Clear the current chat session
*  Simple interactive Streamlit interface

---

##  RAG Architecture

```text
                 PDF Upload
                     │
                     ▼
              PDF Text Extraction
                     │
                     ▼
               Text Chunking
                     │
                     ▼
            Gemini Embeddings
                     │
                     ▼
                ChromaDB
             Vector Database
                     │
                     │
              User Question
                     │
                     ▼
            Question Embedding
                     │
                     ▼
             Similarity Search
                     │
                     ▼
            Relevant PDF Chunks
                     │
                     ▼
              Gemini LLM
                     │
                     ▼
                Answer
                     │
                     ▼
             Source References
```

---

## 🛠️ Tech Stack

| Technology                   | Purpose                          |
| ---------------------------- | -------------------------------- |
| **Python**                   | Application and RAG pipeline     |
| **Streamlit**                | Web interface                    |
| **Google Gemini**            | Embeddings and answer generation |
| **ChromaDB**                 | Vector database                  |
| **LangChain Community**      | PDF loading                      |
| **LangChain Text Splitters** | Document chunking                |
| **PyMuPDF**                  | PDF text extraction              |
| **python-dotenv**            | Environment variable management  |

### Gemini Models

* **Embedding:** `gemini-embedding-001`
* **Generation:** `gemini-3.6-flash`

---

## 📂 Project Structure

```text
GEN-AI-RAG-PROJECT/
│
├── app.py                  # Streamlit application
│
├── src/
│   ├── __init__.py
│   ├── ingestion.py        # PDF processing and embedding
│   ├── retrieval.py        # Semantic search and retrieval
│   └── generation.py       # Gemini answer generation
│
├── data/                   # Local PDF documents
│
├── chroma_db/              # Local ChromaDB storage
│
├── embedding_test.py       # Embedding experiments
├── chroma_test.py          # ChromaDB experiments
├── ingest.py               # Initial ingestion experiments
├── retrieve.py             # Initial retrieval experiments
├── generate.py             # Initial generation experiments
├── test_api.py             # Gemini API testing
├── test_rag.py             # RAG pipeline testing
│
├── requirements.txt
├── .gitignore
└── README.md
```

> `chroma_db/`, `.env`, the virtual environment, and local PDF files are excluded from Git using `.gitignore`.

---

## 🔄 How It Works

### 1. PDF Ingestion

When a user uploads a PDF, the application extracts its text using **PyMuPDF**.

The extracted document is then divided into smaller chunks using a recursive text splitter.

Current configuration:

```text
Chunk size: 800 characters
Chunk overlap: 100 characters
```

The overlap helps preserve context between neighboring chunks.

---

### 2. Embedding Generation

Each text chunk is converted into a numerical vector using:

```text
gemini-embedding-001
```

These vectors represent the semantic meaning of the text and allow the application to search for relevant information based on meaning rather than exact keyword matches.

---

### 3. Vector Storage

The generated embeddings and their corresponding text are stored in **ChromaDB**.

Metadata is also stored with each chunk, including:

* Source PDF
* Page number

The application removes previously stored chunks belonging to the same PDF before re-ingesting it, preventing duplicate document entries.

---

### 4. Question Retrieval

When the user asks a question, the question is also converted into an embedding.

ChromaDB performs a vector similarity search to retrieve the most relevant document chunks.

The application currently retrieves the top **5 relevant chunks**.

---

### 5. Answer Generation

The retrieved chunks are passed to Gemini along with the user's question.

The prompt instructs the model to:

* Use only information from the retrieved document content
* Avoid using outside knowledge
* Avoid guessing or inventing information
* Combine information from multiple relevant chunks when necessary
* Return a fallback response when the answer cannot be found

This helps keep the generated response grounded in the uploaded documents.

---

## Getting Started

### Prerequisites

Make sure you have:

* Python 3.10+
* A Google Gemini API key
* Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/Annesha-Pal/GEN-AI-RAG-PROJECT.git
```

Navigate into the project:

```bash
cd GEN-AI-RAG-PROJECT
```

---

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure the Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

---

### 5. Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 💡 Example

After uploading a PDF, users can ask questions such as:

```text
Who is Jim?
```

or:

```text
Why did Della want to buy a gift for Jim?
```

The system retrieves relevant sections of the PDF and generates an answer based on those sections.

For questions unrelated to the uploaded document, the application is designed to respond:

```text
I could not find the answer in the document.
```

---

## Current Project Status

This project is currently a **learning and portfolio project** focused on understanding the core concepts behind Retrieval-Augmented Generation.

The implemented pipeline covers:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
Vector Database
 ↓
Similarity Search
 ↓
LLM
 ↓
Grounded Answer
```

The project is functional locally and demonstrates the fundamental RAG workflow.

---

## Future Improvements

Possible improvements for future versions include:

* [ ] Streaming LLM responses
* [ ] Improved document citation display
* [ ] Reranking retrieved chunks
* [ ] Hybrid keyword + semantic search
* [ ] Conversation memory
* [ ] Query expansion
* [ ] Retrieval evaluation and benchmarking
* [ ] Support for additional document formats
* [ ] Improved UI/UX
* [ ] Cloud deployment

---

## What I Learned

Through this project, I explored the fundamentals of building a RAG application, including:

* Document ingestion and preprocessing
* Text chunking and chunk overlap
* Semantic embeddings
* Vector databases
* Similarity search
* Retrieval pipelines
* LLM-based generation
* Prompt design for grounded responses
* Connecting a Python application with the Gemini API
* Building an interactive AI application using Streamlit

---

## Author

**Annesha Pal**

B.Tech Computer Science & Engineering

---

## License

This project is intended for educational and portfolio purposes.
