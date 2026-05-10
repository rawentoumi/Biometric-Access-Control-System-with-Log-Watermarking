# database/db_manager.py
import sqlite3
import numpy as np
import pickle
import hashlib
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crée les tables si elles n'existent pas."""
    conn = get_connection()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            encoding      BLOB    NOT NULL,
            is_authorized INTEGER DEFAULT 1,
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS access_logs (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id          INTEGER,
            user_name        TEXT,
            event_type       TEXT    NOT NULL,
            timestamp        DATETIME DEFAULT CURRENT_TIMESTAMP,
            image_path       TEXT,
            watermark_valid  INTEGER DEFAULT 1,
            image_hash       TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


# ─── Users ─────────────────────────────────────────────────────────────

def add_user(name: str, encoding: np.ndarray) -> int:
    """Enregistre un nouvel utilisateur avec son encodage facial."""
    blob = pickle.dumps(encoding)
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (name, encoding) VALUES (?, ?)",
        (name, blob)
    )
    uid = c.lastrowid
    conn.commit()
    conn.close()
    return uid


def get_all_users() -> list:
    """Retourne tous les utilisateurs avec leurs encodages décodés."""
    conn = get_connection()
    rows = conn.execute("SELECT id, name, encoding, is_authorized FROM users").fetchall()
    conn.close()
    users = []
    for row in rows:
        users.append({
            "id":            row["id"],
            "name":          row["name"],
            "encoding":      pickle.loads(row["encoding"]),
            "is_authorized": bool(row["is_authorized"])
        })
    return users


def get_all_users_info() -> list:
    """Retourne les infos utilisateurs sans encodages (pour affichage)."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, name, is_authorized, created_at FROM users ORDER BY name"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def set_user_authorization(user_id: int, authorized: bool):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET is_authorized = ? WHERE id = ?",
        (int(authorized), user_id)
    )
    conn.commit()
    conn.close()


def delete_user(user_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


# ─── Logs ─────────────────────────────────────────────────────────────────────

def add_log(event_type: str, image_path: str = None,
            user_id: int = None, user_name: str = None,
            image_hash: str = None) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO access_logs
           (user_id, user_name, event_type, image_path, image_hash)
           VALUES (?, ?, ?, ?, ?)""",
        (user_id, user_name, event_type, image_path, image_hash)
    )
    lid = c.lastrowid
    conn.commit()
    conn.close()
    return lid


def update_log_watermark(log_id: int, valid: bool):
    conn = get_connection()
    conn.execute(
        "UPDATE access_logs SET watermark_valid = ? WHERE id = ?",
        (int(valid), log_id)
    )
    conn.commit()
    conn.close()


def get_all_logs(limit: int = 200) -> list:
    conn = get_connection()
    rows = conn.execute(
        """SELECT id, user_id, user_name, event_type, timestamp,
                  image_path, watermark_valid, image_hash
           FROM access_logs
           ORDER BY timestamp DESC LIMIT ?""",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def compute_image_hash(path: str) -> str:
    """Calcule le SHA-256 d'un fichier image."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()