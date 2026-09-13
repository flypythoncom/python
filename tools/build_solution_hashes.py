#!/usr/bin/env python3
"""Generate or verify course-solutions.json — the per-course solution tree
hashes the website uses to independently recompute receipt.solution_match
(docs/CLAIM-RECEIPT.md, FP-705).

The hash is exactly tools/claim_receipt.tree_sha256 over the course's
solution/ directory, so producer and verifier agree byte-for-byte. Courses
without a solution/ directory are omitted; courses whose solution tree is
empty hash to the empty-tree digest (still published, still comparable).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "course-solutions.json"
COURSE_ID_PATTERN = re.compile(r'''^COURSE_ID\s*=\s*["']([^"']+)["']''', re.M)

sys.path.insert(0, str(ROOT / "tools"))
import claim_receipt  # noqa: E402


def build(root: Path) -> dict:
    courses = []
    for course_dir in sorted((root / "courses").iterdir()):
        if not course_dir.is_dir():
            continue
        verify = course_dir / "verify.py"
        if not verify.exists():
            continue
        match = COURSE_ID_PATTERN.search(verify.read_text(encoding="utf-8"))
        if not match:
            raise SystemExit(f"{course_dir.name}: no COURSE_ID constant in verify.py")
        digest = claim_receipt.solution_sha256(course_dir)
        if digest is None:
            continue
        courses.append(
            {
                "slug": course_dir.name,
                "course_id": match.group(1),
                "solution_sha256": digest,
            }
        )
    return {"schema_version": 1, "courses": courses}


def dump(document: dict) -> str:
    return json.dumps(document, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rendered = dump(build(ROOT))
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != rendered:
            print("course-solutions.json is stale; regenerate it", file=sys.stderr)
            return 1
        print("course-solutions.json is current")
        return 0
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUTPUT.name} ({len(json.loads(rendered)['courses'])} courses)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
