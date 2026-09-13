#!/usr/bin/env python3
"""Shared claim-receipt production for course verify.py scripts.

Implements the producer side of docs/CLAIM-RECEIPT.md (flypython.com) —
canonical JSON, the implementation-tree hash, and the HMAC-SHA256 signature.
Receipts are only produced when FLYPYTHON_CLAIM_SECRET is set in the
environment; without it every caller keeps its exact old behavior.

Imported from courses/<slug>/verify.py via a repo-root sys.path insert, so a
course folder copied out of the repo still verifies — the import is optional
and receipts simply stay off.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

SECRET_ENV = "FLYPYTHON_CLAIM_SECRET"

# Directory names never hashed into an implementation tree — caches, the
# graded suite, the reference implementation, and VCS/venv noise.
SKIP_DIRS = {"__pycache__", "tests", "solution", ".git", ".venv", "venv", "node_modules"}


def canonical_json(obj) -> bytes:
    """docs/CLAIM-RECEIPT.md §2 — sorted keys, no whitespace, raw UTF-8."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def tree_sha256(root: Path) -> str:
    """docs/CLAIM-RECEIPT.md §3 — sorted (path, content) pairs, NUL-separated."""
    root = Path(root)
    entries: list[tuple[str, bytes]] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if not path.is_file():
            continue
        entries.append((rel.as_posix(), path.read_bytes()))
    entries.sort(key=lambda pair: pair[0])
    h = hashlib.sha256()
    for rel, content in entries:
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(content)
        h.update(b"\0")
    return h.hexdigest()


def solution_sha256(course_dir: Path) -> str | None:
    """Hash the course's solution tree; None when there is none to compare."""
    solution = Path(course_dir) / "solution"
    if not solution.is_dir():
        return None
    return tree_sha256(solution)


def make_receipt(
    course_id: str,
    checkpoint_id: str,
    *,
    passed: bool,
    tests: int,
    duration_ms: int,
    impl_dir: Path,
    solution_hash: str | None,
    secret: str,
) -> dict:
    """One receipt per gated checkpoint — see the spec for field semantics."""
    impl_hash = tree_sha256(impl_dir)
    receipt = {
        "v": 1,
        "course": course_id,
        "checkpoint": checkpoint_id,
        "suite": {
            "passed": bool(passed),
            "tests": int(tests),
            "duration_ms": int(duration_ms),
        },
        "impl_sha256": impl_hash,
        "solution_match": (impl_hash == solution_hash) if solution_hash else False,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "nonce": secrets.token_hex(16),
    }
    receipt["sig"] = hmac.new(
        secret.encode("utf-8"), canonical_json(receipt), hashlib.sha256
    ).hexdigest()
    return receipt


def receipts_enabled() -> str | None:
    """The account secret from the environment, or None to keep old output."""
    secret = __import__("os").environ.get(SECRET_ENV, "").strip()
    return secret or None


def count_tests(suite_output: str) -> int:
    """`unittest` prints 'Ran N tests' to stderr; receipts record N."""
    import re

    match = re.search(r"Ran (\d+) test", suite_output or "")
    return int(match.group(1)) if match else 0
