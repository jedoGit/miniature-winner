from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from app.loader import load_and_chunk
from app.vectorstore import update_vectorstore
from app.rag_chain import build_qa_chain
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings


from config import OPENAI_API_KEY

CHROMA_PATH = "vectorstore"
app = FastAPI()

class Query(BaseModel):
    question: str
    filters: dict | None = None

vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings())
qa_chain = build_qa_chain(vectorstore)

@app.post("/ask")
async def ask(query: Query):
    chain = build_qa_chain(vectorstore, filters=query.filters)
    result = chain(query.question)
    return {"answer": result["result"]}

@app.post("/upload")
async def upload(file: UploadFile = File(...), tags: str = Form("")):
    if not file.filename.endswith((".md", ".txt")):
        raise HTTPException(status_code=400, detail="Only .md and .txt files are allowed.")
    content = await file.read()
    if len(content) > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Max size is 2MB.")

    path = f"docs/{file.filename}"
    with open(path, "wb") as f:
        f.write(content)

    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    new_chunks = load_and_chunk(path, tags=tag_list)
    update_vectorstore(vectorstore, new_chunks)
    return {"status": "uploaded", "tags": tag_list}