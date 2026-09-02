from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "examples" / "product-slug" / "verify.py"


def test_product_slug_example_has_a_failing_starter_and_passing_solution() -> None:
    subprocess.run(
        [sys.executable, str(VERIFY), "starter", "--expect-failure"],
        check=True,
    )
    subprocess.run([sys.executable, str(VERIFY), "solution"], check=True)
