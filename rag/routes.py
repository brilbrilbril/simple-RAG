from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from rag.controller import RAGController
from rag.helper_utils import (chunk_docs, embed_docs, init_embedding,
                              process_pdf)
from rag.init_qdrant import init_vectorstore
from rag.prompt import prompt_template

app = FastAPI()

# Global state
embeddings = None
vectorstore = None
rag_controller = None


class QuestionRequest(BaseModel):
    question: str


@app.post("/process_pdf")
async def process_pdf_endpoint(file: UploadFile = File(...)):
    global embeddings, vectorstore, rag_controller

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        print(f"Processing PDF: {file.filename}")
        docs = process_pdf(file.file)
        print(f"Loaded {len(docs)} pages from PDF")

        chunks = chunk_docs(docs)
        print(f"Created {len(chunks)} chunks")

        embeddings = init_embedding()

        vectorstore = init_vectorstore(embeddings)
        vectorstore = embed_docs(chunks, vectorstore)
        print("Embeddings created and stored successfully")

        prompt = prompt_template
        rag_controller = RAGController(embeddings, vectorstore, prompt)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "PDF processed successfully",
                "filename": file.filename,
                "pages_processed": len(docs),
                "chunks_created": len(chunks),
            },
        )

    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    global rag_controller

    if rag_controller is None:
        raise HTTPException(
            status_code=400,
            detail="No PDF has been processed yet. Please upload a PDF first.",
        )

    try:
        return StreamingResponse(
            rag_controller.generate_stream_response(request.question),
            media_type="text/plain",
        )
    except Exception as e:
        print(f"Error generating response: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error generating response: {str(e)}"
        )


@app.get("/")
async def root():
    return {
        "message": "PDF Processing API",
        "endpoints": {
            "/process_pdf": "POST - Upload and process a PDF file",
            "/ask": "POST - Ask questions about the processed PDF",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
