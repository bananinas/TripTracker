import db
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def add_user(username, password):
    password_hash = generate_password_hash(password)
    try:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            [username, password_hash]
        )
        return True
    except sqlite3.IntegrityError:
        return False

def get_password_hash(username):
    rows = db.query("SELECT password_hash FROM users WHERE username = ?", [username])
    row = rows[0] if rows else None
    return row["password_hash"] if row else None

def verify_login(username, password_plain):
    ph = get_password_hash(username)
    return bool(ph and check_password_hash(ph, password_plain))

