import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("chatbot.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL,
            modelo TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def salvar_interacao(pergunta: str, resposta: str, modelo: str = "open_llama_3b"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO historico (pergunta, resposta, modelo) VALUES (?, ?, ?)",
        (pergunta, resposta, modelo)
    )
    conn.commit()
    conn.close()

def getHistorico(limite: int = 10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, pergunta, resposta, modelo, timestamp FROM historico ORDER BY timestamp DESC LIMIT ?",
        (limite,)
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados

if __name__ == "__main__":
    init_db()
