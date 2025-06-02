from fastapi import FastAPI, Form
import requests

app = FastAPI()

def call_llm(prompt: str):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama2", "prompt": prompt, "stream": False},
            timeout=60 # Added a timeout
        )
        response.raise_for_status() # Will raise an HTTPError for bad responses (4XX or 5XX)
        return response.json()["response"].strip()
    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM: {e}")
        return f"Error communicating with LLM: {e}"
    except KeyError:
        print(f"Error parsing LLM response: {response.text}")
        return "Error: Unexpected response format from LLM."

@app.post("/analyze/")
def analyze_legal(text: str = Form(...)):
    prompts = {
        "summary": f"Summarize this legal document concisely, highlighting the main purpose and key outcomes:\n\n{text}",
        "clauses": f"Extract key clauses from this legal text (e.g., Termination, Confidentiality, Payment Terms, Governing Law). For each clause, provide a brief description of its meaning:\n\n{text}",
        "entities": f"Extract all named entities (e.g., parties involved, company names, locations, dates, monetary amounts) from this legal document. List them clearly:\n\n{text}"
    }
    results = {k: call_llm(p) for k, p in prompts.items()}
    return results