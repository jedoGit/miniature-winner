from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

CHROMA_PATH = "vectorstore"

def deduplicate_chunks(chunks):
    seen = set()
    unique_chunks = []
    for doc in chunks:
        text = doc.page_content.strip()
        if text not in seen:
            seen.add(text)
            unique_chunks.append(doc)
    return unique_chunks

def update_vectorstore(vectorstore, new_chunks):
    unique_chunks = deduplicate_chunks(new_chunks)
    vectorstore.add_documents(unique_chunks)
    vectorstore.persist()