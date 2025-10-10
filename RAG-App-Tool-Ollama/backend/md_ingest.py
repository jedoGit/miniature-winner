import os
from typing import Tuple, List, Dict
import frontmatter
import markdown2
from bs4 import BeautifulSoup
from .utils import chunk_text

def load_markdown_file(path: str) -> Tuple[str, Dict]:
    post = frontmatter.load(path)
    md_text = post.content
    metadata = post.metadata or {}
    return md_text, metadata

def markdown_to_plain_text(md_text: str) -> str:
    # Convert markdown to HTML, then strip to clean text
    html = markdown2.markdown(md_text)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n")
    # Normalize whitespace
    return " ".join(text.split())

def chunk_markdown(md_text: str) -> Tuple[List[str], List[Dict]]:
    plain = markdown_to_plain_text(md_text)
    chunks = chunk_text(plain)
    # Simple metadata per chunk; could include headings via a richer parser
    metas = [{"source": "markdown", "type": "md"} for _ in chunks]
    return chunks, metas