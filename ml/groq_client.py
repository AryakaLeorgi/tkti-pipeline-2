import requests
import os

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def groq_chat(prompt: str, model="llama3-8b-8192"):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(GROQ_API_URL, json=body, headers=headers)

    if response.status_code != 200:
        print("[ERROR] Groq response:", response.text)
        response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]
