import os
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

st.set_page_config(page_title="RAG Markdown Chatbot", page_icon="📝", layout="wide")
st.title("RAG Chatbot (gemma3:4b + nomic-embed-text:v1.5)")

with st.sidebar:
    st.header("Settings")
    use_web = st.checkbox("Use web context", value=True)
    top_k = st.slider("Top K (vector hits)", 2, 15, 6)
    st.divider()
    st.caption("Backend health")
    try:
        health = requests.get(f"{API_BASE}/health", timeout=10).json()
        st.success(f"Status: {health['status']}")
    except Exception as e:
        st.error(f"Health check failed: {e}")

    st.divider()
    st.header("Ingest Markdown")
    md_file = st.file_uploader("Upload a .md file", type=["md", "markdown"])
    if md_file and st.button("Index Markdown"):
        with st.spinner("Indexing markdown..."):
            files = {"file": (md_file.name, md_file.getvalue(), "text/markdown")}
            resp = requests.post(f"{API_BASE}/ingest_markdown", files=files).json()
        st.success(f"Indexed {resp['chunks_indexed']} chunk(s) from {resp['source']}")

    st.divider()
    st.header("Ingest URLs")
    urls_text = st.text_area("Enter URLs (one per line)")
    if st.button("Fetch & Index URLs"):
        urls = [u.strip() for u in urls_text.splitlines() if u.strip()]
        if urls:
            with st.spinner("Fetching and indexing..."):
                resp = requests.post(f"{API_BASE}/ingest_urls", json={"urls": urls}).json()
            st.success(f"Ingested from {resp['count']} URL(s)")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Web URLs for ephemeral context (without indexing)
web_ephemeral = st.text_input("Optional web URLs (comma-separated) used only for this answer")

query = st.chat_input("Ask about your markdown or the web…")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    urls_param = [u.strip() for u in web_ephemeral.split(",") if u.strip()] if web_ephemeral else None

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            resp = requests.post(f"{API_BASE}/chat", json={
                "query": query,
                "use_web": use_web,
                "web_urls": urls_param,
                "top_k": top_k,
            }).json()
        st.markdown(resp["answer"])
        # if resp.get("sources"):
        #     st.caption("Sources")
        #     for s in resp["sources"]:
        #         st.write(f"- [{s['index']}] {s['label']}")
        st.session_state.messages.append({"role": "assistant", "content": resp["answer"]})