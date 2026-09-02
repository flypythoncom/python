#!/usr/bin/env python3
"""Verify every published runnable example."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    verify = ROOT / "examples" / "product-slug" / "verify.py"
    commands = (
        [sys.executable, str(verify), "starter", "--expect-failure"],
        [sys.executable, str(verify), "solution"],
    )
    for command in commands:
        result = subprocess.run(command, check=False)
        if result.returncode:
            return result.returncode
    print("all runnable examples are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
