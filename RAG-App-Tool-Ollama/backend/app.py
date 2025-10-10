import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .schemas import ChatRequest, ChatResponse, IngestTextRequest, IngestUrlRequest, IngestMarkdownResponse, HealthResponse
from .chroma_store import ChromaStore
from .rag_pipeline import RAGPipeline
from .web_fetch import fetch_urls
from .md_ingest import load_markdown_file, chunk_markdown

app = FastAPI(title="RAG Markdown Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = ChromaStore()
rag = RAGPipeline(store)

@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    web_ctx = []
    if req.use_web and req.web_urls:
        web_ctx = [r for r in fetch_urls(req.web_urls) if "text" in r]
    res = rag.answer(req.query, top_k=req.top_k, web_contexts=web_ctx)
    return ChatResponse(answer=res["answer"], sources=res["sources"])

@app.post("/ingest_texts")
def ingest_texts(req: IngestTextRequest):
    rag.ingest_texts(req.texts, metadatas=req.metadatas)
    return {"status": "ingested", "count": len(req.texts)}

@app.post("/ingest_urls")
def ingest_urls(req: IngestUrlRequest):
    fetched = fetch_urls(req.urls)
    texts, metas = [], []
    for item in fetched:
        if "text" in item:
            texts.append(item["text"])
            metas.append({"source": item["url"], "title": item.get("title"), "domain": item.get("domain")})
    rag.ingest_texts(texts, metas)
    return {"status": "ingested", "count": len(texts)}

@app.post("/ingest_markdown", response_model=IngestMarkdownResponse)
async def ingest_markdown(file: UploadFile = File(...)):
    # Save temporarily
    tmp_path = os.path.join("data", "docs", file.filename)
    os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
    content = await file.read()
    with open(tmp_path, "wb") as f:
        f.write(content)

    # Load and chunk
    md_text, fm = load_markdown_file(tmp_path)
    chunks, metas = chunk_markdown(md_text)
    # Enrich metadata with frontmatter
    metas = [{**m, **fm, "source": file.filename} for m in metas]
    store.add_texts(chunks, metadatas=metas)

    return IngestMarkdownResponse(status="ingested", chunks_indexed=len(chunks), source=file.filename)