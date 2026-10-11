# Task contract: close five security flaws in a notes service

Change only `starter/notes_app.py`. Standard library only. Never modify
`tests/`, `solution/`, `scenario/`, or `attack_replay.py` (the provided
harness, identical in `starter/` and `solution/`). `init_db` is provided and
already correct. Every argument below is attacker-controlled unless it says
otherwise. Refusals raise `SecurityError`.

- `find_notes(conn, owner, query) -> list[dict]`:
  - Return `{"id", "title", "body"}` for *owner*'s notes whose title
    contains *query*, case-insensitively, ordered by id.
  - *owner* and *query* reach SQLite only as bound parameters (`?`), never
    through string formatting. No input can return another owner's notes.
  - *query* is a literal substring: `%` and `_` match only themselves.
- `read_attachment(base_dir, name) -> bytes`:
  - *base_dir* is trusted; *name* is not. Refuse an empty or absolute
    *name*, and refuse any *name* whose resolved path (after `..` and
    symlinks) is not inside the resolved *base_dir*.
  - A refused name never reads a file. A name inside *base_dir* that does
    not exist raises `FileNotFoundError`.
- `load_secret_key(env=None) -> bytes`:
  - Read `NOTES_SECRET_KEY` from *env* (default `os.environ`). Missing or
    shorter than 32 characters raises `SecurityError` naming
    `NOTES_SECRET_KEY`. There is no default key.
- `hash_password(password, *, salt=None, iterations=600_000) -> str`:
  - Return `pbkdf2_sha256$<iterations>$<salt hex>$<digest hex>` using
    `hashlib.pbkdf2_hmac("sha256", …)` and a fresh 16-byte salt from
    `secrets` when *salt* is `None`. Hashing the same password twice gives
    different strings. Any *iterations* value is accepted here; the
    minimum is enforced by `verify_password`.
- `verify_password(password, stored) -> bool`:
  - True only for a `pbkdf2_sha256` string with at least 600 000 iterations
    whose digest matches, compared with `hmac.compare_digest`. Any other
    format — including a bare MD5 hex digest — returns False.
- `dump_session(data, key) -> str` / `load_session(token, key) -> dict`:
  - A token is the base64url-encoded JSON, a literal `.`, then the hex
    HMAC-SHA256 of the base64url part under *key*; padding may be
    stripped. Never use `pickle`.
  - `load_session` checks the signature with `hmac.compare_digest`
    **before** decoding anything. A malformed token, a wrong signature, a
    token signed with another key, a token with non-ASCII characters, a
    payload that is not JSON, or JSON that is not an object raises
    `SecurityError` — never another exception type.

`python starter/attack_replay.py <scenario-dir>` replays the scenario's
`attacks.json` and prints `blocked=X/Y`; it exits 0 only when every attack
is blocked.

Running the suite against the shipped starter deliberately unpickles a
harmless gadget that creates a directory inside a temporary folder — that
is the proof the starter executes attacker-supplied data.

Done means `python verify.py starter` exits 0 with all sixteen tests
passing (fifteen where the platform cannot create symlinks and the symlink
test is skipped).
