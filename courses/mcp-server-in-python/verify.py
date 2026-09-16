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

# Optional shared claim-receipt producer (docs/CLAIM-RECEIPT.md). The course
# folder still verifies standalone — without the tools/ sibling or without
# FLYPYTHON_CLAIM_SECRET set, verify.py behaves exactly as before.
try:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
    import claim_receipt
except ImportError:
    claim_receipt = None



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


def _display_title(title):
    # FP-820: shared-core checkpoint titles are stored "Chinese / English";
    # the default command prints English first, Chinese after (FP-709 debt).
    if " / " in title:
        left, _, right = title.partition(" / ")
        if any("\u4e00" <= character <= "\u9fff" for character in left):
            return right + " / " + left
    return title

def _run_suite(implementation):
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / implementation)
    return subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests")],
        env=environment, check=False, capture_output=True, text=True,
    )

def run_progress(as_json, receipt_out=None, default=False):
    import time
    t0 = time.monotonic()
    starter = _run_suite("starter")
    starter_ms = int((time.monotonic() - t0) * 1000)
    t0 = time.monotonic()
    solution = _run_suite("solution")
    solution_ms = int((time.monotonic() - t0) * 1000)
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
    secret = claim_receipt.receipts_enabled() if claim_receipt else None
    receipts = []
    if secret:
        starter_tests = claim_receipt.count_tests(starter.stderr)
        solution_tests = claim_receipt.count_tests(solution.stderr)
        solution_hash = claim_receipt.solution_sha256(ROOT)
        for checkpoint in CHECKPOINTS:
            gate = checkpoint["gate"]
            if gate == "starter-suite":
                passed, tests, ms = starter_ok, starter_tests, starter_ms
            elif gate == "both-suites":
                passed = starter_ok and solution_ok
                tests, ms = starter_tests + solution_tests, starter_ms + solution_ms
            else:
                continue
            receipts.append(claim_receipt.make_receipt(
                COURSE_ID, checkpoint["id"], passed=passed, tests=tests,
                duration_ms=ms, impl_dir=ROOT / "starter",
                solution_hash=solution_hash, secret=secret))
    if default and not as_json:
        # FP-820: bare ``python verify.py`` — check the learner's own
        # implementation, print per-checkpoint status and earned claim codes,
        # English first then Chinese (FP-709 debt). ``progress`` keeps its
        # exact published output; this block is the only new surface.
        print("Course " + COURSE_ID)
        print("Suites: starter " + ("passed" if starter_ok else "not passed")
              + " / solution " + ("passed" if solution_ok else "not passed"))
        for row in rows:
            state = row["status"] + (" (self-attested)" if row["kind"] == "attested" else "")
            code = row["claim_code"] if row["claim_code"] else "\u2014"
            print("  " + row["id"] + "  " + _display_title(row["title"]) + "  [" + state + "]  " + code)
        open_gates = [row["id"] for row in rows
                      if row["kind"] == "objective" and row["status"] != "passed"]
        if open_gates:
            print("Next: keep implementing starter/ until " + ", ".join(open_gates)
                  + " show [passed]; then re-run: python verify.py")
        else:
            print("All objective checkpoints passed — the codes above are ready"
                  " to submit (batch POST /api/claims, see SKILL.md §5).")
        print("\u4e2d\u6587\uff1a\u68c0\u67e5\u70b9\u72b6\u6001\u4e0e\u8ba4\u9886\u7801\u89c1\u4e0a\uff1b\u5e26 [passed]/[attest] \u7684\u884c\u6709\u8ba4\u9886\u7801\uff0c[open] \u7684\u884c\u7ee7\u7eed\u5728 starter/ \u91cc\u5b9e\u73b0\u540e\u518d\u8dd1\u3002")
        print("Claim codes are self-reported evidence, recorded at flypython.com; never a certificate.")
        print("\u8ba4\u9886\u7801\u662f\u81ea\u6211\u62a5\u544a\u7684\u8bc1\u636e\uff0c\u8bb0\u5f55\u5728 flypython.com\uff1b\u4e0d\u662f\u8bc1\u4e66\u3002")
        if secret:
            print(f"Signed run receipts prepared for {len(receipts)} gated checkpoint(s);"
                  " submit each with its claim to mark it as a local-run receipt.")
        return 1 if open_gates else 0
    if as_json:
        document = {"course": COURSE_ID,
            "starter_suite_passed": starter_ok,
            "solution_suite_passed": solution_ok,
            "checkpoints": rows}
        if secret:
            document["receipts"] = receipts
        print(json.dumps(document, ensure_ascii=False, indent=2))
    else:
        starter_state = "passed" if starter_ok else "not passed"
        solution_state = "passed" if solution_ok else "not passed"
        print("Course " + COURSE_ID)
        print("Suites: starter " + starter_state + " / solution " + solution_state)
        for row in rows:
            state = row["status"] + (" (self-attested)" if row["kind"] == "attested" else "")
            code = "claim code " + row["claim_code"] if row["claim_code"] else "—"
            print("  " + row["id"] + "  " + row["title"] + "  [" + state + "]  " + code)
        print("Claim codes are self-reported evidence, recorded at flypython.com; never a certificate.")
        if secret:
            print(f"Signed run receipts prepared for {len(receipts)} gated checkpoint(s);"
                  " submit each with its claim to mark them as a local-run receipt.")
    if receipt_out and secret:
        Path(receipt_out).write_text(
            json.dumps({"receipts": receipts}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        print(f"Wrote {len(receipts)} receipt(s) to {receipt_out}", file=sys.stderr)
    return 0

def run_check(as_json=False, attested=()):
    """Learner-facing v2 check: run only starter/ and require explicit attestation.

    The published progress command remains the v1 claim-receipt interface.
    The reference solution is checked by the maintainer's course validation,
    not rerun on every learner check.
    """
    selected = set(attested)
    allowed = {item["id"] for item in CHECKPOINTS if item["gate"] == "attest"}
    unknown = selected - allowed
    if unknown:
        print("Only self-reported checkpoints can be attested: " + ", ".join(sorted(unknown)), file=sys.stderr)
        return 2
    dependency_check = globals().get("_deps_available")
    blocked = callable(dependency_check) and not dependency_check()
    result = None if blocked else _run_suite("starter")
    passed = result is not None and result.returncode == 0
    rows = []
    for item in CHECKPOINTS:
        self_report = item["gate"] == "attest"
        status = ("attested" if item["id"] in selected else "pending") if self_report else ("blocked" if blocked else "passed" if passed else "open")
        rows.append({"id": item["id"], "title": _display_title(item["title"]),
                     "kind": "self-reported" if self_report else "objective",
                     "status": status,
                     "claim_code": _claim_code(item["id"]) if status in ("passed", "attested") else None})
    document = {"v": 2, "course": COURSE_ID, "implementation": "starter",
                "suite": {"status": "blocked" if blocked else "passed" if passed else "failed",
                          "reason": "Install this course's requirements first." if blocked else None},
                "checkpoints": rows}
    if as_json:
        print(json.dumps(document, ensure_ascii=False, indent=2))
    else:
        print("Course " + COURSE_ID)
        print("Suites: starter " + ("blocked: install course requirements" if blocked else "passed" if passed else "not passed"))
        for row in rows:
            print("  " + row["id"] + "  " + row["title"] + "  [" + row["status"] + "]  " + (row["claim_code"] or "—"))
        pending = [row["id"] for row in rows if row["status"] == "pending"]
        if pending:
            print("Confirm completed reflection checkpoints explicitly with --attest ID (repeat for each): " + ", ".join(pending))
        if result is not None and not passed:
            print((result.stderr or result.stdout or "").strip()[-3000:], file=sys.stderr)
        print("Codes record self-reported progress, not a certificate. / 认领码只记录自报进度，不是证书。")
    return 0 if all(row["status"] in ("passed", "attested") for row in rows) else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("implementation", choices=("check", "progress", "starter", "solution"),
                        nargs="?", default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--expect-failure", action="store_true")
    parser.add_argument("--receipt-out", metavar="PATH", help="write signed run receipts JSON (requires FLYPYTHON_CLAIM_SECRET)")
    parser.add_argument("--attest", action="append", default=[], metavar="ID", help="confirm one self-reported checkpoint after doing its work")
    args = parser.parse_args()

    if args.implementation in (None, "check"):
        if args.receipt_out or args.expect_failure:
            parser.error("--receipt-out and --expect-failure are for legacy progress/fixture commands")
        return run_check(args.json, args.attest)
    if args.attest:
        parser.error("--attest is only valid with the learner check command")
    if args.implementation == "progress":
        return run_progress(args.json, args.receipt_out)

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
    if result.returncode == 0:
        print(f"{args.implementation}: all tests passed")
    else:
        sys.stderr.write((result.stderr or "") or (result.stdout or ""))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
