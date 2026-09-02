#!/usr/bin/env python3
"""Run the product-slug contract against the starter or solution."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("implementation", choices=("starter", "solution"))
    parser.add_argument("--expect-failure", action="store_true")
    args = parser.parse_args()

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
            "FAIL: test_collapses_mixed_separators",
            "FAIL: test_rejects_an_empty_result",
            "FAIL: test_removes_punctuation",
        )
        if not all(failure in output for failure in expected_failures):
            print("Starter failed for an unexpected reason:", file=sys.stderr)
            print(output, file=sys.stderr)
            return 1
        print("Expected regression reproduced: 3 boundary cases fail.")
        return 0
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
