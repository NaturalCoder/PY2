import requests

def chat_with_ollama(prompt, model="deepseek-r1:14b"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    return response.json()["response"]

# Teste
resposta = chat_with_ollama("Explique quantum computing em 1 parágrafo.")
print(resposta)