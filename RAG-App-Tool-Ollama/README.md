# Gemma3 4B RAG App

A Python-based Retrieval-Augmented Generation app using Googles Gemma3 4B model. Upload documents, ask questions, and get context-aware answers.

## Setup

python -m venv .venv
on Linux: source .venv/bin/activate
on Windows: source .venv/Scripts/activate

1. Install dependencies: `pip install -r requirements.txt`
2. Start Ollama server: `ollama serve`, `ollama pull gemma3:4b`, `ollama pull nomic-embed-text:v1.5`
3. Run backend: `uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload`
4. Run frontend: `streamlit run frontend/ui.py`
