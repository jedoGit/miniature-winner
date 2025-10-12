from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

db = None

def store_chunks(chunks):
    global db
    embeddings = OllamaEmbeddings(model="nomic-embed-text:v1.5")
    db = FAISS.from_documents(chunks, embeddings)

def retrieve_chunks(query):
    if db is None:
        return "No documents loaded."
    return "\n".join([doc.page_content for doc in db.similarity_search(query, k=4)])