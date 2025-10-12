from fastapi import FastAPI, UploadFile
from backend.document_loader import load_and_chunk
from backend.vector_store import store_chunks, retrieve_chunks
from backend.ollama_client import generate_answer

app = FastAPI()

@app.post("/upload/")
async def upload(file: UploadFile):
    chunks = load_and_chunk(await file.read())
    store_chunks(chunks)
    return {"message": "Document processed"}

@app.get("/query/")
def query(q: str):
    context = retrieve_chunks(q)
    answer = generate_answer(q, context)
    return {"answer": answer}