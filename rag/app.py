import requests
import streamlit as st

from rag.config import settings

API_URL = settings.API_URL

# Page config
st.set_page_config(page_title="PDF Q&A Assistant", page_icon="📄", layout="centered")

st.title("📄 PDF Q&A Assistant")
st.markdown("---")

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False
if "pdf_filename" not in st.session_state:
    st.session_state.pdf_filename = None

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded_file = st.file_uploader(
        "Upload your PDF file",
        type=["pdf"],
        help="Upload a PDF document to ask questions about",
    )

# Process uploaded PDF
if uploaded_file is not None and not st.session_state.pdf_uploaded:
    with st.spinner("Processing PDF..."):
        try:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf",
                )
            }
            response = requests.post(f"{API_URL}/process_pdf", files=files)

            if response.status_code == 200:
                result = response.json()
                st.session_state.pdf_uploaded = True
                st.session_state.pdf_filename = uploaded_file.name
                st.success(
                    f"PDF processed successfully! ({result['pages_processed']} pages, {result['chunks_created']} chunks)"
                )
            else:
                st.error(
                    f"Error processing PDF: {response.json().get('detail', 'Unknown error')}"
                )
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")

if st.session_state.pdf_uploaded:
    st.info(f"📄 Current document: **{st.session_state.pdf_filename}**")

st.markdown("---")

# Input query
st.subheader("Ask a question")
question = st.text_input(
    "Type your question here:",
    placeholder="What is this document about?",
    disabled=not st.session_state.pdf_uploaded,
    label_visibility="collapsed",
)

if st.button(
    "Ask", type="primary", disabled=not st.session_state.pdf_uploaded or not question
):
    if question:
        with st.spinner("Generating answer..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask", json={"question": question}, stream=True
                )

                if response.status_code == 200:
                    st.markdown("### Answer")
                    answer_placeholder = st.empty()
                    full_answer = ""

                    print("streaming response....")

                    for chunk in response.iter_content(
                        chunk_size=1, decode_unicode=True
                    ):
                        if chunk:
                            full_answer += chunk
                            answer_placeholder.markdown(full_answer + "▌")

                    answer_placeholder.markdown(full_answer)
                else:
                    error_detail = response.json().get("detail", "Unknown error")
                    st.error(f"Error: {error_detail}")
            except Exception as e:
                st.error(f"Error connecting to API: {str(e)}")

if not st.session_state.pdf_uploaded:
    st.markdown("---")
    st.info("👆 Please upload a PDF file to get started!")

if st.session_state.pdf_uploaded:
    st.markdown("---")
    if st.button("Upload a new PDF"):
        st.session_state.pdf_uploaded = False
        st.session_state.pdf_filename = None
        st.rerun()
