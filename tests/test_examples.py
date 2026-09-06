from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from tools.verify_examples import discover_example_verifiers

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_VERIFIERS = discover_example_verifiers(ROOT)


@pytest.mark.parametrize("verify_path", EXAMPLE_VERIFIERS, ids=lambda p: p.parent.name)
def test_example_has_failing_starter_and_passing_solution(verify_path: Path) -> None:
    subprocess.run(
        [sys.executable, str(verify_path), "starter", "--expect-failure"],
        check=True,
    )
    subprocess.run([sys.executable, str(verify_path), "solution"], check=True)
