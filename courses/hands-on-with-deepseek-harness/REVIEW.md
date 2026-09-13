# Maintainer run-through record

## 2026-09-13 — authored from official documentation (mechanical verification only)

- Course authored against the DeepSeek Harness documentation
  (deepseek-harness.github.io/deepseek-harness: plugin architecture,
  `cordis.yml` composition, append-only trajectory logs with
  inspect/resume/fork) and the shared `report-tool` core. `TASK.md`,
  `tests/`, `scenario/`, `starter/`, `solution/` are byte-identical to the
  Claude Code / Codex course cores — enforced by the `core-group` check in
  `tools/verify_courses.py`.
- Environment for mechanical verification: macOS (arm64), Python 3.13.
- Commands and results:
  - `python verify.py starter --expect-failure` — exit 0; expected failures
    reproduced.
  - `python verify.py solution` — exit 0; 9/9 tests pass.
  - `python tools/verify_courses.py` — contract satisfied, core identical.
- **Not done:** any run under DeepSeek Harness. No harness install, model
  endpoint, or API key was used; every harness behavior described in the
  lessons is sourced from official documentation, not observed.

## 2026-09-13 — 0.0.8 rework: lesson 1 is now tool → Skill → agent fetch (FP-822)

- L01 (EN+ZH) rewritten around the fixed order: get the tool running →
  install the FlyPython Skill (network access included) → let the agent
  fetch this course's files via the files endpoint. All "download this
  folder" wording removed from `COURSE.md` and lessons.
- The learner's check command across lessons is now the bare
  `python verify.py` (FP-820): per-checkpoint status + claim codes,
  non-zero exit while gated checkpoints are open. `solution` is no longer
  presented as a completion standard.
- Tool-specific Skill install and network steps are authored from the
  same official documentation as the course; **not yet exercised inside
  the tool** — the pending live run-through below still stands.

## Pending before this course can be called taught-in-tool

- One full agent-taught run-through under DeepSeek Harness ("start lesson 1"
  through the Lesson 5 checkpoint) on a current release, recording observed
  deviations from `COURSE.md` here — including the exact `cordis.yml` used
  and the model plugin configured.

## Deviation log

(none yet — no live run has happened)
