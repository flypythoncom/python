"""Scenario report tool (reviewed solution).

Reads a scenario data file (CSV or JSON), isolates invalid rows instead of
crashing, aggregates valid rows per group with two-decimal rounding, and
writes the report atomically so an interrupted run never leaves a half-written
file. Standard library only.
"""

from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

SUPPORTED_SUFFIXES = {".csv", ".json"}


def load_records(path: str | Path) -> list[dict]:
    """Load CSV or JSON records from *path* as a list of dicts."""
    source = Path(path)
    suffix = source.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(f"unsupported data file type: {source.name}")
    if suffix == ".csv":
        with source.open("r", encoding="utf-8", newline="") as handle:
            records = list(csv.DictReader(handle))
    else:
        data = json.loads(source.read_text(encoding="utf-8"))
        records = data if isinstance(data, list) else None
    if not all(isinstance(record, dict) for record in records):
        raise ValueError("data file must contain a list of objects")
    return records


def _field_text(record: dict, field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str):
        return "" if value is None else str(value).strip()
    return value.strip()


def build_report(
    records: list[dict],
    *,
    required_fields: list[str],
    numeric_field: str,
    group_field: str,
) -> dict:
    """Aggregate *records*, isolating invalid rows with recorded reasons."""
    groups: dict[str, dict] = {}
    errors: list[dict] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append({"index": index, "reason": "record is not an object"})
            continue
        missing = [
            field for field in required_fields if not _field_text(record, field)
        ]
        if missing:
            errors.append(
                {"index": index, "reason": f"missing required field: {missing[0]}"}
            )
            continue
        raw_number = _field_text(record, numeric_field)
        try:
            number = float(raw_number)
        except ValueError:
            errors.append(
                {
                    "index": index,
                    "reason": f"field {numeric_field!r} is not a number: {raw_number!r}",
                }
            )
            continue
        group = _field_text(record, group_field)
        bucket = groups.setdefault(group, {"count": 0, "total": 0.0})
        bucket["count"] += 1
        bucket["total"] = round(bucket["total"] + number, 2)
    return {
        "total": len(records),
        "valid": len(records) - len(errors),
        "invalid": len(errors),
        "groups": groups,
        "errors": errors,
    }


def write_report(report: dict, destination: str | Path) -> None:
    """Atomically write *report* as JSON, creating parent directories."""
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp")
    temporary.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, target)


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
    try:
        report = run_scenario(arguments[0])
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(
        f"total={report['total']} valid={report['valid']} invalid={report['invalid']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
