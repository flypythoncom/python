from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from tools.catalog import load_catalog
from tools.content_manifest import build_manifest

ROOT = Path(__file__).resolve().parents[1]


def _extract_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} must start with frontmatter"
    parts = text.split("---\n", maxsplit=2)
    return yaml.safe_load(parts[1])


def test_content_manifest_builds_without_errors() -> None:
    manifest = build_manifest(ROOT)
    assert manifest["schema_version"] == 1
    assert len(manifest["documents"]) >= 10


def test_bilingual_guide_urls_are_in_catalog() -> None:
    catalog = load_catalog(ROOT / "catalog")
    catalog_urls = {resource["url"] for resource in catalog["resources"]}

    for guide_path in ROOT.glob("guides/**/*.md"):
        if guide_path.name == "README.md" or guide_path.name == "README_cn.md":
            continue
        text = guide_path.read_text(encoding="utf-8")
        external_urls = set(re.findall(r"\]\((https://[^)]+)\)", text))
        for url in external_urls:
            assert url in catalog_urls, (
                f"Guide {guide_path.relative_to(ROOT)} references unreviewed URL: {url}"
            )
