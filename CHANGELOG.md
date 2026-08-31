# Changelog

This file records notable repository and catalog-process changes. The Git
history remains the source for changes made before this changelog was added.

## [Unreleased]

### Added

- A single bilingual catalog source with 21 reviewed primary resources across
  Python foundations, web and APIs, automation, and AI-agent paths.
- Catalog schema validation and a safe external-link auditor with tests,
  retry/backoff behavior, JSON reports, and SSRF/DNS-rebinding protection.
- English and Chinese catalog pages generated from the same resource data,
  plus a 1200x630 social preview image.
- Contribution, conduct, security, and resource-curation policies.
- Structured issue forms and a pull request review checklist.
- Dependency update configuration and validation workflows.
- Scheduled, manually dispatchable external-link auditing that does not run on
  untrusted pull requests.

### Changed

- Reframed the repository as the broad, community-maintained catalog behind
  FlyPython while keeping the README files as short entry points.
- Pinned the Python 3.12 and Ruby 3.3 build toolchains and their validation
  dependencies for reproducible local and CI checks.

### Fixed

- Corrected repository links, dynamic resource counts, bilingual metadata,
  canonical and hreflang output, robots rules, and duplicate heading/meta tags.

### Removed

- Removed the legacy `README_cn` site route without adding a redirect, along
  with unused feed, navigation, collection, theme, and inline-style config.
