"""Keep developer entry points safe and aligned with generated-content gates."""

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _make(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    if not shutil.which("make"):
        pytest.skip("GNU/POSIX make is not installed")
    return subprocess.run(
        ["make", *args], cwd=cwd, capture_output=True, text=True, timeout=15,
        check=False,
    )


def test_agent_entrypoint_has_single_source() -> None:
    assert (ROOT / "CLAUDE.md").read_text().strip() == "@AGENTS.md"
    assert "* text=auto eol=lf" in (ROOT / ".gitattributes").read_text()


def test_make_rejects_unrelated_working_directory(tmp_path: Path) -> None:
    result = _make("-f", str(ROOT / "Makefile"), "-n", "setup", cwd=tmp_path)
    assert result.returncode != 0
    assert "run make in the Python repository" in result.stderr


def test_make_generated_checks_are_read_only_and_include_solution_hashes() -> None:
    result = _make("-n", "generated-check")
    assert result.returncode == 0, result.stderr
    for name in ("export_catalog", "render_readmes", "build_content_manifest", "build_solution_hashes"):
        assert f"tools/{name}.py --check" in result.stdout


def test_make_setup_uses_pinned_interpreter_and_locked_dependencies() -> None:
    result = _make("-n", "setup")
    assert result.returncode == 0, result.stderr
    assert ".python-version" in result.stdout
    assert "pip sync --python .venv/bin/python requirements-dev.lock.txt" in result.stdout


def test_make_all_regenerates_before_checks_even_in_parallel() -> None:
    result = _make("-n", "-j4", "all")
    assert result.returncode == 0, result.stderr
    assert result.stdout.index("tools/build_solution_hashes.py\n") < result.stdout.index("-m ruff check .")
