import sys
from groq_client import groq_chat

template = """
Kamu adalah AI untuk memperbaiki error CI/CD.

INCOMING ERROR:
{ERROR}

Tolong berikan:
1. Analisa penyebab error
2. Perbaikan yang diperlukan
3. Patch code / Jenkinsfile yang direkomendasikan
"""

if __name__ == "__main__":
    err = sys.argv[1] if len(sys.argv) > 1 else "Unknown Error"
    prompt = template.replace("{ERROR}", err)
    print(groq_chat(prompt))
