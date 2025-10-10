import requests
from .config import OLLAMA_BASE_URL, GENERATION_MODEL, EMBEDDING_MODEL, TIMEOUT

def embed_texts(texts: list[str]) -> list[list[float]]:
    resp = requests.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={"model": EMBEDDING_MODEL, "input": texts},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    data = resp.json()
    # Handle list vs single input response formats
    return data.get("embeddings") or [data["embedding"]]

def generate(prompt: str, temperature: float = 0.2, max_tokens: int = 1024) -> str:
    resp = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": GENERATION_MODEL,
            "prompt": prompt,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        },
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json().get("response", "")