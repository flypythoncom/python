# FlyPython Python Catalog

[![GitHub stars](https://img.shields.io/github/stars/flypythoncom/python?style=flat-square&label=stars)](https://github.com/flypythoncom/python/stargazers)
[![Validate](https://github.com/flypythoncom/python/actions/workflows/validate.yml/badge.svg)](https://github.com/flypythoncom/python/actions/workflows/validate.yml)

[English](README.md) · [中文](README_cn.md)

This repository is the reviewed data source behind Python resources shown on
[flypython.com](https://flypython.com/). It is not a second website and does not
contain a site renderer, theme, or deployment configuration.

## What belongs here

- Canonical links to official documentation, standards, and project sources.
- Human-reviewed English and Chinese rationales.
- Learning-path, level, access, review-date, and safety metadata.
- Deterministic validation, JSON export, and safe link-audit tooling.
- Public contribution and curation rules.

The main website owns learning guides, task playbooks, navigation, and visual
presentation. This repository owns the broader catalog and its evidence-backed
maintenance workflow.

## Repository structure

```text
catalog/
  catalog.yml        catalog status and review date
  paths.yml          bilingual learning-path definitions
  resources/         one reviewed resource per YAML file
schema/
  catalog-v1.schema.json
catalog.json         deterministic public export for consumers
tools/               validation, export, and link-audit commands
tests/               catalog and network-safety tests
docs/                curation policy
```

`catalog.json` is generated from `catalog/`; do not edit it by hand. Consumer
repositories should read the export from a pinned commit, verify its checksum,
and record that revision in their own lock file. They should not fetch a moving
`master` branch during a production build.

Example immutable URL:

```text
https://raw.githubusercontent.com/flypythoncom/python/<full-commit-sha>/catalog.json
```

The export intentionally includes the bilingual path summaries and resource
rationales that flypython.com may render. Editorial guides and task-specific
playbooks remain in the website repository.

## Validate a change

Use the Python version declared in `.python-version`, then install the locked
development dependencies:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.lock.txt
```

Run the deterministic checks:

```bash
python -m pytest
python tools/validate_catalog.py
python tools/export_catalog.py --check
```

After changing catalog sources, regenerate the public export before running the
checks:

```bash
python tools/export_catalog.py
```

Network link fetching is intentionally excluded from pull-request validation.
Maintainers run it through the scheduled or manual **Catalog link audit**
workflow.

Read [CONTRIBUTING.md](CONTRIBUTING.md) and the
[curation policy](docs/CURATION_POLICY.md) before proposing a resource or
changing its classification. Website integrations should also follow the
[consumer contract](docs/CONSUMING.md).
