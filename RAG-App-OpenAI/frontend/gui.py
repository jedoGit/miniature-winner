import streamlit as st
import requests

st.title("RAG Q&A App")

uploaded_file = st.file_uploader("Upload a document", type=["md", "txt"])
tags = st.text_input("Optional tags (comma-separated)")

if uploaded_file:
    res = requests.post(
        "http://localhost:8000/upload",
        files={"file": (uploaded_file.name, uploaded_file.getvalue())},
        data={"tags": tags}
    )
    st.success(f"Uploaded: {uploaded_file.name} with tags: {tags}")

question = st.text_input("Ask a question:")
filter_tag = st.text_input("Filter by tag (optional)")

if st.button("Submit") and question:
    filters = {"tags": filter_tag} if filter_tag else {}
    response = requests.post("http://localhost:8000/ask", json={"question": question, "filters": filters})
    st.write("### Answer:")
    st.write(response.json()["answer"])