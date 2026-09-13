#!/usr/bin/env python3
"""Run the mcp-server contract against the starter or solution."""

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



COURSE_ID = 'course-mcp-tools'
# Documented constant: claim codes derive deterministically from
# (COURSE_ID, checkpoint_id, COURSE_SALT). They are spot-checkable
# self-reported evidence, not tamper-proof secrets — see
# docs/repo-plan-0.0.4.md FP-411.
COURSE_SALT = 'c328e39d6c8f8de4'

CHECKPOINTS = [
    {"id": "l01", "gate": "attest", "title": 'MCP 是什么（2026-07-28）/ What MCP actually is'},
    {"id": "l02", "gate": "attest", "title": 'JSON-RPC 分发契约 / The dispatch contract'},
    {"id": "l03", "gate": "starter-suite", "title": '校验与错误隔离 / Validation and error isolation'},
    {"id": "l04", "gate": "both-suites", "title": 'input_required 多轮交互 / The input_required round-trip'},
    {"id": "l05", "gate": "attest", "title": '暴露一个真实工具 / Expose one real tool'},
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
    starter = _run_suite("starter")
    solution = _run_suite("solution")
    starter_ok = starter.returncode == 0
    solution_ok = solution.returncode == 0
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
        starter_state = "通过" if starter_ok else "未通过"
        solution_state = "通过" if solution_ok else "未通过"
        print("课程 " + COURSE_ID)
        print("实现状态: starter " + starter_state + " / solution " + solution_state)
        for row in rows:
            state = row["status"] + ("（自报）" if row["kind"] == "attested" else "")
            code = "认领码 " + row["claim_code"] if row["claim_code"] else "—"
            print("  " + row["id"] + "  " + row["title"] + "  [" + state + "]  " + code)
        print("认领码是自我报告的证据，在 flypython.com 记录；绝非证书。")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("implementation", choices=("progress", "starter", "solution"))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--expect-failure", action="store_true")
    args = parser.parse_args()

    if args.implementation == "progress":
        return run_progress(args.json)

    command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        str(ROOT / "tests"),
    ]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / args.implementation)
    result = subprocess.run(
        command,
        env=environment,
        check=False,
        capture_output=args.expect_failure,
        text=args.expect_failure,
    )

    if args.expect_failure:
        if result.returncode == 0:
            print("Expected the starter to fail, but it passed.", file=sys.stderr)
            return 1
        output = (result.stdout or "") + (result.stderr or "")
        expected_failures = (
            "test_invalid_request_structure",
            "test_tools_call_handles_runtime_exception",
            "test_tools_call_missing_required_argument",
        )
        missing = [n for n in expected_failures if n not in output]
        if missing:
            print("Starter failed for unexpected reasons:", file=sys.stderr)
            print("\n".join(missing), file=sys.stderr)
            print(output, file=sys.stderr)
            return 1
        print("Expected MCP boundary regression reproduced: unhandled exceptions and missing schema validations fail.")
        return 0
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
