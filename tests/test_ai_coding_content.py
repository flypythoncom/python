from __future__ import annotations

import re
from pathlib import Path

import yaml

from tools.catalog import load_catalog


ROOT = Path(__file__).resolve().parents[1]
GUIDES = {
    "en-US": ROOT / "guides" / "ai-coding" / "workflow.md",
    "zh-CN": ROOT / "guides" / "ai-coding" / "workflow_cn.md",
}


def load_guide(path: Path) -> tuple[dict, str]:
    content = path.read_text(encoding="utf-8")
    assert content.startswith("---\n")
    _, front_matter, body = content.split("---\n", maxsplit=2)
    return yaml.safe_load(front_matter), body


def test_ai_coding_guides_have_matching_identity_and_version() -> None:
    loaded = {lang: load_guide(path) for lang, path in GUIDES.items()}
    english, _ = loaded["en-US"]
    chinese, _ = loaded["zh-CN"]

    assert english["id"] == chinese["id"] == "python-ai-coding-workflow"
    assert english["content_version"] == chinese["content_version"] == 1
    assert english["reviewed_on"] == chinese["reviewed_on"]
    assert english["lang"] == "en-US"
    assert chinese["lang"] == "zh-CN"


def test_ai_coding_guides_cover_the_same_eight_step_workflow() -> None:
    for path in GUIDES.values():
        _, body = load_guide(path)
        headings = re.findall(r"^## ([1-8])\.", body, flags=re.MULTILINE)
        assert headings == [str(number) for number in range(1, 9)]


def test_guide_reference_urls_come_from_reviewed_catalog() -> None:
    catalog = load_catalog(ROOT / "catalog")
    catalog_urls = {resource["url"] for resource in catalog["resources"]}

    for path in GUIDES.values():
        _, body = load_guide(path)
        urls = set(re.findall(r"\]\((https://[^)]+)\)", body))
        assert urls
        assert urls <= catalog_urls


def test_readmes_link_to_the_matching_ai_coding_guide() -> None:
    english = (ROOT / "README.md").read_text(encoding="utf-8")
    chinese = (ROOT / "README_cn.md").read_text(encoding="utf-8")

    assert "guides/ai-coding/workflow.md" in english
    assert "guides/ai-coding/workflow_cn.md" in chinese
