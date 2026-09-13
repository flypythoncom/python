#!/usr/bin/env python3
"""Verify the data-analysis capstone output.

Checks out/results.json against dataset ground truth (tolerance 0.01)
and out/report.md for the required sections. Prints the capstone claim
code on success — self-reported evidence for flypython.com, never a
certificate.
"""

from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "out"

CHALLENGE_ID = "capstone-data-analysis"
COURSE_SALT = "f1a2b3c4d5e6f7a8"

EXPECTED = {
    "rows_total": 303,
    "duplicates_removed": 3,
    "rows_clean": 294,
    "total_revenue": 110217.74,
    "avg_order_value": 374.89,
    "total_quantity": 1286,
    "top_category": "Clothing",
    "first_date": "2026-05-01",
    "last_date": "2026-06-30",
}
EXPECTED_REGIONS = {"East": 34031.39, "North": 22001.64,
                    "South": 28675.58, "West": 25509.13}
REQUIRED_SECTIONS = ("## Data quality", "## Findings", "## Appendix")


def _claim_code():
    digest = hashlib.sha256(
        (CHALLENGE_ID + ":capstone:" + COURSE_SALT).encode("utf-8")
    ).digest()
    return base64.b32encode(digest).decode("ascii")[:8]


def _close(actual, expected, tol=0.01):
    try:
        return abs(float(actual) - float(expected)) <= tol
    except (TypeError, ValueError):
        return False


def main() -> int:
    problems = []
    results_path = OUT_DIR / "results.json"
    report_path = OUT_DIR / "report.md"

    if not results_path.exists():
        problems.append("missing out/results.json")
    else:
        try:
            results = json.loads(results_path.read_text(encoding="utf-8"))
        except ValueError:
            problems.append("out/results.json is not valid JSON")
            results = None
        if results is not None:
            for key, expected in EXPECTED.items():
                actual = results.get(key)
                if isinstance(expected, float):
                    ok = _close(actual, expected)
                else:
                    ok = actual == expected
                if not ok:
                    problems.append(f"results.{key}: expected {expected!r}, got {actual!r}")
            regions = results.get("revenue_by_region") or {}
            for region, expected in EXPECTED_REGIONS.items():
                if not _close(regions.get(region), expected):
                    problems.append(
                        f"revenue_by_region.{region}: expected {expected}, "
                        f"got {regions.get(region)!r}")

    if not report_path.exists():
        problems.append("missing out/report.md")
    else:
        text = report_path.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                problems.append(f"report.md missing section {section!r}")
        if "110217.74" not in text:
            problems.append("report.md does not state the verified total revenue")

    if problems:
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        return 1

    print(f"capstone verified — claim code: {_claim_code()}")
    print("\u4e2d\u6587\uff1a\u6bd5\u4e1a\u9879\u76ee\u5df2\u901a\u8fc7\uff0c\u8ba4\u9886\u7801\u89c1\u4e0a\uff1b\u63d0\u4ea4\u5230 flypython.com\u3002")
    print("Self-reported evidence for flypython.com, never a certificate.")
    print("\u8ba4\u9886\u7801\u662f\u81ea\u6211\u62a5\u544a\u7684\u8bc1\u636e\uff0c\u4e0d\u662f\u8bc1\u4e66\u3002")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
