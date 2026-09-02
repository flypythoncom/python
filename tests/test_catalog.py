from __future__ import annotations

from copy import deepcopy
from datetime import date
from pathlib import Path

import pytest
import yaml

from tools.catalog import (
    CatalogLoadError,
    canonical_hostname,
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


def test_loader_rejects_non_string_mapping_keys(tmp_path) -> None:
    catalog = tmp_path / "resources.yml"
    catalog.write_text("? [catalog]\n: {}\nresources: []\n", encoding="utf-8")
    with pytest.raises(CatalogLoadError, match="mapping keys must be strings"):
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


def test_path_orders_must_be_consecutive(valid_catalog: dict) -> None:
    data = deepcopy(valid_catalog)
    data["catalog"]["paths"][-1]["order"] = 5

    codes = {
        issue.code for issue in validate_catalog(data, today=date(2026, 8, 31))
    }

    assert "order-parity" in codes


def test_resource_orders_must_be_unique_and_consecutive(valid_catalog: dict) -> None:
    data = deepcopy(valid_catalog)
    duplicate = deepcopy(data["resources"][0])
    duplicate["id"] = "another-foundation-resource"
    duplicate["url"] = "https://another.example.com/docs/"
    data["resources"].append(duplicate)

    codes = {
        issue.code for issue in validate_catalog(data, today=date(2026, 8, 31))
    }

    assert {"duplicate-resource-order", "resource-order-parity"} <= codes


def test_directory_loader_composes_catalog_sources(
    tmp_path: Path, valid_catalog: dict
) -> None:
    catalog_dir = tmp_path / "catalog"
    resources_dir = catalog_dir / "resources"
    resources_dir.mkdir(parents=True)
    metadata = {
        "reviewed_on": valid_catalog["catalog"]["reviewed_on"],
        "status": valid_catalog["catalog"]["status"],
    }
    (catalog_dir / "catalog.yml").write_text(
        yaml.safe_dump(metadata, sort_keys=False), encoding="utf-8"
    )
    (catalog_dir / "paths.yml").write_text(
        yaml.safe_dump(valid_catalog["catalog"]["paths"], sort_keys=False),
        encoding="utf-8",
    )
    for resource in reversed(valid_catalog["resources"]):
        (resources_dir / f"{resource['id']}.yml").write_text(
            yaml.safe_dump(resource, sort_keys=False), encoding="utf-8"
        )

    loaded = load_catalog(catalog_dir)

    assert loaded == valid_catalog


def test_directory_loader_requires_resource_id_to_match_filename(
    tmp_path: Path, valid_catalog: dict
) -> None:
    catalog_dir = tmp_path / "catalog"
    resources_dir = catalog_dir / "resources"
    resources_dir.mkdir(parents=True)
    (catalog_dir / "catalog.yml").write_text(
        "reviewed_on: 2026-08-31\nstatus: active\n", encoding="utf-8"
    )
    (catalog_dir / "paths.yml").write_text("[]\n", encoding="utf-8")
    (resources_dir / "wrong-name.yml").write_text(
        yaml.safe_dump(valid_catalog["resources"][0], sort_keys=False),
        encoding="utf-8",
    )

    with pytest.raises(CatalogLoadError, match="resource id must match filename"):
        load_catalog(catalog_dir)


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


def test_hostname_canonicalization_handles_idna_and_trailing_dot() -> None:
    assert canonical_hostname("BÜCHER.example.") == "xn--bcher-kva.example"


def test_validator_detects_idna_equivalent_duplicate_urls(valid_catalog: dict) -> None:
    data = deepcopy(valid_catalog)
    data["resources"][0]["url"] = "https://bücher.example/docs/"
    data["resources"][1]["url"] = "https://xn--bcher-kva.example/docs"

    codes = {
        issue.code for issue in validate_catalog(data, today=date(2026, 8, 31))
    }

    assert "duplicate-url" in codes


def test_validator_reports_non_string_mapping_keys(valid_catalog: dict) -> None:
    data = deepcopy(valid_catalog)
    data["catalog"][1] = "unexpected"

    issues = validate_catalog(data, today=date(2026, 8, 31))

    assert any(issue.code == "invalid-key" for issue in issues)


def test_validator_exit_code_for_invalid_catalog(tmp_path) -> None:
    catalog = tmp_path / "resources.yml"
    catalog.write_text("catalog: {}\nresources: []\n", encoding="utf-8")
    assert run(["--catalog", str(catalog)]) == 1
