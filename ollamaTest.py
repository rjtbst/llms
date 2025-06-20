import requests

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3",
    "prompt": "What are the applications of generative AI?",
    "stream": False
})
# Print full response for debugging
print("Raw response:", response.text)

