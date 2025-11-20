from groq_client import groq_chat

prompt = """
Jenkins pipeline mendeteksi anomali.
Berikan kemungkinan penyebab dan contoh perbaikan kode.
"""

print(groq_chat(prompt))
