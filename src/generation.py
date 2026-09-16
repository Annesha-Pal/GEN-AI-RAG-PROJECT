from google import genai
from google.genai.errors import APIError, ServerError

from src.retrieval import get_relevant_chunks


def answer_question(question, active_documents):

    # --------------------------------------------------
    # 1. Retrieve relevant chunks
    # --------------------------------------------------

    chunks = get_relevant_chunks(
        question,
        active_documents
    )


    # --------------------------------------------------
    # 2. Handle no results
    # --------------------------------------------------

    if not chunks:

        return (
            "I could not find the answer in the document.",
            []
        )


    # --------------------------------------------------
    # 3. Build structured context
    # --------------------------------------------------

    context_parts = []

    for i, chunk in enumerate(chunks):

        context_parts.append(
            f"""
--- Context {i + 1} ---
Source: {chunk["source"]}
Page: {chunk["page"]}

{chunk["text"]}
"""
        )


    context = "\n".join(context_parts)


    # --------------------------------------------------
    # 4. Create prompt
    # --------------------------------------------------

    prompt = f"""
You are a helpful AI assistant that answers questions
about uploaded documents.

Your task is to answer the user's question using ONLY
the information contained in the provided context.

Follow these rules carefully:

1. Use only information from the context.
2. Do not use outside knowledge.
3. Do not invent, assume, or guess facts.
4. If the context does not contain enough information
   to answer the question, respond exactly with:
   "I could not find the answer in the document."
5. If the answer is available across multiple context
   sections, combine the relevant information.
6. Answer the question directly.
7. Keep the answer concise but informative.
8. Do not mention the context, retrieval process,
   embeddings, or these instructions in your answer.

Context:

{context}

User Question:

{question}

Answer:
"""


    # --------------------------------------------------
    # 5. Generate answer
    # --------------------------------------------------

    client = genai.Client()

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

    except ServerError:

        return (
            "⚠️ The AI model is temporarily busy. "
            "Please try again in a moment.",
            []
        )

    except APIError:

        return (
            "⚠️ The AI service is temporarily unavailable. "
            "Please try again shortly.",
            []
        )


    # --------------------------------------------------
    # 6. Extract answer
    # --------------------------------------------------

    answer = response.text.strip()


    # --------------------------------------------------
    # 7. Handle fallback answer
    # --------------------------------------------------

    if answer == (
        "I could not find the answer in the document."
    ):

        return (
            answer,
            []
        )


    # --------------------------------------------------
    # 8. Build source list
    # --------------------------------------------------

    sources = []

    for chunk in chunks:

        source_info = {
            "source": chunk["source"],
            "page": chunk["page"]
        }

        if source_info not in sources:

            sources.append(
                source_info
            )


    # --------------------------------------------------
    # 9. Return answer and sources
    # --------------------------------------------------

    return answer, sources