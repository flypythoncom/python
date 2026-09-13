from __future__ import annotations

from pathlib import Path

from tools.content_manifest import build_manifest
from tools.verify_courses import check_bilingual_contract, discover_courses

ROOT = Path(__file__).resolve().parents[1]


def test_courses_directory_is_discovered() -> None:
    courses = discover_courses(ROOT)
    names = {course.name for course in courses}
    assert {
        "hands-on-python-with-claude-code",
        "hands-on-with-openai-codex",
        "hands-on-with-cursor",
        "hands-on-with-deepseek-harness",
        "hands-on-with-kimi-code",
        "hands-on-with-zcode",
        "agent-rules-single-source",
        "verifying-ai-generated-code",
        "mcp-server-in-python",
    } <= names


def test_course_folders_satisfy_the_bilingual_contract() -> None:
    for course in discover_courses(ROOT):
        assert check_bilingual_contract(course) == []


def test_missing_chinese_pair_is_reported(tmp_path: Path) -> None:
    course = tmp_path / "demo-course"
    (course / "lessons").mkdir(parents=True)
    (course / "lessons" / "L01.md").write_text("# L01\n", encoding="utf-8")
    problems = check_bilingual_contract(course)
    assert any("without _cn.md pair: L01" in problem for problem in problems)


def test_orphan_chinese_lesson_is_reported(tmp_path: Path) -> None:
    course = tmp_path / "demo-course"
    (course / "lessons").mkdir(parents=True)
    (course / "lessons" / "L01.md").write_text("# L01\n", encoding="utf-8")
    (course / "lessons" / "L01_cn.md").write_text("# L01\n", encoding="utf-8")
    (course / "lessons" / "L02_cn.md").write_text("# L02\n", encoding="utf-8")
    problems = check_bilingual_contract(course)
    assert any("without English pair: L02" in problem for problem in problems)


def test_course_documents_enter_the_content_manifest() -> None:
    manifest = build_manifest(ROOT)
    course_documents = [
        document
        for document in manifest["documents"]
        if document["type"] == "course"
    ]
    ids = {document["id"] for document in course_documents}
    expected_courses = {
        "course-claude-code",
        "course-codex-cli",
        "course-cursor",
        "course-deepseek-harness",
        "course-kimi-code",
        "course-zcode",
        "course-agent-rules",
        "course-verify-ship",
        "course-mcp-tools",
    }
    assert expected_courses <= ids
    for prefix in expected_courses:
        for lesson in range(1, 6):
            assert f"{prefix}-l0{lesson}" in ids
    for document in course_documents:
        langs = {locale["lang"] for locale in document["locales"]}
        assert langs == {"en-US", "zh-CN"}


def test_course_manifest_schema_allows_course_type() -> None:
    import json

    schema = json.loads(
        (ROOT / "schema" / "content-manifest-v1.schema.json").read_text(
            encoding="utf-8"
        )
    )
    enum = schema["properties"]["documents"]["items"]["properties"]["type"][
        "enum"
    ]
    assert "course" in enum
