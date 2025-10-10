import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from .ollama_client import embed_texts
from .config import CHROMA_PERSIST_DIR

class ChromaStore:
    def __init__(self, collection_name: str = "rag_docs"):
        self.client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR,
            settings=Settings(allow_reset=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] | None = None, ids: List[str] | None = None):
        if ids is None:
            ids = [f"doc-{i}" for i in range(len(texts))]
        
        # print("id: " + str(ids))

        # print("texts: " + str(texts))
        # print("embeddings: " + str(embeddings))

        embeddings = embed_texts(texts)
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas or [{} for _ in texts],
        )

    def query(self, query: str, top_k: int = 6):
        q_emb = embed_texts([query])[0]
        res = self.collection.query(
            query_embeddings=[q_emb],
            n_results=top_k,
        )
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        ids = res.get("ids", [[]])[0]
        distances = res.get("distances", [[]])[0]
        return [
            {"id": i, "text": d, "metadata": m, "score": s}
            for i, d, m, s in zip(ids, docs, metas, distances)
        ]