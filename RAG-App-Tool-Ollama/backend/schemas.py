from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str
    use_web: bool = True
    web_urls: Optional[List[str]] = None
    top_k: int = 6

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]

class IngestTextRequest(BaseModel):
    texts: List[str]
    metadatas: Optional[List[dict]] = None

class IngestUrlRequest(BaseModel):
    urls: List[str]

class IngestMarkdownResponse(BaseModel):
    status: str
    chunks_indexed: int
    source: str

class HealthResponse(BaseModel):
    status: str