from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def load_and_chunk(path, tags=None):
    loader = TextLoader(path)
    raw_docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(raw_docs)

    filename = os.path.basename(path)
    for chunk in chunks:
        chunk.metadata["source"] = filename
        if tags:
            chunk.metadata["tags"] = tags
    return chunks