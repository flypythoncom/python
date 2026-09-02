# Contributing to the FlyPython catalog

FlyPython maintains a bilingual, reviewed source catalog used by
[flypython.com](https://flypython.com/). Contributions should improve source
quality, factual accuracy, or the maintenance workflow. General Python questions
belong in [GitHub Discussions](https://github.com/flypythoncom/python/discussions).

Read the [curation policy](docs/CURATION_POLICY.md) before contributing.

## Permissions

This repository currently does not grant a general license to reuse its content
or code. Public visibility is not permission to copy, redistribute, or relicense
repository material. Contributors must submit only material they have the right
to submit and retain required third-party notices.

## Propose a change

Use the matching issue form before a larger change:

- **Resource proposal** for a new official source.
- **Broken link** for an unreachable or replaced resource.
- **Security report** for a vulnerability; follow [SECURITY.md](SECURITY.md)
  instead of opening a public issue.

Small typo, metadata, or tooling fixes may go directly to a focused pull request.

## Catalog sources

The canonical source is the `catalog/` directory:

- `catalog/catalog.yml` contains catalog-level review state.
- `catalog/paths.yml` defines the four bilingual learning paths.
- `catalog/resources/<id>.yml` contains one reviewed resource.
- `catalog.json` is generated output and must not be edited by hand.

Every resource file must include:

- `id`, `path`, `order`, `title`, and `url`
- `source_type`, `level`, and `language`
- `why_en` and `why_zh`
- `reviewed_on` and `status`
- `requires_key`, `risk`, and `featured`

The filename must match the stable resource ID. Resource `order` values must be
unique and consecutive within each path.

Descriptions and classifications require human review. Do not use an LLM or a
web-search API to generate them. Prefer official documentation, official
standards, and official project pages.

A 403, 429, timeout, or transient 5xx response is not enough to delete a
resource. Mark it for human review and provide repeatable evidence.

## Local setup

Install the exact Python version from `.python-version` and the locked
development dependencies:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.lock.txt
```

After changing catalog sources, regenerate the public export:

```bash
python tools/export_catalog.py
```

Run the same deterministic checks as CI:

```bash
python -m pytest
python tools/validate_catalog.py
python tools/export_catalog.py --check
```

Maintainers can run the networked link audit through GitHub Actions. For a
deliberate local audit of every catalog entry:

```bash
python tools/check_links.py --mode all --output reports/link-check.json
```

Network fetching is excluded from pull-request CI. Any review-needed result
fails the scheduled audit for maintainer inspection, but does not by itself
justify removing a resource.

## Pull request checklist

- Keep source data and the generated `catalog.json` consistent.
- Preserve English and Chinese meaning.
- Include evidence for maintenance, ownership, access, and safety claims.
- Do not call a project production-ready without current evidence.
- Do not commit secrets, generated reports, caches, or local environments.
- Explain consumer-visible changes and list the validation results.

Passing automation does not replace editorial review. After merge, a website
consumer must deliberately update its pinned catalog commit before the new data
appears on flypython.com.
