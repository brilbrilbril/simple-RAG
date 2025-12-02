from langchain_core.prompts import ChatPromptTemplate

prompt = """
You are an AI assistant that must answer the question using only the information contained in the provided context.

## Instructions:

1. Carefully analyze both the question and the context.
2. Provide a clear, complete, and well-structured answer.
3. Do NOT use outside knowledge.
4. Do NOT infer or assume anything that is not explicitly stated in the context.
5. If the context does not contain enough information to answer the question, say so explicitly.
6. Paraphrase the context into meaningful sentences rather than copying it verbatim.

Question: {question}
Context: {context}

Answer:
"""

prompt_template = ChatPromptTemplate.from_template(prompt)
