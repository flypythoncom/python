# Changelog

This file records notable catalog-contract and maintenance changes.

## [Unreleased]

0.1.0 — companion-repository half of the public launch (website
`docs/product-and-growth-plan-0.1.0.md`; see the website `CHANGELOG.md`
for the platform half).

Release mapping (FP-1012): this repository ships **v0.1.1** on this
release train — the earlier `v0.1.0` tag stays immutably on `e420fca`.
Compatibility: website `v0.1.0` ↔ repository `v0.1.1`.

### Changed

- FP-1012: `docs/repo-plan-0.1.0.md` renamed to `docs/repo-plan-0.1.x.md`
  — community courses are a 0.1.x track that starts after 0.1.0 ships,
  not part of the launch version.

0.0.9 — optional entry points (companion-repository half; see the
website plan `docs/product-and-growth-plan-0.0.9.md`).

### Changed

- FP-983: all six agent-tool courses' lesson 1 (EN+ZH) makes the
  FlyPython Skill install step optional-but-recommended, and the named
  failure count is unified as "five categories plus two end-to-end —
  seven named failures" everywhere.
- FP-984: the foundation path's M0 orientation module is optional
  extra credit (`paths/foundation/path.json`, `tools/verify_paths.py`
  badge math updated); the route challenge moved off repository files
  onto the site's `/tracks/<slug>/<module>` pages.

0.0.8 — Skill as the main entry (companion-repository half; see the
website plan `docs/product-and-growth-plan-0.0.8.md`).

### Added

- FP-820: bare `python verify.py` is the learner's default command on
  every course and the data-analysis capstone — runs the suites, prints
  per-checkpoint status and earned claim codes (English first, Chinese
  after), exits non-zero while gated checkpoints are open. The four
  explicit usages remain maintainer checks; the published
  `progress --json` / `--receipt-out` formats are unchanged.
- FP-821: `tools/verify_courses.py` now copies each course folder plus
  the shared `tools/claim_receipt.py` into an isolated tree and runs the
  default command and the receipts contract there — a course fetched via
  the files endpoint verifies alone.

### Changed

- FP-822: the six agent-tool courses' lesson 1 (EN+ZH) is rewritten
  around the fixed order get-the-tool-running → install the FlyPython
  Skill (network access included) → let the agent fetch the course
  files; every "download this folder" wording is gone from `COURSE.md`,
  `COURSE_cn.md`, and the lessons, and `verify.py solution` is no longer
  presented as a completion standard.
- FP-823: the prose checkpoints of `agent-rules-single-source`,
  `mcp-server-in-python`, and `verifying-ai-generated-code` are question
  lists the agent can ask directly at the human-in-the-loop gate;
  data-analysis courses keep their concrete checkpoint criteria and
  frontmatter hint questions.
- FP-824: both READMEs' "Start in three minutes" leads with the Skill
  entry sentence and the six agent-tool courses instead of a clone +
  download flow.

## [Unreleased-0.0.4-phase-A]

0.0.4 phase A — challenge-platform rework on top of 0.1.0.

### Added

- Per-checkpoint claim codes, badge frontmatter contracts, and the
  deterministic `verify.py progress` subcommand (FP-411/412/415), enforced
  by `tools/verify_courses.py`.
- The data-analysis course track: `da-eda`, `da-visualization`, and
  `da-report` (EN+ZH), each with pandas/matplotlib `requirements.txt` where
  needed and a stdlib-only report capstone.
- `paths/` learning paths sequencing courses into badge routes, plus
  `tools/verify_paths.py` enforcing the path contract (FP-413/416/417/418,
  wired into the Makefile and the validation workflow).
- `content-manifest.json` path entries (`type: "path"`) for the website.
- Checkpoint hints, the branch-path contract, and agent-solvability review
  records across all eight courses (2026-09-13).

### Changed

- Repository narrative moved from agent-taught courses to challenge courses
  with `TASK.md` contracts and `verify.py` claim codes; `COURSE.md` remains
  the guided mode. README, README_cn, and `llms.txt` now reflect it.

## [0.1.0] - 2026-09-12

