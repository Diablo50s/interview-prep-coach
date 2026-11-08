import sqlite3
import json
import datetime

DB_NAME = "sessions.db"


def _connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                difficulty TEXT,
                conversation TEXT,
                score INTEGER
            )
        """)


def save_session(difficulty, messages, score):
    with _connect() as conn:
        conn.execute("""
            INSERT INTO sessions (date, difficulty, conversation, score)
            VALUES (?, ?, ?, ?)
        """, (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            difficulty,
            json.dumps(messages),
            score,
        ))


def get_past_sessions(limit=10):
    with _connect() as conn:
        return conn.execute(
            "SELECT id, date, difficulty, score FROM sessions ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()


def get_session_conversation(session_id):
    with _connect() as conn:
        result = conn.execute(
            "SELECT conversation FROM sessions WHERE id=?", (session_id,)
        ).fetchone()
    if result:
        return json.loads(result[0])
    return []