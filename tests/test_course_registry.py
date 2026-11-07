"""Regression coverage for the canonical course-to-website contract."""
import copy
import json
import shutil
from pathlib import Path

import pytest
from jsonschema import ValidationError

from tools.build_course_registry import build_registry, verifier_contract

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def repo(tmp_path):
    shutil.copytree(ROOT / "courses", tmp_path / "courses")
    shutil.copytree(ROOT / "schemas", tmp_path / "schemas")
    return tmp_path


def test_registry_matches_generated_and_verifiers():
    registry = build_registry()
    assert registry == json.loads((ROOT / "course-registry.json").read_text())
    for course in registry["courses"]:
        assert registry["contracts"][course["id"]] == verifier_contract(ROOT / course["repoDir"] / "verify.py")
        for filename, identity in [("COURSE.md", "I'm Coach P, an AI coach running inside your own agent"),
                                   ("COURSE_cn.md", "我是小P老师，一个运行在你自己 Agent 里的 AI 教练")]:
            text = (ROOT / course["repoDir"] / filename).read_text()
            assert identity in text
            assert "--attest" in text
            assert "solution/" in text


def test_new_course_is_discovered_without_website_edits(repo):
    source = repo / "courses/hands-on-python-with-claude-code"
    target = repo / "courses/new-course"
    shutil.copytree(source, target)
    # Include lesson metadata IDs, as each is unique in the public manifest.
    for path in target.rglob("*.md"):
        path.write_text(path.read_text().replace("course-claude-code", "course-new"))
    verifier = target / "verify.py"
    verifier.write_text(verifier.read_text().replace("course-claude-code", "course-new"))
    path = target / "website.json"
    metadata = json.loads(path.read_text())
    metadata.update(id="new-course", order=100, agentTool=False, aliases=[])
    path.write_text(json.dumps(metadata))
    registry = build_registry(repo)
    assert registry["courses"][-1]["id"] == "new-course"
    assert registry["contracts"]["new-course"]["courseId"] == "course-new"


@pytest.mark.parametrize("mutation", ["missing", "duplicate-order", "bad-lessons", "alias-collision", "private"])
def test_invalid_course_fails_closed(repo, mutation):
    path = repo / "courses/hands-on-python-with-claude-code/website.json"
    data = json.loads(path.read_text())
    if mutation == "missing":
        del data["summaryZh"]
    elif mutation == "duplicate-order":
        data["order"] = 1
    elif mutation == "bad-lessons":
        data["lessons"][0]["id"] = "l99"
    elif mutation == "alias-collision":
        data["aliases"] = ["hands-on-with-cursor"]
    else:
        data["pro"] = True
    path.write_text(json.dumps(data))
    with pytest.raises((ValueError, ValidationError)):
        build_registry(repo)


def test_verifier_is_parsed_never_executed(tmp_path):
    path = tmp_path / "verify.py"
    path.write_text('raise RuntimeError("must not execute")\nCOURSE_ID="course-c"\nCOURSE_SALT="0123456789abcdef"\nCHECKPOINTS=[{"id":"l01","gate":"attest"}]\n')
    assert verifier_contract(path)["gated"] == []
    path.write_text('COURSE_ID = __import__("os").getcwd()')
    with pytest.raises(ValueError):
        verifier_contract(path)


def test_unknown_gate_and_duplicate_checkpoints_rejected(tmp_path):
    checkpoints = [{"id": "l01", "gate": "attest"}]
    for values in [checkpoints * 2, [{**copy.copy(checkpoints[0]), "gate": "unknown"}]]:
        path = tmp_path / "verify.py"
        path.write_text(f'COURSE_ID="course-c"\nCOURSE_SALT="0123456789abcdef"\nCHECKPOINTS={values!r}')
        with pytest.raises(ValueError):
            verifier_contract(path)
