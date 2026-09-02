from __future__ import annotations

import json
from pathlib import Path

from tools.export_catalog import build_export, render_export, run


ROOT = Path(__file__).resolve().parents[1]


def test_export_has_stable_public_contract(valid_catalog: dict) -> None:
    export = build_export(valid_catalog)

    assert export["schema_version"] == 1
    assert export["catalog"] == {
        "reviewed_on": "2026-08-31",
        "status": "active",
    }
    assert export["paths"] == valid_catalog["catalog"]["paths"]
    assert export["resources"][0]["reviewed_on"] == "2026-08-31"


def test_checked_in_export_matches_catalog_sources() -> None:
    assert run(["--check"]) == 0


def test_catalog_schema_is_valid_json() -> None:
    schema = json.loads(
        (ROOT / "schema" / "catalog-v1.schema.json").read_text(encoding="utf-8")
    )

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["properties"]["schema_version"]["const"] == 1


def test_render_export_is_deterministic(valid_catalog: dict) -> None:
    assert render_export(valid_catalog) == render_export(valid_catalog)
