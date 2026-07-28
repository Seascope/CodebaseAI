from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def get_answer(question: str, context_chunks: list, history: list = None):
    # Defaulting to a local llama3 model via Ollama
    llm = ChatOllama(model="llama3")
    
    messages = [
        SystemMessage(content="You are an AI Codebase Assistant. Answer the following question based on the provided code context and previous conversation history.")
    ]
    
    if history:
        for msg in history:
            if msg.get("role") == "user":
                messages.append(HumanMessage(content=msg.get("content", "")))
            else:
                messages.append(AIMessage(content=msg.get("content", "")))
                
    context_str = ""
    for chunk in context_chunks:
        line_info = f" (Line {chunk.get('line', 'Unknown')})" if 'line' in chunk else ""
        context_str += f"File: {chunk['source']}{line_info}\n{chunk['content']}\n\n"
        
    final_prompt = f"Context:\n{context_str}\n\nQuestion: {question}"
    messages.append(HumanMessage(content=final_prompt))
    
    response = llm.invoke(messages)
    return response.content
