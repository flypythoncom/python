#!/usr/bin/env python3
"""Verify every published runnable example dynamically."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def discover_example_verifiers(root: Path) -> list[Path]:
    """Find all verify.py scripts in example directories."""
    examples_dir = root / "examples"
    if not examples_dir.exists():
        return []
    return sorted(examples_dir.glob("*/verify.py"))


def main() -> int:
    verifiers = discover_example_verifiers(ROOT)
    if not verifiers:
        print("error: no runnable examples found under examples/*/", file=sys.stderr)
        return 1

    for verify in verifiers:
        example_name = verify.parent.name
        commands = (
            [sys.executable, str(verify), "starter", "--expect-failure"],
            [sys.executable, str(verify), "solution"],
        )
        for command in commands:
            result = subprocess.run(command, check=False)
            if result.returncode != 0:
                print(
                    f"verification failed for example '{example_name}': {' '.join(command)}",
                    file=sys.stderr,
                )
                return result.returncode

    print(f"all {len(verifiers)} runnable example(s) are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
