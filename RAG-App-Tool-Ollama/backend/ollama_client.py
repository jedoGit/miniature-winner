import requests
import logging
from .config import OLLAMA_BASE_URL, GENERATION_MODEL, EMBEDDING_MODEL, TIMEOUT

# Get a logger instance
logger = logging.getLogger(__name__)

# Configure basic logging to console (optional, Uvicorn usually handles this)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def embed_texts(texts: list[str]) -> list[list[float]]:
    resp = requests.post(
        f"{OLLAMA_BASE_URL}/api/embed",
        json={"model": EMBEDDING_MODEL, "input": texts},
        timeout=TIMEOUT,
    )

    # logger.info(f"Embedded Text: {resp.json()}")

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
            "stream": False,
        },
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json().get("response", "")