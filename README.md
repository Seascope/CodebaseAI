# CodebaseAI

An AI-powered codebase assistant using Retrieval-Augmented Generation (RAG) to understand your repositories. Upload any GitHub repository, and chat with it to understand its architecture, find where authentication is handled, or locate dead code.

## Key Features
- **Semantic Code Search**: Uses vector embeddings and ChromaDB.
- **RAG Architecture**: Answers questions using context from your own code.
- **Source Citations**: Highlights file names and line numbers.
- **Local LLMs**: Powered by Ollama.
- **FastAPI Backend**: Robust REST API for repository indexing and querying.
- **Premium React Frontend**: Sleek glassmorphism UI built without node.js.

## Quickstart

1. Clone this repository.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Start an Ollama server locally:
```bash
ollama run llama3
```
4. Run the application:
```bash
python main.py
```
5. Open `http://localhost:8000/` in your browser.
