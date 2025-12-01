from langchain_core.prompts import ChatPromptTemplate

prompt = """
You are an AI assistant answering questions based ONLY on the provided context.
- Analyze the question and context. 
- Answer with well-structured sentences.
- **Do not** make any assumptions.

Question: {question}  
Context: {context}  
Answer:
"""

prompt_template = ChatPromptTemplate.from_template(prompt)
