#!/usr/bin/env python3
"""Run the course contract against starter or solution.

Objective completion evidence for "From analysis to report" (da-report).
``progress`` prints checkpoint claim codes for recording on flypython.com.
Standard library only — no dependencies to install.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXPECTED_STARTER_FAILURES = (
    "test_load_returns_dict",
    "test_metrics_match_inputs",
    "test_required_sections_in_order",
    "test_headings_present",
    "test_key_numbers_appear",
    "test_main_writes_report_files",
)

COURSE_ID = 'course-da-report'
# Documented constant: claim codes derive deterministically from
# (COURSE_ID, checkpoint_id, COURSE_SALT). Spot-checkable self-reported
# evidence, not tamper-proof secrets — see docs/repo-plan-0.0.4.md FP-411.
COURSE_SALT = 'b9d2e8f14c6a7053'

CHECKPOINTS = [
    {"id": "l01", "gate": "attest", "title": 'A report is a contract with the reader'},
    {"id": "l02", "gate": "attest", "title": 'Structure before prose'},
    {"id": "l03", "gate": "starter-suite", "title": 'Build and render the report'},
    {"id": "l04", "gate": "both-suites", "title": 'Numbers traceable to inputs'},
    {"id": "l05", "gate": "attest", "title": 'What report verification cannot see'},
]


def _claim_code(checkpoint_id):
    digest = hashlib.sha256(
        (COURSE_ID + ":" + checkpoint_id + ":" + COURSE_SALT).encode("utf-8")
    ).digest()
    return base64.b32encode(digest).decode("ascii")[:8]


def _run_suite(implementation):
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / implementation)
    return subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests")],
        env=environment, check=False, capture_output=True, text=True,
    )


def run_progress(as_json):
    starter_ok = _run_suite("starter").returncode == 0
    solution_ok = _run_suite("solution").returncode == 0
    rows = []
    for checkpoint in CHECKPOINTS:
        gate = checkpoint["gate"]
        if gate == "attest":
            status, kind = "attest", "attested"
        elif gate == "starter-suite":
            status = "passed" if starter_ok else "open"
            kind = "objective"
        else:
            status = "passed" if (starter_ok and solution_ok) else "open"
            kind = "objective"
        code = _claim_code(checkpoint["id"]) if status in ("passed", "attest") else None
        row = dict(checkpoint)
        row["status"] = status
        row["kind"] = kind
        row["claim_code"] = code
        rows.append(row)
    if as_json:
        print(json.dumps({"course": COURSE_ID,
            "starter_suite_passed": starter_ok,
            "solution_suite_passed": solution_ok,
            "checkpoints": rows}, ensure_ascii=False, indent=2))
    else:
        starter_state = "passed" if starter_ok else "not passed"
        solution_state = "passed" if solution_ok else "not passed"
        print("Course " + COURSE_ID)
        print("Suites: starter " + starter_state + " / solution " + solution_state)
        for row in rows:
            state = row["status"] + (" (self-attested)" if row["kind"] == "attested" else "")
            code = "claim " + row["claim_code"] if row["claim_code"] else "—"
            print("  " + row["id"] + "  " + row["title"] + "  [" + state + "]  " + code)
        print("Claim codes are self-reported evidence recorded on flypython.com — never a certificate.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("implementation", choices=("progress", "starter", "solution"))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--expect-failure", action="store_true")
    args = parser.parse_args()

    if args.implementation == "progress":
        return run_progress(args.json)

    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / args.implementation)
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests")],
        env=environment, check=False, capture_output=True, text=True,
    )

    if args.expect_failure:
        if result.returncode == 0:
            print("Expected the starter to fail, but it passed.", file=sys.stderr)
            return 1
        output = (result.stdout or "") + (result.stderr or "")
        missing = [n for n in EXPECTED_STARTER_FAILURES if n not in output]
        if missing:
            print("Starter failed for unexpected reasons:", file=sys.stderr)
            print("\n".join(missing), file=sys.stderr)
            print(output, file=sys.stderr)
            return 1
        print("Expected starter state reproduced: report functions unimplemented.")
        return 0
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
