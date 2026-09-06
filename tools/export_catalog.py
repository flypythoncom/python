#!/usr/bin/env python3
"""Build the deterministic JSON catalog consumed by flypython.com."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from datetime import date, datetime
from pathlib import Path
from typing import Any

try:
    from tools.catalog import CatalogLoadError, load_catalog, validate_catalog
except ModuleNotFoundError:  # Direct ``python tools/export_catalog.py`` execution.
    from catalog import CatalogLoadError, load_catalog, validate_catalog


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = ROOT_DIR / "catalog"
DEFAULT_OUTPUT = ROOT_DIR / "catalog.json"


def _json_ready(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    return value


def build_export(data: Mapping[str, Any]) -> dict[str, Any]:
    metadata = data["catalog"]
    return {
        "$schema": "./schema/catalog-v1.schema.json",
        "schema_version": 1,
        "catalog": {
            "reviewed_on": _json_ready(metadata["reviewed_on"]),
            "status": metadata["status"],
        },
        "paths": _json_ready(metadata["paths"]),
        "resources": _json_ready(data["resources"]),
    }


def render_export(data: Mapping[str, Any]) -> str:
    return json.dumps(build_export(data), ensure_ascii=False, indent=2) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail when the checked-in JSON export is missing or out of date",
    )
    parser.add_argument(
        "--stdout", action="store_true", help="write the export to standard output"
    )
    return parser


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        data = load_catalog(args.catalog)
    except CatalogLoadError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    issues = validate_catalog(data)
    if issues:
        for issue in issues:
            print(
                f"{issue.location}: {issue.code}: {issue.message}", file=sys.stderr
            )
        return 1

    rendered = render_export(data)
    if args.stdout:
        print(rendered, end="")
        return 0

    if args.check:
        try:
            current = args.output.read_text(encoding="utf-8")
        except OSError:
            print(f"catalog export is missing: {args.output}", file=sys.stderr)
            return 1
        if current != rendered:
            print(
                f"catalog export is out of date: run {Path(__file__).name}",
                file=sys.stderr,
            )
            return 1
        print(f"catalog export current: {args.output}")
        return 0

    args.output.write_text(rendered, encoding="utf-8")
    print(f"wrote {len(data['resources'])} resources to {args.output}")
    return 0


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
