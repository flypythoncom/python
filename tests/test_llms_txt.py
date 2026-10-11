"""llms.txt is the entry point agents read first, so a stale path or a missing
course sends them to a 404 or hides a course entirely."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LLMS = ROOT / "llms.txt"
REPO_PATH = re.compile(
    r"`((?:catalog|courses|examples|guides|paths|playbooks|schema|templates|tools)/[^`\s]*)`"
)


def _listed_paths() -> list[str]:
    return REPO_PATH.findall(LLMS.read_text(encoding="utf-8"))


def test_every_repository_path_exists() -> None:
    missing = [path for path in _listed_paths() if not (ROOT / path).exists()]
    assert not missing, f"llms.txt points at paths that do not exist: {missing}"


def test_every_course_folder_is_listed() -> None:
    listed = {path.rstrip("/") for path in _listed_paths()}
    courses = sorted(
        f"courses/{course.name}"
        for course in (ROOT / "courses").iterdir()
        if (course / "COURSE.md").is_file()
    )
    unlisted = [course for course in courses if course not in listed]
    assert not unlisted, f"llms.txt does not list these courses: {unlisted}"
