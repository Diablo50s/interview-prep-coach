import sqlite3
import json
import datetime

DB_NAME = "sessions.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            difficulty TEXT,
            conversation TEXT,
            score INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_session(difficulty, messages, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO sessions (date, difficulty, conversation, score)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        difficulty,
        json.dumps(messages),
        score
    ))
    conn.commit()
    conn.close()

def get_past_sessions(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, date, difficulty, score FROM sessions ORDER BY id DESC LIMIT ?", (limit,))
    sessions = c.fetchall()
    conn.close()
    return sessions

def get_session_conversation(session_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT conversation FROM sessions WHERE id=?", (session_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return json.loads(result[0])
    return []