First versioned release: agent-taught courses, the Project Radar
system, and the 0.0.3 contract updates.


### Added

- A `courses/` content type: agent-taught folders with COURSE.md teaching
  contracts, bilingual lesson pairs, scenario skins, task contracts, runnable
  starter/solution pairs, and objective `verify.py` completion evidence.
- The five-course 0.0.3 batch: "Hands-on Python with Claude Code"
  (flagship), "Hands-on with OpenAI Codex CLI" (reuses the C1 core), "One
  source of truth for agent rules" (rule-drift checker core), "From 'it
  runs' to 'it ships'" (release-evidence builder core), and "Give your
  agent tools with MCP" (reuses the reviewed mcp-server contract) — each
  EN+ZH with scenario skins and REVIEW.md run-through records.
- `tools/verify_courses.py` enforcing the course folder contract, wired into
  the Makefile and the validation workflow.
- Project Radar per-project YAML records (`catalog/projects/*.yml`) with
  lifecycle status, maintenance evidence, and `ai_familiarity` grading.
- Deterministic `radar.json` export with `schema/radar-v1.schema.json` and
  `--check` support in `tools/export_catalog.py` (`--target both`).
- Bilingual generated Radar tables in `catalog/projects/README.md` and
  `README_cn.md`.
- `tools/radar_scan.py`: read-only, rate-limited discovery of Radar review
  candidates from GitHub Search, the PyPI feed, and Hacker News — candidates
  only, never descriptions or status.
- A `course-feedback` issue template for teaching drift and verify mismatches.
- `content-manifest.json` and its schema now carry `course` documents.
- Courses and Radar sections in `llms.txt`.

### Changed

- README/README_cn gained a course banner, a courses row, and contextual
  flypython.com footers on every guide, playbook, and example (first-party
  continuation links per `docs/REPO_TO_WEBSITE.md`).
- The validation workflow now verifies the radar export and every course
  folder in addition to the existing gates.
- Bilingual guide-URL tests now allow first-party flypython.com footer links
  alongside reviewed catalog URLs.

### Added (0.0.2 and earlier)

- A complete bilingual Python AI-coding workflow covering task contracts,
  repository inspection, reproducible environments, bounded changes, tests,
  runtime verification, side-effect review, and evidence-based delivery.
- Browsable English and Chinese README indexes containing every reviewed
  resource, its rationale, level, access requirements, risk, and review date.
- Deterministic README generation and drift checks backed by canonical catalog
  data.
- One source file per reviewed resource under `catalog/resources/`.
- A deterministic, versioned `catalog.json` export for pinned website consumers.
- A JSON Schema describing the public catalog v1 contract.
- A pinned-revision and checksum contract for website consumers.
- Export drift checks in tests and pull-request validation.
- Positive, unique, consecutive ordering within each learning path.
- Catalog validation and a safe external-link auditor with retry, report, and
  SSRF/DNS-rebinding protection.
- Contribution, conduct, security, issue, and resource-curation policies.
- A product-quality guide and five bilingual task playbooks for bug fixes, API
  work, external integrations, dependency upgrades, and releases.
- A standard-library-only example with a deliberately failing starter, verified
  solution, and task contract.
- Reusable task, plan, review, verification, agent-instruction, and pyproject
  templates.
- A versioned `content-manifest.json` with bilingual paths, summaries, review
  state, and source checksums for pinned website consumers.
- A human-review contribution queue for current Python Project Radar entries.

### Changed (0.0.2 and earlier)

- Defined this repository as the canonical Python product-engineering content,
  catalog-data, and review layer behind flypython.com, rather than a second
  public website.
- Split catalog metadata, paths, and resources into independently reviewable
  files while preserving the 21 existing human-reviewed resource records.
- Required website consumers to pin a full repository commit and verify the
  exported catalog checksum instead of following a moving branch.
- Reduced the required local toolchain to Python 3.12 and locked Python
  dependencies.

### Removed (0.0.2 and earlier)

- Removed Jekyll, Ruby, page templates, styles, scripts, social assets, CNAME,
  robots configuration, and site-rendering tests.
