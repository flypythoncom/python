#!/usr/bin/env python3
"""Verify every published course folder against the course contract.

Checks per course directory: COURSE.md and COURSE_cn.md exist, every English
lesson has a paired ``*_cn.md`` file (and vice versa), and the course's own
``verify.py`` reproduces the starter failure and passes the solution.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON_NAME = re.compile(r"^L\d{2,}\.md$")

sys.path.insert(0, str(ROOT / "tools"))
import claim_receipt  # noqa: E402


def discover_courses(root: Path) -> list[Path]:
    courses_dir = root / "courses"
    if not courses_dir.exists():
        return []
    return sorted(path for path in courses_dir.iterdir() if path.is_dir())


def check_bilingual_contract(course: Path) -> list[str]:
    problems: list[str] = []
    name = course.name

    for required in ("COURSE.md", "COURSE_cn.md", "TASK.md", "TASK_cn.md", "REVIEW.md", "verify.py"):
        if not (course / required).exists():
            problems.append(f"{name}: missing {required}")

    lessons_dir = course / "lessons"
    if not lessons_dir.is_dir():
        problems.append(f"{name}: missing lessons/ directory")
        return problems

    english = {path.name.removesuffix(".md") for path in lessons_dir.iterdir() if LESSON_NAME.fullmatch(path.name)}
    chinese_stems = {
        path.name.removesuffix("_cn.md")
        for path in lessons_dir.iterdir()
        if path.name.endswith("_cn.md")
    }

    missing_pairs = sorted(english - chinese_stems)
    orphan_chinese = sorted(chinese_stems - english)
    if missing_pairs:
        problems.append(f"{name}: lessons without _cn.md pair: {', '.join(missing_pairs)}")
    if orphan_chinese:
        problems.append(f"{name}: _cn.md lessons without English pair: {', '.join(orphan_chinese)}")
    if not english:
        problems.append(f"{name}: lessons/ contains no L*.md lessons")
    return problems


def run_course_verifier(course: Path) -> list[str]:
    name = course.name
    verify = course / "verify.py"
    if not verify.exists():
        return []  # Already reported by the contract check.
    commands = (
        [sys.executable, str(verify), "starter", "--expect-failure"],
        [sys.executable, str(verify), "solution"],
    )
    problems: list[str] = []
    for command in commands:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        if result.returncode != 0:
            problems.append(
                f"{name}: verification failed: {' '.join(command[2:])}"
                f"\n{(result.stdout or '') + (result.stderr or '')}".rstrip()
            )
    problems.extend(check_progress_contract(course))
    problems.extend(check_receipt_contract(course))
    return problems


def check_progress_contract(course: Path) -> list[str]:
    """FP-415: the progress subcommand must be deterministic and well-shaped.

    Runs ``verify.py progress --json`` twice and requires identical output,
    a valid document, five checkpoints (l01..l05), and well-formed claim
    codes wherever one is printed.
    """

    verify = course / "verify.py"
    if not verify.exists():
        return []
    name = course.name
    runs: list[str] = []
    for _ in range(2):
        result = subprocess.run(
            [sys.executable, str(verify), "progress", "--json"],
            check=False, capture_output=True, text=True,
        )
        if result.returncode != 0:
            return [f"{name}: progress failed\n{(result.stdout or '') + (result.stderr or '')}".rstrip()]
        runs.append(result.stdout)
    if runs[0] != runs[1]:
        return [f"{name}: progress output is not deterministic between runs"]
    try:
        document = json.loads(runs[0])
    except ValueError:
        return [f"{name}: progress --json did not emit valid JSON"]

    problems: list[str] = []
    for key in ("course", "starter_suite_passed", "solution_suite_passed", "checkpoints"):
        if key not in document:
            problems.append(f"{name}: progress document missing {key!r}")
    checkpoints = document.get("checkpoints")
    if not isinstance(checkpoints, list) or len(checkpoints) != 5:
        problems.append(f"{name}: progress must list exactly five checkpoints")
        return problems
    expected_ids = [f"l0{index}" for index in range(1, 6)]
    if [item.get("id") for item in checkpoints] != expected_ids:
        problems.append(f"{name}: checkpoint ids must be {expected_ids}")
    for item in checkpoints:
        code = item.get("claim_code")
        if code is not None and not re.fullmatch(r"[A-Z2-7]{8}", str(code)):
            problems.append(f"{name}: malformed claim code for {item.get('id')}: {code!r}")
    return problems


def check_receipt_contract(course: Path) -> list[str]:
    """FP-704: under FLYPYTHON_CLAIM_SECRET, progress --json must attach one
    spec-shaped receipt per gated checkpoint with a verifiable HMAC."""
    verify = course / "verify.py"
    if not verify.exists():
        return []
    name = course.name
    secret = "contract-test-secret"
    env = dict(os.environ, FLYPYTHON_CLAIM_SECRET=secret)
    result = subprocess.run(
        [sys.executable, str(verify), "progress", "--json"],
        check=False, capture_output=True, text=True, env=env,
    )
    if result.returncode != 0:
        return [f"{name}: progress with {claim_receipt.SECRET_ENV} failed\n"
                f"{(result.stdout or '') + (result.stderr or '')}".rstrip()]
    try:
        document = json.loads(result.stdout)
    except ValueError:
        return [f"{name}: progress --json with secret did not emit valid JSON"]

    receipts = document.get("receipts")
    if not isinstance(receipts, list) or not receipts:
        return [f"{name}: progress --json emitted no receipts under {claim_receipt.SECRET_ENV}"]

    gated = {item["id"] for item in document.get("checkpoints", [])
             if item.get("kind") == "objective"}
    problems: list[str] = []
    if {receipt.get("checkpoint") for receipt in receipts} != gated:
        problems.append(f"{name}: receipts must cover exactly the gated checkpoints")
    for receipt in receipts:
        sig = receipt.pop("sig", None)
        expected = hmac.new(
            secret.encode(), claim_receipt.canonical_json(receipt), hashlib.sha256
        ).hexdigest()
        if not isinstance(sig, str) or not hmac.compare_digest(sig, expected):
            problems.append(f"{name}: receipt for {receipt.get('checkpoint')} has a bad signature")
        for field in ("v", "course", "checkpoint", "suite", "impl_sha256",
                      "solution_match", "created_at", "nonce"):
            if field not in receipt:
                problems.append(f"{name}: receipt for {receipt.get('checkpoint')} missing {field!r}")
        suite = receipt.get("suite")
        if not isinstance(suite, dict) or not all(
            key in suite for key in ("passed", "tests", "duration_ms")
        ):
            problems.append(f"{name}: receipt for {receipt.get('checkpoint')} has a malformed suite block")
    return problems


# ── Default command contract (FP-820) ──────────────────────────────────────
# Bare ``python verify.py`` is the learner's command: it runs the same engine
# as ``progress``, prints English-first output with the Chinese lines after,
# and exits 1 while objective gates are open (a shipped starter intentionally
# fails). The published ``progress --json`` / ``--receipt-out`` formats must
# stay byte-compatible with 0.0.7 — check_progress/check_receipt above own
# those; this check owns the new surface.


def check_default_command(course: Path) -> list[str]:
    verify = course / "verify.py"
    if not verify.exists():
        return []
    name = course.name
    problems: list[str] = []
    result = subprocess.run(
        [sys.executable, str(verify)],
        check=False, capture_output=True, text=True,
    )
    if result.returncode != 1:
        problems.append(
            f"{name}: default command exited {result.returncode}"
            " (expected 1: the shipped starter intentionally fails)")
    lines = result.stdout.splitlines()
    if not any(line.startswith("Suites: starter ") for line in lines):
        problems.append(f"{name}: default command missing the Suites line")
    if not any("[open]" in line and "l03" in line for line in lines):
        problems.append(f"{name}: default command does not show l03 as open")
    if not any("[attest" in line for line in lines):
        problems.append(f"{name}: default command does not show self-attested checkpoints")
    # English before Chinese: checkpoint titles must not lead with Chinese
    # (FP-709 mixed-order debt) — shared-core titles are stored "zh / en".
    for line in lines:
        if re.match(r"  l\d{2}  ", line):
            title = line.split("  ", 3)[2] if line.count("  ") >= 3 else ""
            if re.match(r"^[\u4e00-\u9fff]", title):
                problems.append(f"{name}: default command prints a Chinese-first checkpoint title")
                break
    return problems


# ── Standalone-folder contract (FP-821) ────────────────────────────────────
# A course fetched through /api/challenges/<slug>/files must verify alone:
# only the course folder plus the shared files the endpoint attaches (the
# repo-relative tools/ tree, e.g. claim_receipt.py). This check rebuilds that
# layout in a temp directory and runs the default command + receipts there.

STANDALONE_SHARED = ("tools/claim_receipt.py",)


def check_standalone_run(course: Path) -> list[str]:
    name = course.name
    problems: list[str] = []
    with tempfile.TemporaryDirectory(prefix="fp-standalone-") as tmp:
        root = Path(tmp)
        isolated = root / "courses" / name
        shutil.copytree(
            course, isolated,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"),
        )
        for shared in STANDALONE_SHARED:
            source = ROOT / shared
            if not source.exists():
                problems.append(f"{name}: shared file {shared} missing from repo")
                continue
            (root / shared).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, root / shared)

        default = subprocess.run(
            [sys.executable, str(isolated / "verify.py")],
            check=False, capture_output=True, text=True,
        )
        if default.returncode != 1:
            problems.append(
                f"{name}: standalone default command exited {default.returncode}"
                " (expected 1: the shipped starter intentionally fails)")
        elif "Suites:" not in default.stdout or "l03" not in default.stdout:
            problems.append(f"{name}: standalone default command did not print checkpoint status")

        env = dict(os.environ, FLYPYTHON_CLAIM_SECRET="standalone-test-secret")
        receipts = subprocess.run(
            [sys.executable, str(isolated / "verify.py"), "progress", "--json"],
            check=False, capture_output=True, text=True, env=env,
        )
        if receipts.returncode != 0:
            problems.append(
                f"{name}: standalone progress failed\n"
                f"{(receipts.stdout or '') + (receipts.stderr or '')}".rstrip())
        else:
            try:
                document = json.loads(receipts.stdout)
            except ValueError:
                problems.append(f"{name}: standalone progress --json did not emit valid JSON")
                document = {}
            if not document.get("receipts"):
                problems.append(
                    f"{name}: standalone run produced no receipts — the shared"
                    " tools/ file the files endpoint attaches is not loadable")
    return problems


# ── Shared-core enforcement (docs/courses/README.md §5.2, FP-711) ─────────
# Agent-tool courses share one exercise — the report-tool scenario skins,
# starter/solution pair, tests, and task contract. Folders stay
# self-contained (a copied course still verifies alone), so instead of a
# shared directory the members carry a `core-group` marker file and this
# check enforces byte-for-byte equality of the core. verify.py is exempt
# only inside its marked PER-COURSE BLOCK (course id, salt, titles).

SKIP_PARTS = {"__pycache__", ".git", ".venv", "venv", "node_modules"}
CORE_FILES = ("TASK.md", "TASK_cn.md")
CORE_DIRS = ("tests", "starter", "solution", "scenario")
BLOCK_RE = re.compile(
    r"# ── PER-COURSE BLOCK ─+\n.*?# ── END PER-COURSE BLOCK ─+", re.S
)


def _core_payloads(course: Path) -> dict[str, bytes]:
    payloads: dict[str, bytes] = {}
    for name in CORE_FILES:
        path = course / name
        if path.exists():
            payloads[name] = path.read_bytes()
    for dirname in CORE_DIRS:
        base = course / dirname
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            rel = path.relative_to(course)
            if not path.is_file() or any(part in SKIP_PARTS for part in rel.parts):
                continue
            payloads[rel.as_posix()] = path.read_bytes()
    verify = course / "verify.py"
    if verify.exists():
        normalized = BLOCK_RE.sub("# <per-course block stripped>", verify.read_text(encoding="utf-8"))
        payloads["verify.py(normalized)"] = normalized.encode("utf-8")
    return payloads


def check_shared_core(courses: list[Path]) -> list[str]:
    groups: dict[str, list[Path]] = {}
    for course in courses:
        marker = course / "core-group"
        if marker.exists():
            groups.setdefault(marker.read_text(encoding="utf-8").strip(), []).append(course)

    problems: list[str] = []
    for group, members in groups.items():
        if len(members) < 2:
            problems.append(f"core-group {group}: only one member ({members[0].name})")
            continue
        reference = _core_payloads(members[0])
        for member in members[1:]:
            other = _core_payloads(member)
            for name in sorted(set(reference) | set(other)):
                if reference.get(name) != other.get(name):
                    problems.append(
                        f"core-group {group}: {members[0].name} vs {member.name} differ on {name}"
                    )
        # Inside the per-course block, checkpoint ids and gates are core —
        # only the display titles may differ. Compare (id, gate) shapes.
        shapes = []
        for member in members:
            verify = (member / "verify.py").read_text(encoding="utf-8") if (member / "verify.py").exists() else ""
            if verify and not BLOCK_RE.search(verify):
                problems.append(f"{member.name}: verify.py has no marked PER-COURSE BLOCK")
            shapes.append(list(zip(
                re.findall(r'"id":\s*"(l\d+|capstone)"', verify),
                re.findall(r'"gate":\s*"([a-z-]+)"', verify),
            )))
        for member, shape in zip(members[1:], shapes[1:]):
            if shape != shapes[0]:
                problems.append(
                    f"core-group {group}: {member.name} checkpoint ids/gates differ from {members[0].name}"
                )
    return problems


def main() -> int:
    courses = discover_courses(ROOT)
    if not courses:
        print("error: no course folders found under courses/*/", file=sys.stderr)
        return 1

    problems: list[str] = []
    for course in courses:
        problems.extend(check_bilingual_contract(course))
        problems.extend(run_course_verifier(course))
        problems.extend(check_default_command(course))
        problems.extend(check_standalone_run(course))
    problems.extend(check_shared_core(courses))

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print(f"all {len(courses)} course folder(s) satisfy the course contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
