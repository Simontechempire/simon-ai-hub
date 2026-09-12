import sqlite3
from pathlib import Path


DATABASE_FILE = Path(__file__).resolve().parent / "simon_hub.db"


def get_connection():
    return sqlite3.connect(DATABASE_FILE)


def init_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()


def add_user(user_id: int, username: str | None, first_name: str | None):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO users
            (id, username, first_name)
            VALUES (?, ?, ?)
            """,
            (user_id, username, first_name),
        )

        connection.commit()


def get_user_count() -> int:
    with get_connection() as connection:
        result = connection.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()

        return result[0]
