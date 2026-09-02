from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from tools.content_manifest import build_manifest


ROOT = Path(__file__).resolve().parents[1]


def test_content_manifest_matches_sources_and_schema() -> None:
    generated = build_manifest(ROOT)
    committed = json.loads((ROOT / "content-manifest.json").read_text(encoding="utf-8"))
    schema = json.loads(
        (ROOT / "schema" / "content-manifest-v1.schema.json").read_text(encoding="utf-8")
    )

    assert committed == generated
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(committed)


def test_each_document_has_a_unique_bilingual_pair() -> None:
    manifest = build_manifest(ROOT)
    assert manifest["documents"]
    assert len({item["id"] for item in manifest["documents"]}) == len(manifest["documents"])
    for item in manifest["documents"]:
        assert [locale["lang"] for locale in item["locales"]] == ["en-US", "zh-CN"]
