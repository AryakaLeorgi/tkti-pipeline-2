import requests
import os
import json

def groq_chat(prompt):
    api_key = os.environ.get("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")
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "deepseek-r1",   # GRATIS di Groq
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    
    return response.json()["choices"][0]["message"]["content"]
