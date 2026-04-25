# Chatbot with AI and Python Backend

API developed in FastAPI that integrates with the Llama 3 model (Groq) to answer questions intelligently. Includes SQLite database for conversation history.

## Technologies
- FastAPI - Backend
- Groq API (Llama 3 70B) - AI
- SQLite - Database
- HTML/CSS/JS - Frontend

## How to run locally

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Configure API key
Create a `.env` file with:
```
GROQ_API_KEY=your_api_key_here
```

3. Start the server
```bash
uvicorn main:app --reload
```

Access http://localhost:8000

## Project structure
```
chatbot/
├── main.py              # FastAPI backend
├── database.py          # SQLite
├── templates/
│   └── index.html       # Frontend
├── .env                 # API key (do not version)
├── requirements.txt     # Dependencies
└── README.md
```

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Chat HTML page |
| POST | /chat | Send question |
| GET | /historico | Retrieve history |