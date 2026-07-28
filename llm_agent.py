from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate

def get_answer(question: str, context_chunks: list):
    # Defaulting to a local llama3 model via Ollama
    llm = ChatOllama(model="llama3")
    
    prompt = PromptTemplate.from_template(
        "You are an AI Codebase Assistant. Answer the following question based on the provided code context.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )
    
    context_str = ""
    for chunk in context_chunks:
        line_info = f" (Line {chunk.get('line', 'Unknown')})" if 'line' in chunk else ""
        context_str += f"File: {chunk['source']}{line_info}\n{chunk['content']}\n\n"
        
    chain = prompt | llm
    response = chain.invoke({"context": context_str, "question": question})
    
    return response.content
