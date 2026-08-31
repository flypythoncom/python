#!/usr/bin/env python3
"""Validate the canonical FlyPython resource catalog."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from tools.catalog import CatalogLoadError, load_catalog, validate_catalog
except ModuleNotFoundError:  # Direct ``python tools/validate_catalog.py`` execution.
    from catalog import CatalogLoadError, load_catalog, validate_catalog


ROOT_DIR = Path(__file__).resolve().parent.parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog", type=Path, default=ROOT_DIR / "_data" / "resources.yml"
    )
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    parser.add_argument("--max-review-age-days", type=int, default=366)
    return parser


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.max_review_age_days < 1:
        print("--max-review-age-days must be positive", file=sys.stderr)
        return 2
    try:
        data = load_catalog(args.catalog)
    except CatalogLoadError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    issues = validate_catalog(data, max_review_age_days=args.max_review_age_days)
    report = {
        "catalog": str(args.catalog),
        "valid": not issues,
        "issue_count": len(issues),
        "issues": [issue.as_dict() for issue in issues],
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    if issues:
        for issue in issues:
            print(
                f"{issue.location}: {issue.code}: {issue.message}", file=sys.stderr
            )
        return 1
    print(f"catalog valid: {len(data.get('resources', []))} resources")
    return 0


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
