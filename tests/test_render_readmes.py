from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from tools.catalog import load_catalog
from tools.render_readmes import (
    END_MARKER,
    START_MARKER,
    render_catalog_index,
    replace_generated_block,
    run,
)

ROOT = Path(__file__).resolve().parents[1]


def test_checked_in_readme_catalog_sections_are_current() -> None:
    assert run(["--check"]) == 0


def test_readmes_expose_every_catalog_resource() -> None:
    catalog = load_catalog(ROOT / "catalog")
    english = (ROOT / "README.md").read_text(encoding="utf-8")
    chinese = (ROOT / "README_cn.md").read_text(encoding="utf-8")

    for resource in catalog["resources"]:
        link = f"[{resource['title']}]({resource['url']})"
        assert link in english
        assert link in chinese
        assert resource["why_en"] in english
        assert resource["why_zh"] in chinese


def test_generated_catalog_escapes_markdown_and_html(valid_catalog: dict) -> None:
    data = deepcopy(valid_catalog)
    data["resources"][0]["title"] = "Unsafe ] <script> | title"
    data["resources"][0]["why_en"] = "A | B <script>alert(1)</script>"

    rendered = render_catalog_index(data, lang="en")

    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
    assert "\\|" in rendered


def test_generated_block_requires_exactly_one_marker_pair() -> None:
    with pytest.raises(ValueError, match="exactly one"):
        replace_generated_block("missing markers", "generated")

    content = f"before\n{START_MARKER}\nold\n{END_MARKER}\nafter\n"
    generated = f"{START_MARKER}\nnew\n{END_MARKER}"
    expected = "before\n" + generated + "\nafter\n"
    assert replace_generated_block(content, generated) == expected


def test_renderer_rejects_unknown_language(valid_catalog: dict) -> None:
    with pytest.raises(ValueError, match="lang"):
        render_catalog_index(valid_catalog, lang="fr")
