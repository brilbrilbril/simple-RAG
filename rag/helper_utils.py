import tempfile

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.config import settings


def init_embedding():
    embedding = GoogleGenerativeAIEmbeddings(
        model=settings.EMBEDDING_MODEL, google_api_key=settings.GEMINI_API_KEY
    )
    return embedding


# load the pdf using PyMuPDFLoader
def process_pdf(pdf_file):
    """Processes the uploaded PDF using PyMuPDFLoader."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_file.read())
        temp_pdf_path = temp_pdf.name
    loader = PyMuPDFLoader(temp_pdf_path)
    docs = loader.load()
    return docs


def chunk_docs(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", ".", "!", "?"],
    )
    chunks = text_splitter.split_documents(docs)
    return chunks


# create embeddings and store it in vectorstore & bm25
def embed_docs(chunks, vectorstore):
    vectorstore.add_documents(documents=chunks)
    return vectorstore
