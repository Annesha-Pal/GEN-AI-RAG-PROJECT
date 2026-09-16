import streamlit as st
import tempfile

from src.ingestion import ingest_document, clear_documents
from src.generation import answer_question


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Document AI Assistant",
    page_icon="📚",
    layout="centered"
)


# --------------------------------------------------
# Initialize Session State
# --------------------------------------------------

if "document_processed" not in st.session_state:
    st.session_state.document_processed = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "active_documents" not in st.session_state:
    st.session_state.active_documents = []


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>
h1 {
    text-align: center;
}

.center-text {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("AI PDF Reader")

st.markdown(
    '<div class="center-text">Upload PDFs and chat with your documents.</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("Documents")


    # --------------------------------------------------
    # PDF Upload
    # --------------------------------------------------

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"uploaded_files_{st.session_state.uploader_key}"
    )


    # --------------------------------------------------
    # Display Uploaded Files
    # --------------------------------------------------

    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} PDF(s) uploaded"
        )

        for file in uploaded_files:

            st.write(
                f"📄 {file.name}"
            )


        # --------------------------------------------------
        # Process Documents
        # --------------------------------------------------

        if st.button(
            "⚙️ Process Documents",
            type="primary"
        ):

            with st.spinner(
                "Processing documents..."
            ):

                for uploaded_file in uploaded_files:

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as temp_file:

                        temp_file.write(
                            uploaded_file.getbuffer()
                        )

                        pdf_path = temp_file.name


                    ingest_document(
                        pdf_path,
                        uploaded_file.name
                    )


            # Remember active documents
            st.session_state.active_documents = [
                uploaded_file.name
                for uploaded_file in uploaded_files
            ]

            st.session_state.document_processed = True

            st.session_state.messages = []

            st.success(
                "✅ Documents processed!"
            )


    st.divider()


    # --------------------------------------------------
    # Clear Documents
    # --------------------------------------------------

    if st.button("🗑️ Clear Documents"):

        clear_documents()

        st.session_state.document_processed = False

        st.session_state.active_documents = []

        st.session_state.messages = []

        st.session_state.uploader_key += 1

        st.rerun()


    # --------------------------------------------------
    # Clear Chat
    # --------------------------------------------------

    if st.button("💬 Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# --------------------------------------------------
# Document Status
# --------------------------------------------------

if st.session_state.document_processed:

    st.success(
        "📚 Documents are ready. You can start asking questions."
    )

else:

    st.info(
        "Please upload and process your PDF documents from the sidebar."
    )


# --------------------------------------------------
# Display Chat History
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

question = st.chat_input(
    "Ask something about your documents..."
)


# --------------------------------------------------
# Process Question
# --------------------------------------------------

if question:

    if not st.session_state.document_processed:

        st.warning(
            "Please upload and process a PDF first."
        )

    else:

        # Display user message
        with st.chat_message("user"):

            st.markdown(question)


        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        # Generate answer
        with st.chat_message("assistant"):

            with st.spinner(
                "Finding the answer..."
            ):

                answer, sources = answer_question(
                    question,
                    st.session_state.active_documents
                )

                st.markdown(answer)


                # Display sources only when available
                if sources:

                    st.markdown("**Sources:**")

                    for source in sources:

                        st.markdown(
                            f"📄 `{source['source']}` — "
                            f"Page {source['page']}"
                        )


        # Save AI response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

