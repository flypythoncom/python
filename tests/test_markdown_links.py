from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def test_relative_markdown_links_resolve() -> None:
    missing: list[str] = []
    for document in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in document.relative_to(ROOT).parts):
            continue
        content = document.read_text(encoding="utf-8")
        for target in LINK.findall(content):
            path_text = target.split("#", maxsplit=1)[0]
            if not path_text or "://" in path_text or path_text.startswith("mailto:"):
                continue
            destination = (document.parent / path_text).resolve()
            if not destination.exists() or (destination != ROOT and ROOT not in destination.parents):
                missing.append(f"{document.relative_to(ROOT)} -> {target}")
    assert not missing, "broken relative Markdown links:\n" + "\n".join(missing)
