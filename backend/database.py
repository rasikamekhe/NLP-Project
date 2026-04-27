import sqlite3
from pathlib import Path
from typing import Dict, List


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "threats.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                input_text TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            INSERT OR IGNORE INTO users (username, password)
            VALUES ('admin', 'admin123')
            """
        )


def create_user(username: str, password: str) -> bool:
    """
    Insert a new user into the users table.
    Returns True if created, False if username already exists.
    """
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def validate_user(username: str, password: str) -> bool:
    with get_conn() as conn:
        result = conn.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    print("User found:", result)
    if result is None:
        print("Password match:", False)
        return False
    stored_password = result["password"]
    print("Password match:", stored_password == password)
    return stored_password == password


def save_prediction(username: str, input_text: str, prediction: str, confidence: float) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO predictions (username, input_text, prediction, confidence)
            VALUES (?, ?, ?, ?)
            """,
            (username, input_text, prediction, confidence),
        )


def get_history(limit: int = 50) -> List[Dict]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, username, input_text, prediction, confidence, created_at
            FROM predictions
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]
