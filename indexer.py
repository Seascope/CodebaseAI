from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import os

# Initialize embeddings once
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def index_repository(repo_name, parsed_files):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    docs = []
    
    for file in parsed_files:
        path = file["path"]
        content = file["content"]
        if not content.strip():
            continue
            
        chunks = text_splitter.split_text(content)
        current_char = 0
        for i, chunk in enumerate(chunks):
            # approximate line number
            start_idx = content.find(chunk, current_char)
            if start_idx == -1:
                start_idx = current_char
            line_num = content.count('\n', 0, start_idx) + 1
            current_char = start_idx
            
            docs.append(
                Document(
                    page_content=chunk,
                    metadata={"source": path, "chunk_id": i, "repo": repo_name, "line": line_num}
                )
            )
            
    if not docs:
        return 0
        
    persist_directory = f"./chroma_db/{repo_name}"
    
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=repo_name
    )
    
    return len(docs)
