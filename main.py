import os
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

app = FastAPI(title="Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pergunta(BaseModel):
    pergunta: str

from database import init_db, salvar_interacao, getHistorico
init_db()

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
async def chat(pergunta: Pergunta):
    msg = pergunta.pergunta.strip()
    if not msg:
        return {"resposta": "Digite uma pergunta."}
    if not API_KEY:
        return {"resposta": "Chave da API Groq não configurada."}

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": msg}],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            dados = resp.json()
            resposta = dados["choices"][0]["message"]["content"].strip()
            salvar_interacao(msg, resposta, "llama3-70b")
            return {"resposta": resposta}
        else:
            return {"resposta": f"Erro API Groq: {resp.status_code} - {resp.text[:200]}"}
    except Exception as e:
        return {"resposta": f"Erro interno: {str(e)}"}
