from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from repo_handler import clone_and_parse_repo

class RepoRequest(BaseModel):
    repo_url: str

class SearchRequest(BaseModel):
    repo_name: str
    query: str
    top_k: int = 5


import uvicorn

app = FastAPI(
    title="AI Codebase Assistant",
    description="API for the AI Codebase Assistant using RAG",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Codebase Assistant API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

from indexer import index_repository

@app.post("/upload")
def upload_repo(request: RepoRequest):
    try:
        repo_name, parsed_files = clone_and_parse_repo(request.repo_url)
        chunks_indexed = index_repository(repo_name, parsed_files)
        return {
            "message": f"Successfully cloned, parsed, and indexed {repo_name}",
            "files_parsed": len(parsed_files),
            "chunks_indexed": chunks_indexed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from searcher import search_codebase

@app.post("/search")
def search_repo(request: SearchRequest):
    try:
        results = search_codebase(request.repo_name, request.query, request.top_k)
        return {
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from llm_agent import get_answer

@app.post("/ask")
def ask_question(request: SearchRequest):
    try:
        results = search_codebase(request.repo_name, request.query, request.top_k)
        answer = get_answer(request.query, results)
        return {
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
