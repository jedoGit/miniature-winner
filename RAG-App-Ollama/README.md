# Gemma3 4B RAG App

A Python-based Retrieval-Augmented Generation app using Googles Gemma3 4B model. Upload documents, ask questions, and get context-aware answers.

## Setup

python -m venv venv
on Linux: source venv/bin/activate
on Windows: source venv/Scripts/activate

1. Install dependencies: `pip install -r requirements.txt`
2. Start Ollama with Gemini 4B: `ollama run gemma3:4b`
3. Run backend: `uvicorn backend.main:app --reload`
4. Run frontend: `streamlit run frontend/app.py`
