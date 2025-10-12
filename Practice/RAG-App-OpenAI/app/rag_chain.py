import os
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from config import OPENAI_API_KEY

# Set your OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def build_qa_chain(vectorstore, filters=None):
    retriever = vectorstore.as_retriever(search_kwargs={"filter": filters or {}})
    llm = ChatOpenAI(temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )