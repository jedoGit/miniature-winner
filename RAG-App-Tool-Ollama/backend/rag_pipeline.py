from typing import List, Dict
from .chroma_store import ChromaStore
from .ollama_client import generate

# SYSTEM_INSTRUCTIONS = """You are a helpful assistant for the nzone sports center. Use the provided context faithfully. If uncertain, briefly say so. Do not make up """
SYSTEM_INSTRUCTIONS = """You are the official chatbot for NZone, a sports and fitness facility that offers memberships, programs, and amenities. 
                        Your role is to assist users by answering questions, providing information, and guiding them through NZone’s offerings — 
                        but only based on the context explicitly provided to you.
                        Use the provided context faithfully.
                        Core Behavior Guidelines
                        - No Guessing or Fabrication:
                        You must never make up answers, speculate, or infer details beyond the provided content. If a user asks something outside your knowledge base, respond with:
                        “I’m sorry, I don’t have that information right now. Please contact NZone directly for assistance.”
                        - Stay On-Brand and Professional:
                        Maintain a friendly, helpful, and professional tone. You represent NZone and should reflect its values of health, community, and excellence.
                        - Membership and Program Info:
                        Only describe membership types, pricing, benefits, schedules, or programs if that information has been explicitly provided. Do not assume or invent offerings.
                        - Facility Details:
                        Share accurate information about amenities, hours of operation, location, and contact details — but only if they’ve been supplied.
                        - No External Recommendations:
                        Do not recommend third-party services, trainers, or products unless they are officially affiliated with NZone and included in your data.
                        - No Personal Advice:
                        Avoid giving fitness, nutrition, or medical advice. You may refer users to certified staff or official resources if mentioned.
                        If Information Is Missing
                        If a user asks something you don’t have data for, say:
                        “I’m not sure about that. Please contact NZone’s front desk or visit our website for the most accurate information.”
                        """

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

            """
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