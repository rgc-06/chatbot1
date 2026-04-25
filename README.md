# AI Chatbot with FastAPI + Groq

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/)

**Live Demo:** https://chatbot1-3sio.onrender.com/

A modern chat application with conversation memory managed in RAM. Messages are stored on the server side using a global dictionary, with session IDs persisted in the browser's localStorage.

## Features

- **Conversation Memory**: Full context retained for all messages within a session
- **Session Persistence**: `session_id` stored in browser `localStorage` for continuity
- **Reset Capability**: Option to clear chat history at any time
- **Modern UI**: Dark theme with responsive Flexbox layout

## Tech Stack

- **Backend**: FastAPI (Python)
- **AI Model**: Groq API (Llama 3.3 70B)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Storage**: In-memory dictionary (no external database)

## Environment Setup

Create a `.env` file in the project root with:

```
GROQ_API_KEY=your_groq_api_key_here
```

## Running Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open http://localhost:8000 in your browser.

## Deployment to Render (Free Tier)

1. Create a new Web Service on [Render](https://render.com/)
2. Connect your GitHub repository
3. Set these environment variables:
   - `GROQ_API_KEY`: Your Groq API key
4. Set the build command: `pip install -r requirements.txt`
5. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy

**Note**: Memory is volatile! The conversation history resets when the Render instance restarts (which happens periodically on the free tier). This is acceptable for portfolio/demo purposes.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Main HTML page |
| POST | /chat | Send message (expects `{message: "text"}`) |
| GET | /history | Retrieve conversation history for session |
| POST | /reset | Reset conversation for current session |

## Session Management

- Session ID is generated using `crypto.randomUUID()` on first load
- Stored in browser `localStorage` as `chat_session`
- Sent to backend via `X-Session-ID` header
- Conversations are scoped per session ID