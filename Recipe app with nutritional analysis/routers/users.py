from fastapi import APIRouter, HTTPException, Header
from database.database import get_db
from models.user import UserCreate, UserOut
import sqlite3

API_KEY = "12345"

router = APIRouter(prefix="/users", tags=["Users"])


def check_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API KEY")


@router.post("/register")
def register_user(user: UserCreate, x_api_key: str = Header(None)):
    check_api_key(x_api_key)

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                    (user.username, user.password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")

    return {"message": "User created successfully"}


@router.get("/")
def get_users(x_api_key: str = Header(None)):
    check_api_key(x_api_key)

    conn = get_db()
    cur = conn.cursor()

    rows = cur.execute("SELECT id, username FROM users").fetchall()

    return [UserOut(id=r["id"], username=r["username"]) for r in rows]



