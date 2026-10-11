"""A small notes service (starter, insecure).

Search, attachments, configuration, passwords, and sessions — five places
where AI-written web code commonly trusts input it should not. This starter
works on every friendly input and is written the way a quick first draft
often is: SQL built with an f-string, file paths joined as given, a
hard-coded fallback secret, unsalted MD5 passwords, and pickled sessions.
``attack_replay.py`` replays a scenario's attacks against these functions.
../TASK.md defines the contract.
"""

from __future__ import annotations

import base64
import hashlib
import os
import pickle
import sqlite3
from pathlib import Path

KEY_ENV = "NOTES_SECRET_KEY"
MIN_KEY_LENGTH = 32
PBKDF2_ITERATIONS = 600_000
MIN_ITERATIONS = 600_000
HASH_SCHEME = "pbkdf2_sha256"


class SecurityError(ValueError):
    """Input the service refuses to act on."""


def init_db(conn: sqlite3.Connection, notes: list[dict]) -> None:
    """Create the notes table and insert *notes* (owner, title, body)."""
    conn.execute(
        "CREATE TABLE notes (id INTEGER PRIMARY KEY, owner TEXT NOT NULL,"
        " title TEXT NOT NULL, body TEXT NOT NULL)"
    )
    conn.executemany(
        "INSERT INTO notes (owner, title, body) VALUES (?, ?, ?)",
        [(note["owner"], note["title"], note["body"]) for note in notes],
    )
    conn.commit()


def find_notes(conn: sqlite3.Connection, owner: str, query: str) -> list[dict]:
    """Return *owner*'s notes whose title contains *query* (case-insensitive)."""
    rows = conn.execute(
        f"SELECT id, title, body FROM notes WHERE owner = '{owner}'"
        f" AND title LIKE '%{query}%' ORDER BY id"
    ).fetchall()
    return [{"id": row[0], "title": row[1], "body": row[2]} for row in rows]


def read_attachment(base_dir: str | Path, name: str) -> bytes:
    """Return the bytes of attachment *name*, which must live inside *base_dir*."""
    return (Path(base_dir) / name).read_bytes()


def load_secret_key(env: dict | None = None) -> bytes:
    """Return the session signing key from the environment."""
    source = os.environ if env is None else env
    return source.get(KEY_ENV, "dev-secret-change-me").encode("utf-8")


def hash_password(password: str, *, salt: bytes | None = None, iterations: int = PBKDF2_ITERATIONS) -> str:
    """Return a hash of *password* for storage."""
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def verify_password(password: str, stored: str) -> bool:
    """Check *password* against a stored hash."""
    return hashlib.md5(password.encode("utf-8")).hexdigest() == stored


def dump_session(data: dict, key: bytes) -> str:
    """Serialize *data* into a session token."""
    return base64.b64encode(pickle.dumps(data)).decode("ascii")


def load_session(token: str, key: bytes) -> dict:
    """Restore session data from a token."""
    return pickle.loads(base64.b64decode(token))
