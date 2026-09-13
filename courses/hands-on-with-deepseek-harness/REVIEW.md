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

## Pending before this course can be called taught-in-tool

- One full agent-taught run-through under DeepSeek Harness ("start lesson 1"
  through the Lesson 5 checkpoint) on a current release, recording observed
  deviations from `COURSE.md` here — including the exact `cordis.yml` used
  and the model plugin configured.

## Deviation log

(none yet — no live run has happened)
