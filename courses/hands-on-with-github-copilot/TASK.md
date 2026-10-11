# Task contract: scenario report tool (hands-on course core)

Change only `starter/report_tool.py`. Standard library only; no new
dependencies.

- `load_records(path) -> list[dict]`:
  - `.csv` files load through `csv.DictReader`.
  - `.json` files load as a list of objects; a non-list or non-object payload
    raises `ValueError`.
  - Any other suffix raises `ValueError` naming the unsupported file.
- `build_report(records, *, required_fields, numeric_field, group_field) -> dict`:
  - Returns `{"total", "valid", "invalid", "groups", "errors"}`.
  - Invalid rows never abort the run: each is collected in `errors` as
    `{"index": <row position>, "reason": <short string>}`. Invalid means:
    not a dict, missing or blank required field, or a non-numeric
    `numeric_field` value (booleans do not count as numbers).
  - Valid rows aggregate into `groups[group_value] = {"count": int,
    "total": float}`; each group total is rounded to two decimals.
  - `total = valid + invalid` must hold for every input.
- `write_report(report, destination)`:
  - Writes JSON (UTF-8, indent 2, trailing newline) atomically: write a
    sibling temp file, then `os.replace`.
  - Creates missing parent directories.
  - Never leaves a `.tmp` file behind on success.
- `run_scenario(scenario_dir) -> dict`:
  - Reads `scenario.json` (`data_file`, `required_fields`, `numeric_field`,
    `group_field`, `report_file`), processes the data file, writes the
    report inside the scenario directory, and returns the report.
- `main(argv=None) -> int`:
  - Exactly one argument (the scenario directory). Otherwise print usage to
    stderr and return 2.
  - On success print `total=... valid=... invalid=...` to stdout and return 0.
  - On input failure print `error: ...` to stderr and return 1.

Done means `python verify.py starter` exits 0 with all nine tests passing,
and `python verify.py starter --expect-failure` exits nonzero because the
starter no longer reproduces the unfinished state.
