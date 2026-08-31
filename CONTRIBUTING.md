# Contributing to FlyPython

FlyPython is a bilingual, reviewed catalog of durable Python and AI-agent
resources. Contributions should improve accuracy, source quality, or the
catalog workflow. General Python questions belong in
[GitHub Discussions](https://github.com/flypythoncom/python/discussions).

Before contributing, read the [curation policy](docs/CURATION_POLICY.md).

## Permissions

This repository currently does not grant a general license to reuse its
content or code. Public visibility is not permission to copy, redistribute,
or relicense repository material. Contributors must submit only material
they have the right to submit and must preserve any required third-party
notices. A contribution does not change the terms of third-party material.

## Propose a change

Use the matching issue form before a larger change:

- **Resource proposal** for a new catalog entry.
- **Broken link** for an unreachable or replaced resource.
- **Security report** for a vulnerability. Follow [SECURITY.md](SECURITY.md)
  instead of opening a public issue.

Small typo, metadata, or maintenance fixes may go directly to a pull request.
Keep each pull request focused on one purpose.

## Catalog changes

`_data/resources.yml` is the canonical catalog source. Do not add or change a
resource only in a rendered Markdown page.

Each resource entry must include these fields:

- `id`, `path`, `title`, and `url`
- `source_type`, `level`, and `language`
- `why_en` and `why_zh`
- `reviewed_on` and `status`
- `requires_key`, `risk`, and `featured`

Descriptions and classifications require human review. Do not use an LLM or a
web-search API to generate them. Prefer official documentation, official
standards, and official project pages.

A 403, 429, or transient 5xx response is not enough to delete a resource. Mark
it for review and provide repeatable evidence.

## Local setup

Install the exact Python version from `.python-version`, Ruby, Bundler, and the
repository dependencies:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.lock.txt
bundle install
```

## Required validation

Run the same checks as CI before requesting review:

```bash
python -m pytest
python tools/validate_catalog.py
bundle exec jekyll build
```

Maintainers can run the networked link audit from GitHub Actions with the
scheduled **External link audit** workflow. For a deliberate local audit:

```bash
python tools/check_links.py --mode external --output reports/link-check.json
```

External-link fetching is intentionally excluded from pull-request CI. A pull
request can contain untrusted URLs, and status checks must remain deterministic.

## Pull request checklist

- Keep catalog data and bilingual output consistent.
- Include evidence for maintenance, license, safety, and adoption claims.
- Do not call a project production-ready without current evidence.
- Do not commit secrets, API keys, analytics IDs, generated reports, or local
  build output.
- Submit only material you have the right to submit and retain any required
  third-party notice.
- Explain user-visible changes and list the commands you ran.

## Review and merge

Maintainers may request edits, reclassify an entry, or decline resources that
do not meet the curation policy. Passing automated checks does not replace
editorial review. After merge, maintainers verify the GitHub Pages deployment
and the production domain.
