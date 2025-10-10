import re
import requests
from bs4 import BeautifulSoup
from readability import Document
from urllib.parse import urlparse
from typing import List, Dict
from .config import TIMEOUT, MAX_WEB_SOURCES

def fetch_url(url: str) -> dict:
    resp = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    html = resp.text
    doc = Document(html)
    content_html = doc.summary(html_partial=True)
    soup = BeautifulSoup(content_html, "html.parser")
    text = soup.get_text("\n").strip()
    title = doc.short_title()
    domain = urlparse(url).netloc
    return {"url": url, "title": title, "domain": domain, "text": sanitize_text(text)}

def sanitize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def fetch_urls(urls: List[str], limit: int = MAX_WEB_SOURCES) -> List[Dict]:
    results = []
    for url in urls[:limit]:
        try:
            results.append(fetch_url(url))
        except Exception as e:
            results.append({"url": url, "error": str(e)})
    return results