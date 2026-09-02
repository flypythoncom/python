# Changelog

This file records notable catalog-contract and maintenance changes.

## [Unreleased]

### Added

- One source file per reviewed resource under `catalog/resources/`.
- A deterministic, versioned `catalog.json` export for pinned website consumers.
- A JSON Schema describing the public catalog v1 contract.
- A pinned-revision and checksum contract for website consumers.
- Export drift checks in tests and pull-request validation.
- Positive, unique, consecutive ordering within each learning path.
- Catalog validation and a safe external-link auditor with retry, report, and
  SSRF/DNS-rebinding protection.
- Contribution, conduct, security, issue, and resource-curation policies.

### Changed

- Defined this repository as the canonical catalog-data and review layer behind
  flypython.com, rather than a second public website.
- Split catalog metadata, paths, and resources into independently reviewable
  files while preserving the 21 existing human-reviewed resource records.
- Required website consumers to pin a full repository commit and verify the
  exported catalog checksum instead of following a moving branch.
- Reduced the required local toolchain to Python 3.12 and locked Python
  dependencies.

### Removed

- Removed Jekyll, Ruby, page templates, styles, scripts, social assets, CNAME,
  robots configuration, and site-rendering tests.
