import requests
import json
import os
from docx import Document  # <- NEW

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"

def call_llama(messages):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "messages": messages,
        "stream": False
    })

    if response.status_code != 200:
        raise Exception(f"Ollama API Error: {response.status_code} - {response.text}")

    return response.json()['message']['content']

def summarize_cv(cv_text):
    messages = [
        {"role": "user", "content": f"Please summarize the following CV:\n\n{cv_text}"}
    ]
    return call_llama(messages)

def generate_cover_letter(cv_summary, job_description):
    messages = [
        {"role": "system", "content": "You are a master at crafting perfect cover letters from a given CV."},
        {"role": "user", "content": f"Using the following CV summary:\n\n{cv_summary}\n\nAnd this job description:\n\n{job_description}\n\nWrite a personalized cover letter."}
    ]
    return call_llama(messages)

# === Replace .txt reading with .docx reading ===
def read_resume_from_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise Exception(f"Failed to read Word document: {e}")

# Main logic
try:
    resume_path = 'resume.docx'  # Make sure your file is in the same folder
    if not os.path.exists(resume_path):
        raise FileNotFoundError(f"{resume_path} not found.")

    cv_text = read_resume_from_docx(resume_path)

    cv_summary = summarize_cv(cv_text)
    print("\n=== CV Summary ===")
    print(cv_summary)

    job_description = input("\nEnter the job description:\n")

    cover_letter = generate_cover_letter(cv_summary, job_description)
    print("\n=== Generated Cover Letter ===")
    print(cover_letter)

except FileNotFoundError as fnf:
    print(f"Error: {fnf}")
except Exception as e:
    print("Error:", e)
