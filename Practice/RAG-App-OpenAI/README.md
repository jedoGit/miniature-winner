# 🧠 RAG Q&A App

A Retrieval-Augmented Generation (RAG) application using LangChain, Chroma, FastAPI, and Streamlit.

## Features

- Upload markdown/txt documents
- Tag documents with metadata
- Ask questions with optional tag filtering
- Persistent vectorstore using Chroma

## Setup

```bash
python -m venv venv
on Linux: source venv/bin/activate
on Windows: source venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
streamlit run frontend/gui.py
```
