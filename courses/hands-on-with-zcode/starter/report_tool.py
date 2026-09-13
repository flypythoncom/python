"""Scenario report tool (starter, deliberately incomplete).

Reads a scenario data file, aggregates valid rows, and writes a JSON report.
This starter reproduces the classic "it runs on the happy path" state of an
AI-written script: JSON inputs crash, invalid rows abort the run, group totals
carry floating-point noise, and reports cannot be written into a fresh
directory. The task contract in ../TASK.md defines the expected behavior.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


def load_records(path: str | Path) -> list[dict]:
    """Load CSV or JSON records from *path* as a list of dicts."""
    source = Path(path)
    with source.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_report(
    records: list[dict],
    *,
    required_fields: list[str],
    numeric_field: str,
    group_field: str,
) -> dict:
    """Aggregate *records* into a summary report."""
    groups: dict[str, dict] = {}
    for record in records:
        for field in required_fields:
            value = (record.get(field) or "").strip()
            if not value:
                raise KeyError(f"missing required field: {field}")
        group = record[group_field].strip()
        bucket = groups.setdefault(group, {"count": 0, "total": 0.0})
        bucket["count"] += 1
        bucket["total"] += float(record[numeric_field])
    return {
        "total": len(records),
        "valid": len(records),
        "invalid": 0,
        "groups": groups,
        "errors": [],
    }


def write_report(report: dict, destination: str | Path) -> None:
    """Write *report* as JSON to *destination*."""
    Path(destination).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def run_scenario(scenario_dir: str | Path) -> dict:
    """Load scenario.json, process its data file, and write the report."""
    directory = Path(scenario_dir)
    config = json.loads((directory / "scenario.json").read_text(encoding="utf-8"))
    records = load_records(directory / config["data_file"])
    report = build_report(
        records,
        required_fields=config["required_fields"],
        numeric_field=config["numeric_field"],
        group_field=config["group_field"],
    )
    write_report(report, directory / config["report_file"])
    return report


def main(argv: list[str] | None = None) -> int:
    """Run one scenario directory and print a one-line summary."""
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        print("usage: python report_tool.py <scenario-dir>", file=sys.stderr)
        return 2
    report = run_scenario(arguments[0])
    print(
        f"total={report['total']} valid={report['valid']} invalid={report['invalid']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
