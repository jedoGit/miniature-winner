import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
GENERATION_MODEL = os.getenv("GENERATION_MODEL", "gemma3:4b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text:v1.5")

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", os.path.join("data", "chroma"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
TOP_K = int(os.getenv("TOP_K", "6"))
MAX_WEB_SOURCES = int(os.getenv("MAX_WEB_SOURCES", "3"))
TIMEOUT = int(os.getenv("TIMEOUT", "30"))