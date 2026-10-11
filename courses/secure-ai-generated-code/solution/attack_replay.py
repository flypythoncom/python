"""Replay a scenario's attacks against notes_app (provided harness).

``python attack_replay.py <scenario-dir>`` loads ``seed.json`` and
``attacks.json``, runs each attack against the functions in ``notes_app``,
prints ``blocked=X/Y`` with one line per attack, and exits 0 only when every
attack was blocked. An attack counts as blocked when the function refuses it
with ``SecurityError`` or returns nothing it should not; an unexpected crash
is not a defense. This file is the same in starter/ and solution/ — do not
edit it.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import pickle
import sqlite3
import sys
import tempfile
from pathlib import Path

import notes_app

AUDIT_KEY = b"audit-only-key-0123456789abcdefghijklmnop"
ATTACKER_KEY = b"attacker-chosen-key-not-the-real-one"


class _Marker:
    """Pickle gadget: unpickling it creates a directory at *path*."""

    def __init__(self, path: str) -> None:
        self.path = path

    def __reduce__(self):
        return (os.mkdir, (self.path,))


def _sql(conn, owned, attack, directory):
    rows = notes_app.find_notes(conn, attack["owner"], attack["query"])
    leaked = sorted({row["id"] for row in rows} - owned.get(attack["owner"], set()))
    if leaked:
        return False, f"leaked other owners' note ids {leaked}"
    return True, "no other owner's notes returned"


def _path(conn, owned, attack, directory):
    name = attack["name"].replace("{scenario}", str(directory))
    notes_app.read_attachment(directory / "attachments", name)
    return False, "a file outside attachments/ was served"


def _secret_key(conn, owned, attack, directory):
    notes_app.load_secret_key(attack["env"])
    return False, "the service started without a strong secret key"


def _fast_hash(conn, owned, attack, directory):
    password = attack["password"].encode("utf-8")
    stored = notes_app.hash_password(attack["password"])
    cheap = {getattr(hashlib, name)(password).hexdigest() for name in ("md5", "sha1", "sha256")}
    if stored in cheap:
        return False, "the stored hash is one fast unsalted digest"
    if not notes_app.verify_password(attack["password"], stored):
        return False, "the stored hash does not verify"
    if notes_app.verify_password(attack["password"], hashlib.md5(password).hexdigest()):
        return False, "a leaked MD5 hash still logs in"
    return True, "salted slow hash; legacy MD5 refused"


def _forged_session(conn, owned, attack, directory):
    forged = notes_app.dump_session(attack["claims"], ATTACKER_KEY)
    notes_app.load_session(forged, AUDIT_KEY)
    return False, "a session signed with another key was accepted"


def _pickle_session(conn, owned, attack, directory):
    with tempfile.TemporaryDirectory() as tmp:
        marker = os.path.join(tmp, "executed")
        token = base64.b64encode(pickle.dumps(_Marker(marker))).decode("ascii")
        refused = None
        try:
            notes_app.load_session(token, AUDIT_KEY)
        except notes_app.SecurityError as error:
            refused = error
        if os.path.exists(marker):
            return False, "an attacker-supplied pickle executed code"
        if refused is None:
            return False, "an attacker-supplied pickle was accepted"
        return True, f"refused: {refused}"


CHECKS = {
    "sql": _sql,
    "path": _path,
    "secret-key": _secret_key,
    "fast-hash": _fast_hash,
    "forged-session": _forged_session,
    "pickle-session": _pickle_session,
}


def audit(scenario_dir: str | Path) -> dict:
    """Replay every attack in ``attacks.json`` and report which were blocked."""
    directory = Path(scenario_dir).resolve()
    seed = json.loads((directory / "seed.json").read_text(encoding="utf-8"))
    attacks = json.loads((directory / "attacks.json").read_text(encoding="utf-8"))
    conn = sqlite3.connect(":memory:")
    notes_app.init_db(conn, seed["notes"])
    owned: dict[str, set[int]] = {}
    for note_id, note in enumerate(seed["notes"], start=1):
        owned.setdefault(note["owner"], set()).add(note_id)
    results = []
    for attack in attacks:
        check = CHECKS[attack["kind"]]
        try:
            blocked, detail = check(conn, owned, attack, directory)
        except notes_app.SecurityError as error:
            blocked, detail = True, f"refused: {error}"
        except Exception as error:
            blocked, detail = False, f"crashed: {type(error).__name__}: {error}"
        results.append({"id": attack["id"], "kind": attack["kind"], "blocked": blocked, "detail": detail})
    conn.close()
    return {
        "total": len(results),
        "blocked": sum(result["blocked"] for result in results),
        "results": results,
    }


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        print("usage: python attack_replay.py <scenario-dir>", file=sys.stderr)
        return 2
    report = audit(arguments[0])
    print(f"blocked={report['blocked']}/{report['total']}")
    for result in report["results"]:
        state = "blocked" if result["blocked"] else "OPEN"
        print(f"  [{state}] {result['id']} ({result['kind']}): {result['detail']}")
    return 0 if report["blocked"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
