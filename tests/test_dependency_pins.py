"""Learners install a course's own requirements.txt; CI verifies the course
with requirements-dev.lock.txt. Both must resolve to the same versions, or CI
would pass on a stack learners never get (the pandas 3 risk in PR #94)."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==([^\s;]+)\s*(;.*)?$")


def _normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _requirement_lines(path: Path) -> list[str]:
    lines = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            lines.append(line)
    return lines


def _learner_requirement_files() -> list[Path]:
    tracked = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "courses/*/requirements.txt", "paths/**/requirements.txt"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.split()
    return [ROOT / name for name in sorted(tracked)]


def _dev_lock_pins() -> dict[str, list[tuple[str, str | None]]]:
    pins: dict[str, list[tuple[str, str | None]]] = {}
    for line in _requirement_lines(ROOT / "requirements-dev.lock.txt"):
        match = PIN.match(line)
        if match:
            name, version, marker = match.groups()
            pins.setdefault(_normalize(name), []).append((version, marker))
    return pins


def test_learner_requirement_files_exist() -> None:
    assert _learner_requirement_files(), "expected course/path requirements.txt files"


def test_learner_requirements_match_the_ci_lock() -> None:
    lock = _dev_lock_pins()
    problems = []
    for path in _learner_requirement_files():
        rel = path.relative_to(ROOT)
        for line in _requirement_lines(path):
            match = PIN.match(line)
            if not match or match.group(3):
                problems.append(f"{rel}: '{line}' must be an exact, unconditional == pin")
                continue
            name, version, _ = match.groups()
            locked = lock.get(_normalize(name))
            if locked is None:
                problems.append(f"{rel}: {name} is not in requirements-dev.lock.txt")
            elif locked != [(version, None)]:
                found = ", ".join(v + (f" ({m.lstrip('; ')})" if m else "") for v, m in locked)
                problems.append(f"{rel}: {name}=={version}, but the CI lock has {found}")
    assert problems == []
