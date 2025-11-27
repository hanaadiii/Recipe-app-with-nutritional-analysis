import sqlite3
from typing import Optional, List, Dict

DB_PATH = "recipes.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        api_key TEXT UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY(owner_id) REFERENCES users(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        amount REAL NOT NULL,
        unit TEXT,
        calories REAL DEFAULT 0,
        proteins REAL DEFAULT 0,
        fats REAL DEFAULT 0,
        carbs REAL DEFAULT 0,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        performed_by INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        total_calories REAL,
        total_proteins REAL,
        total_fats REAL,
        total_carbs REAL,
        detail_json TEXT,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id),
        FOREIGN KEY(performed_by) REFERENCES users(id)
    );
    """)

    conn.commit()
    conn.close()

def save_analysis(recipe_id: Optional[int], performed_by: Optional[int],
                  totals: Dict[str, float], detail_json: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO analyses (recipe_id, performed_by, total_calories, total_proteins, total_fats, total_carbs, detail_json)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        recipe_id,
        performed_by,
        totals.get("calories", 0.0),
        totals.get("proteins", 0.0),
        totals.get("fats", 0.0),
        totals.get("carbs", 0.0),
        detail_json
    ))
    conn.commit()
    idx = cur.lastrowid
    conn.close()
    return idx

def get_analyses(limit: int = 50) -> List[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM analyses ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    result = [dict(r) for r in rows]
    conn.close()
    return result

