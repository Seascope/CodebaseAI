from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from repo_handler import clone_and_parse_repo

class RepoRequest(BaseModel):
    repo_url: str

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

@app.post("/upload")
def upload_repo(request: RepoRequest):
    try:
        repo_name, parsed_files = clone_and_parse_repo(request.repo_url)
        return {
            "message": f"Successfully cloned and parsed {repo_name}",
            "files_parsed": len(parsed_files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
