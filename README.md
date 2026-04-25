# Chatbot com IA e Backend em Python

API desenvolvida em FastAPI que integra com o modelo Llama 3 (Groq) para responder perguntas de forma inteligente. Inclui banco de dados SQLite para histórico de conversas.

## Tecnologias
- FastAPI - Backend
- Groq API (Llama 3 70B) - IA
- SQLite - Banco de dados
- HTML/CSS/JS - Frontend

## Como executar localmente

1. Instalar dependências
```bash
pip install -r requirements.txt
```

2. Configurar a API key
Criar um arquivo `.env` com:
```
GROQ_API_KEY=sua_api_key_aqui
```

3. Iniciar o servidor
```bash
uvicorn main:app --reload
```

Acesse http://localhost:8000

## Estrutura do projeto
```
chatbot/
├── main.py              # FastAPI backend
├── database.py          # SQLite
├── templates/
│   └── index.html       # Frontend
├── .env                 # API key (não versionar)
├── requirements.txt     # Dependências
└── README.md
```

## Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | / | Página HTML do chat |
| POST | /chat | Enviar pergunta |
| GET | /historico | Recuperar histórico |