import os
import uuid
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

# Global memory: dictionary to store conversation history by session
conversations: dict[str, list[dict[str, str]]] = {}


class ChatMessage(BaseModel):
    message: str


def get_session_id(request: Request) -> str:
    """Extract session_id from header or cookie, generate new if not exists."""
    session_id = request.headers.get("X-Session-ID")
    if not session_id:
        session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/chat")
async def chat(request: Request, body: ChatMessage):
    session_id = get_session_id(request)
    
    # Initialize session if not exists
    if session_id not in conversations:
        conversations[session_id] = []
    
    user_message = body.message.strip()
    if not user_message:
        return JSONResponse(content={"error": "Message cannot be empty"}, status_code=400)
    
    # Add user message to history
    conversations[session_id].append({"role": "user", "content": user_message})
    
    if not API_KEY:
        return JSONResponse(content={"error": "Groq API key not configured"}, status_code=500)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Send full conversation history to Groq
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": conversations[session_id],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            assistant_message = data["choices"][0]["message"]["content"].strip()
            
            # Add assistant response to history
            conversations[session_id].append({"role": "assistant", "content": assistant_message})
            
            return {"response": assistant_message}
        else:
            return JSONResponse(content={"error": f"Groq API error: {resp.status_code}"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"Internal error: {str(e)}"}, status_code=500)


@app.get("/history")
async def history(request: Request):
    session_id = get_session_id(request)
    
    # Initialize session if not exists
    if session_id not in conversations:
        conversations[session_id] = []
    
    return {"history": conversations[session_id]}


@app.post("/reset")
async def reset(request: Request):
    """Reset conversation history for a session."""
    session_id = get_session_id(request)
    if session_id in conversations:
        conversations[session_id] = []
    return {"status": "ok"}