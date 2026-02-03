import hashlib
from backend.database import get_connection


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users VALUES (NULL, ?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    user = cur.fetchone()
    conn.close()
    return user is not None
