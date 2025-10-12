import streamlit as st
import requests

st.title("Gemma3 4B RAG App")

uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])
if uploaded_file:
    res = requests.post("http://localhost:8000/upload/", files={"file": uploaded_file})
    st.success(res.json()["message"])

query = st.text_input("Ask a question")
if query:
    res = requests.get("http://localhost:8000/query/", params={"q": query})
    st.write("Answer:", res.json()["answer"])