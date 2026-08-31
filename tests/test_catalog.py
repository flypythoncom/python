from __future__ import annotations

from copy import deepcopy
from datetime import date

import pytest

from tools.catalog import (
    CatalogLoadError,
    load_catalog,
    normalize_url,
    validate_catalog,
)
from tools.validate_catalog import run


def test_valid_catalog_passes(valid_catalog: dict) -> None:
    assert validate_catalog(valid_catalog, today=date(2026, 8, 31)) == []


@pytest.mark.parametrize("language", ["en", "zh", "multilingual"])
def test_supported_language_values_pass(valid_catalog: dict, language: str) -> None:
    data = deepcopy(valid_catalog)
    data["resources"][0]["language"] = language
    assert validate_catalog(data, today=date(2026, 8, 31)) == []


def test_loader_rejects_duplicate_yaml_keys(tmp_path) -> None:
    catalog = tmp_path / "resources.yml"
    catalog.write_text("catalog: {}\ncatalog: {}\nresources: []\n", encoding="utf-8")
    with pytest.raises(CatalogLoadError, match="duplicate key"):
        load_catalog(catalog)


def test_schema_duplicate_https_date_and_parity_errors(valid_catalog: dict) -> None:
    data = deepcopy(valid_catalog)
    data["resources"][0]["url"] = "http://example.invalid/docs"
    data["resources"][1]["url"] = "https://example.invalid/docs/"
    data["resources"][2]["url"] = "https://example.invalid/docs"
    data["resources"][2]["reviewed_on"] = "2025-01-01"
    data["resources"][3]["why_zh"] = ""
    issues = validate_catalog(data, today=date(2026, 8, 31), max_review_age_days=366)
    codes = {issue.code for issue in issues}
    assert {"https-required", "duplicate-url", "stale-review", "invalid-text"} <= codes


def test_resource_ids_and_urls_reject_unsafe_forms(valid_catalog: dict) -> None:
    data = deepcopy(valid_catalog)
    data["resources"][0]["id"] = "Not A Slug"
    data["resources"][0]["url"] = "https://user:secret@example.com/docs"
    codes = {
        issue.code for issue in validate_catalog(data, today=date(2026, 8, 31))
    }
    assert {"invalid-id", "url-credentials"} <= codes


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (
            "HTTPS://[2001:4860:4860::8888]:443/docs/",
            "https://[2001:4860:4860::8888]/docs",
        ),
        (
            "https://[2001:4860:4860::8888]:8443/docs/",
            "https://[2001:4860:4860::8888]:8443/docs",
        ),
    ],
)
def test_normalize_url_preserves_ipv6_brackets(url: str, expected: str) -> None:
    assert normalize_url(url) == expected


def test_validator_exit_code_for_invalid_catalog(tmp_path) -> None:
    catalog = tmp_path / "resources.yml"
    catalog.write_text("catalog: {}\nresources: []\n", encoding="utf-8")
    assert run(["--catalog", str(catalog)]) == 1
