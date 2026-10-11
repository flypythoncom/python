"""Contract tests for the notes service security fixes."""

from __future__ import annotations

import base64
import contextlib
import hashlib
import io
import os
import pickle
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path

import attack_replay
import notes_app

COURSE_ROOT = Path(__file__).resolve().parent.parent
SCENARIO_ROOT = COURSE_ROOT / "scenario"
STRONG_KEY = "k" * 32


class _Marker:
    def __init__(self, path: str) -> None:
        self.path = path

    def __reduce__(self):
        return (os.mkdir, (self.path,))


def notes_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    notes_app.init_db(conn, [
        {"owner": "alice", "title": "Sprint plan", "body": "a"},
        {"owner": "alice", "title": "100% done list", "body": "b"},
        {"owner": "bob", "title": "Salary review", "body": "secret"},
    ])
    return conn


class FindNotesTest(unittest.TestCase):
    def test_search_is_case_insensitive_and_owner_scoped(self) -> None:
        conn = notes_db()
        self.assertEqual([note["id"] for note in notes_app.find_notes(conn, "alice", "SPRINT")], [1])
        self.assertEqual(notes_app.find_notes(conn, "alice", "salary"), [])

    def test_search_injection_cannot_cross_owners(self) -> None:
        conn = notes_db()
        for query in ("%' OR owner != '", "' UNION SELECT id, title, body FROM notes --", "x' OR 1=1 --"):
            with self.subTest(query=query):
                ids = {note["id"] for note in notes_app.find_notes(conn, "alice", query)}
                self.assertNotIn(3, ids)
        self.assertEqual(notes_app.find_notes(conn, "alice' OR '1'='1", ""), [])

    def test_search_wildcards_are_literal(self) -> None:
        conn = notes_db()
        self.assertEqual([note["id"] for note in notes_app.find_notes(conn, "alice", "%")], [2])
        self.assertEqual(notes_app.find_notes(conn, "alice", "_print"), [])


class ReadAttachmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="attachments-"))
        self.addCleanup(shutil.rmtree, self.root, True)
        self.base = self.root / "attachments"
        (self.base / "docs").mkdir(parents=True)
        (self.base / "docs" / "agenda.txt").write_bytes(b"agenda")
        (self.root / "secrets.txt").write_bytes(b"do not serve")

    def test_attachment_inside_base_is_read(self) -> None:
        self.assertEqual(notes_app.read_attachment(self.base, "docs/agenda.txt"), b"agenda")

    def test_attachment_traversal_is_refused(self) -> None:
        for name in ("../secrets.txt", "docs/../../secrets.txt"):
            with self.subTest(name=name), self.assertRaises(notes_app.SecurityError):
                notes_app.read_attachment(self.base, name)

    def test_absolute_attachment_path_is_refused(self) -> None:
        with self.assertRaises(notes_app.SecurityError):
            notes_app.read_attachment(self.base, str(self.root / "secrets.txt"))

    def test_symlink_escaping_base_is_refused(self) -> None:
        link = self.base / "shortcut.txt"
        try:
            link.symlink_to(self.root / "secrets.txt")
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are not available on this platform")
        with self.assertRaises(notes_app.SecurityError):
            notes_app.read_attachment(self.base, "shortcut.txt")


class SecretKeyTest(unittest.TestCase):
    def test_missing_or_short_secret_key_is_refused(self) -> None:
        for env in ({}, {"NOTES_SECRET_KEY": ""}, {"NOTES_SECRET_KEY": "dev"}, {"NOTES_SECRET_KEY": "k" * 31}):
            with self.subTest(env=env):
                with self.assertRaises(notes_app.SecurityError) as caught:
                    notes_app.load_secret_key(env)
                self.assertIn("NOTES_SECRET_KEY", str(caught.exception))
        self.assertEqual(notes_app.load_secret_key({"NOTES_SECRET_KEY": STRONG_KEY}), STRONG_KEY.encode())


class PasswordTest(unittest.TestCase):
    def test_password_hash_is_salted_pbkdf2(self) -> None:
        first = notes_app.hash_password("hunter2")
        second = notes_app.hash_password("hunter2")
        self.assertNotEqual(first, second)
        scheme, iterations, salt, digest = first.split("$")
        self.assertEqual(scheme, "pbkdf2_sha256")
        self.assertGreaterEqual(int(iterations), 600_000)
        self.assertEqual(len(bytes.fromhex(salt)), 16)
        self.assertEqual(
            digest,
            hashlib.pbkdf2_hmac("sha256", b"hunter2", bytes.fromhex(salt), int(iterations)).hex(),
        )

    def test_verify_accepts_right_and_rejects_wrong_password(self) -> None:
        stored = notes_app.hash_password("hunter2")
        self.assertTrue(notes_app.verify_password("hunter2", stored))
        self.assertFalse(notes_app.verify_password("hunter3", stored))

    def test_verify_rejects_fast_and_weak_hashes(self) -> None:
        self.assertFalse(notes_app.verify_password("hunter2", hashlib.md5(b"hunter2").hexdigest()))
        weak = notes_app.hash_password("hunter2", salt=b"s" * 16, iterations=1_000)
        self.assertFalse(notes_app.verify_password("hunter2", weak))
        self.assertFalse(notes_app.verify_password("hunter2", "not-a-hash"))


class SessionTest(unittest.TestCase):
    key = STRONG_KEY.encode()

    def test_session_round_trip(self) -> None:
        token = notes_app.dump_session({"user": "alice", "role": "member"}, self.key)
        self.assertEqual(notes_app.load_session(token, self.key), {"user": "alice", "role": "member"})

    def test_tampered_or_foreign_session_is_refused(self) -> None:
        token = notes_app.dump_session({"user": "alice", "role": "member"}, self.key)
        forged = notes_app.dump_session({"user": "alice", "role": "admin"}, b"another-key" * 4)
        flipped = ("A" if token[0] != "A" else "B") + token[1:]
        non_ascii = token.rpartition(".")[0] + ".é" + token.rpartition(".")[2][1:]
        for bad in (forged, flipped, non_ascii, "", "no-signature-here"):
            with self.subTest(token=bad[:16]), self.assertRaises(notes_app.SecurityError):
                notes_app.load_session(bad, self.key)

    def test_pickle_payload_is_never_executed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            marker = os.path.join(tmp, "executed")
            token = base64.b64encode(pickle.dumps(_Marker(marker))).decode("ascii")
            with self.assertRaises(notes_app.SecurityError):
                notes_app.load_session(token, self.key)
            self.assertFalse(os.path.exists(marker), "load_session ran attacker-supplied code")


class AttackReplayTest(unittest.TestCase):
    def run_replay(self, argv: list[str]) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            code = attack_replay.main(argv)
        return code, output.getvalue()

    def test_replay_blocks_every_team_notes_attack(self) -> None:
        code, output = self.run_replay([str(SCENARIO_ROOT / "team-notes")])
        self.assertIn("blocked=9/9", output)
        self.assertEqual(code, 0)

    def test_replay_usage_error(self) -> None:
        self.assertEqual(self.run_replay([])[0], 2)


if __name__ == "__main__":
    unittest.main()
