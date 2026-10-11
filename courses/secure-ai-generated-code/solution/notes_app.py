"""A small notes service (reference solution).

Search, attachments, configuration, passwords, and sessions — five places
where AI-written web code commonly trusts input it should not. Every
function here treats its caller's input as attacker-controlled.
``attack_replay.py`` replays a scenario's attacks against these functions.
../TASK.md defines the contract.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
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
        "SELECT id, title, body FROM notes"
        " WHERE owner = ? AND instr(lower(title), lower(?)) > 0 ORDER BY id",
        (owner, query),
    ).fetchall()
    return [{"id": row[0], "title": row[1], "body": row[2]} for row in rows]


def read_attachment(base_dir: str | Path, name: str) -> bytes:
    """Return the bytes of attachment *name*, which must live inside *base_dir*."""
    if not name or Path(name).is_absolute():
        raise SecurityError(f"attachment name must be a relative path: {name!r}")
    base = Path(base_dir).resolve()
    target = (base / name).resolve()
    if not target.is_relative_to(base):
        raise SecurityError(f"attachment escapes the attachments directory: {name!r}")
    if not target.is_file():
        raise FileNotFoundError(name)
    return target.read_bytes()


def load_secret_key(env: dict | None = None) -> bytes:
    """Return the session signing key from the environment; never a default."""
    source = os.environ if env is None else env
    value = source.get(KEY_ENV, "")
    if len(value) < MIN_KEY_LENGTH:
        raise SecurityError(f"{KEY_ENV} must be set to at least {MIN_KEY_LENGTH} characters")
    return value.encode("utf-8")


def hash_password(password: str, *, salt: bytes | None = None, iterations: int = PBKDF2_ITERATIONS) -> str:
    """Return a salted PBKDF2-SHA256 hash as ``scheme$iterations$salt$digest``."""
    salt = secrets.token_bytes(16) if salt is None else salt
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"{HASH_SCHEME}${iterations}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Check *password* against a hash from ``hash_password``; refuse anything else."""
    parts = stored.split("$")
    if len(parts) != 4 or parts[0] != HASH_SCHEME:
        return False
    try:
        iterations = int(parts[1])
        salt = bytes.fromhex(parts[2])
    except ValueError:
        return False
    if iterations < MIN_ITERATIONS:
        return False
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(candidate.hex(), parts[3])


def _b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64decode(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def dump_session(data: dict, key: bytes) -> str:
    """Serialize *data* as signed JSON: ``base64url(json).hmac_sha256_hex``."""
    payload = _b64encode(json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    signature = hmac.new(key, payload.encode("ascii"), hashlib.sha256).hexdigest()
    return f"{payload}.{signature}"


def load_session(token: str, key: bytes) -> dict:
    """Verify the signature first, then decode the JSON payload."""
    payload, dot, signature = token.rpartition(".")
    if not dot or not payload or not token.isascii():
        raise SecurityError("session token is malformed")
    expected = hmac.new(key, payload.encode("ascii", "replace"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise SecurityError("session signature does not match")
    try:
        data = json.loads(_b64decode(payload))
    except ValueError:
        raise SecurityError("session payload is not valid JSON") from None
    if not isinstance(data, dict):
        raise SecurityError("session payload must be an object")
    return data
