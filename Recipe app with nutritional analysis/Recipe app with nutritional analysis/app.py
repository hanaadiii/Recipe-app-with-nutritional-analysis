import sqlite3
from typing import Iterator

DB_PATH = "recipe_app.db"

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_db() -> Iterator[sqlite3.Connection]:
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()