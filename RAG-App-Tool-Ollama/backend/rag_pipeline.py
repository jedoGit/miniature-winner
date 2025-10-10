from typing import List, Dict
from .chroma_store import ChromaStore
from .ollama_client import generate

SYSTEM_INSTRUCTIONS = """You are a helpful assistant. Use the provided context faithfully. If uncertain, briefly say so. Cite sources inline as [n] matching the list of sources."""

def build_prompt(query: str, vect_contexts: List[Dict], web_contexts: List[Dict]) -> str:
    ctx_lines = []
    source_index = 1
    source_map = []

    for vc in vect_contexts:
        label = vc.get("metadata", {}).get("source", vc.get("id"))
        ctx_lines.append(f"[{source_index}] (vector) {vc['text']}")
        source_map.append({"idx": source_index, "label": label})
        source_index += 1

    for wc in web_contexts:
        if "text" in wc:
            label = wc.get("url")
            ctx_lines.append(f"[{source_index}] (web {wc.get('domain')}) {wc['text']}")
            source_map.append({"idx": source_index, "label": label})
            source_index += 1

    sources_list = "\n".join([f"[{s['idx']}] {s['label']}" for s in source_map])

    prompt = f"""{SYSTEM_INSTRUCTIONS}

User question:
{query}

Context snippets:
{'\n'.join(ctx_lines)}

Sources:
{sources_list}

Answer concisely. Use [n] to cite the sources you relied on."""
    return prompt, source_map

class RAGPipeline:
    def __init__(self, store: ChromaStore):
        self.store = store

    def answer(self, query: str, top_k: int = 6, web_contexts: List[Dict] | None = None) -> Dict:
        vect = self.store.query(query, top_k=top_k)
        web_ctx = web_contexts or []
        prompt, source_map = build_prompt(query, vect, web_ctx)
        answer = generate(prompt)
        sources = [{"index": s["idx"], "label": s["label"]} for s in source_map]
        return {"answer": answer, "sources": sources}

    def ingest_texts(self, texts: List[str], metadatas: List[dict] | None = None):
        chunks, meta_out = [], []
        metadatas = metadatas or [{} for _ in texts]
        from .utils import chunk_text
        for t, m in zip(texts, metadatas):
            for ch in chunk_text(t):
                chunks.append(ch)
                meta_out.append(m)
        self.store.add_texts(chunks, metadatas=meta_out)