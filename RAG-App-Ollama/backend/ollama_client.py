import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "gemma3:4b"

def generate_answer(question, context):
    prompt = f"Answer the question based on context:\n\n{context}\n\nQuestion: {question}"
    response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt})
    print(response)
    return response.json().get("response", "")