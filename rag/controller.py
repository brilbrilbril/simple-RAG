from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

from rag.config import settings


class RAGController:
    def __init__(self, embeddings, vectorstore, prompt_template):
        self.embeddings = embeddings
        self.vectorstore = vectorstore
        self.llm = ChatGoogleGenerativeAI(
            model=settings.CHAT_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            streaming=True,
            temperature=0.2,
        )
        self.prompt_template = prompt_template

    def format_docs(self, docs):
        return "\n\n".join([doc.page_content for doc in docs])

    def generate_stream_response(self, question):
        retriever = self.vectorstore.as_retriever(
            search_type="mmr", search_kwargs={"k": 5, "fetch_k": 10, "lambda_mult": 1}
        )
        qna_chain = (
            {"context": retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )

        for output in qna_chain.stream(question):
            yield output
