import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "gemini:4b"

def generate_answer(question, context):
    prompt = f"Answer the question based on context:\n\n{context}\n\nQuestion: {question}"
    response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt})
    return response.json().get("response", "")