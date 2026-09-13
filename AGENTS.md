# FlyPython repository guide

## Mission

This repository is the community-maintained source for building good Python
products in the AI-coding era. It is not a website. Keep `flypython.com`
focused on presentation, discovery, and conversion; keep this repository
focused on practical guides, playbooks, runnable examples, reusable templates,
reviewed catalog data, and stable public JSON contracts.

## Content rules

- Prefer official documentation and primary sources.
- Keep first-party Python engineering and AI-coding guidance specific, testable,
  and honest about what automation can and cannot prove.
- Every catalog entry must include a stable ID, path, path-local order, source
  type, level, rationale, review date, status, and any key or safety requirements.
- Do not call a project production-ready without current maintenance, licensing,
  security, and adoption evidence.
- Do not use an LLM or web-search API to generate resource descriptions.
  Descriptions and classifications require human review.
- Keep English and Chinese website output generated from the same canonical
  resource data. Do not hand-copy catalog content into website source files.
- Keep paired English and Chinese first-party guides aligned in scope, version,
  review date, and factual meaning. All content (guides, playbooks, examples,
  courses, radar entries) ships EN+ZH in the same change.
- Governance documents (`AGENTS.md`, `CONTRIBUTING.md`, `docs/CONSUMING.md`,
  `docs/CURATION_POLICY.md`, `docs/REPO_TO_WEBSITE.md`) are
  English-canonical. Version plans (`docs/repo-plan-*.md`) are maintained
  in Chinese by owner decision (2026-09-12); their English history stays
  in git.
- Add first-party guides, playbooks, and courses to `content-manifest.json`;
  keep each locale pair aligned and verify its source checksum.
- Courses live one folder per course under `courses/<slug>/` and are taught by
  an AI coding agent from the files themselves: `COURSE.md` (metadata plus the
  teaching contract: audience, prerequisites, exact tool and version,
  lesson order, teaching-style rules, when to stop, how to use `verify.py`,
  and what the course does not cover) with `id: course-<slug>` and `badge`
  frontmatter, `lessons/L01.md` with `L01_cn.md`
  pairs (objective, exercise, checkpoint, expected evidence), `scenario/`
  data files for each skin, `TASK.md`/`TASK_cn.md` (task contract),
  `starter/` and `solution/` runnable pairs, a self-contained `verify.py`
  that fails on `starter` and passes on `solution`, exposes deterministic
  claim codes through `verify.py progress` (five checkpoints), and runs on
  the standard library unless the course ships its own `requirements.txt`
  (as the pandas/matplotlib data-analysis courses do), and `REVIEW.md`
  recording the maintainer run-through (date, tool, version, observed agent
  deviations).
  A course is incomplete until every lesson ships EN+ZH in the same change;
  `COURSE.md` must name the exact tool version it was taught with, and a tool
  major release triggers re-review. Never claim guaranteed learning outcomes.
- Treat HTTP 403, 429, and transient 5xx responses as review-needed states, not
  automatic proof that a resource is broken.

## Change workflow

- Work on a feature branch and preserve unrelated contributor changes.
- Run the repository validation workflow before committing.
- Regenerate `catalog.json` and `radar.json` after source changes and verify
  them with `python tools/export_catalog.py --check --target both`.
- Regenerate both README catalog indexes and the Project Radar table, then
  verify them with `python tools/render_readmes.py --check`.
- Regenerate `content-manifest.json` and verify it with
  `python tools/build_content_manifest.py --check`.
- Verify every runnable example with `python tools/verify_examples.py`,
  every course folder with `python tools/verify_courses.py`, and every
  learning path with `python tools/verify_paths.py`.
- Website consumers must pin a full repository commit and verify the catalog
  checksum. Do not make production builds depend on a moving branch.
- Keep external-link checks read-only, rate-limited, retryable, and blocked from
  private or loopback network targets.
- Do not add API keys, tokens, analytics IDs, or generated reports to git.
- After merge, verify the immutable raw `catalog.json`. Verify flypython.com only
  after a separate, deliberate consumer-version update.

## Review priorities

1. Content accuracy and source quality.
2. Deterministic export and bilingual parity.
3. Schema, consumer-contract, and safe link checks.
4. Clear contribution and licensing boundaries.
