import sqlite3
from datetime import datetime

DB_PATH = "data/meetings.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            transcript TEXT,
            summary TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_meeting(title, transcript, summary):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO meetings (title, transcript, summary, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        title,
        transcript,
        summary,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def fetch_previous_summaries(limit=5):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT summary FROM meetings
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]

def init_auth_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

