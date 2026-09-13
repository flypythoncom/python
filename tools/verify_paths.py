#!/usr/bin/env python3
"""Verify every learning-path contract under paths/*/path.json.

Per path: required bilingual fields, a badge block, sequential module
orders, course refs that resolve to courses/<slug>/, and module refs that
resolve to paired EN/ZH markdown files under modules/.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FIELDS = ("id", "slug", "status", "title_en", "title_zh",
                   "summary_en", "summary_zh", "audience_en", "audience_zh",
                   "outcome_en", "outcome_zh", "badge", "modules")
MODULE_KINDS = {"course", "module"}


def check_path(path_file: Path) -> list[str]:
    problems: list[str] = []
    path_dir = path_file.parent
    name = path_dir.name

    try:
        data = json.loads(path_file.read_text(encoding="utf-8"))
    except ValueError:
        return [f"{name}: path.json is not valid JSON"]

    for field in REQUIRED_FIELDS:
        if field not in data:
            problems.append(f"{name}: missing field {field!r}")

    badge = data.get("badge") or {}
    for key in ("id", "name_en", "name_zh"):
        if key not in badge:
            problems.append(f"{name}: badge missing {key!r}")

    modules = data.get("modules")
    if not isinstance(modules, list) or not modules:
        problems.append(f"{name}: modules must be a non-empty list")
        return problems

    orders = [m.get("order") for m in modules]
    if orders != list(range(len(modules))):
        problems.append(f"{name}: module orders must be sequential from 0")

    for module in modules:
        mid = module.get("id", "?")
        kind = module.get("kind")
        if kind not in MODULE_KINDS:
            problems.append(f"{name}: module {mid!r} has unknown kind {kind!r}")
            continue
        if "points" not in module:
            problems.append(f"{name}: module {mid!r} missing points")
        if "optional" in module and not isinstance(module["optional"], bool):
            problems.append(f"{name}: module {mid!r} optional must be a boolean")
        if module.get("optional") and modules[0] is module:
            problems.append(f"{name}: optional module {mid!r} cannot be the first step")
        if kind == "course":
            slug = module.get("course", "")
            if not (ROOT / "courses" / slug).is_dir():
                problems.append(f"{name}: module {mid!r} references missing course {slug!r}")
        else:
            ref = module.get("ref", "")
            doc = path_dir / ref
            if not doc.exists():
                problems.append(f"{name}: module {mid!r} references missing {ref!r}")
            elif ref.endswith(".md") and not (path_dir / ref.replace(".md", "_cn.md")).exists():
                problems.append(f"{name}: module {mid!r} doc {ref!r} has no _cn pair")
    return problems


def main() -> int:
    paths_dir = ROOT / "paths"
    path_files = sorted(paths_dir.glob("*/path.json")) if paths_dir.is_dir() else []
    if not path_files:
        print("error: no paths/*/path.json found", file=sys.stderr)
        return 1

    problems: list[str] = []
    for path_file in path_files:
        problems.extend(check_path(path_file))

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print(f"path contracts verified: {len(path_files)} paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
