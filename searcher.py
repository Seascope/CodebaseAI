import os
from langchain_community.vectorstores import Chroma
from indexer import embeddings

def search_codebase(repo_name: str, query: str, top_k: int = 5):
    persist_directory = f"./chroma_db/{repo_name}"
    
    if not os.path.exists(persist_directory):
        raise ValueError(f"Repository {repo_name} has not been indexed yet.")
        
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name=repo_name
    )
    
    results = vectorstore.similarity_search(query, k=top_k)
    
    formatted_results = []
    for doc in results:
        formatted_results.append({
            "source": doc.metadata.get("source", "Unknown"),
            "content": doc.page_content
        })
        
    return formatted_results
