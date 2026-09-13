# Maintainer run-through record

## 2026-09-13 — authored from official documentation (mechanical verification only)

- Course authored against the Kimi Code documentation
  (moonshotai.github.io/kimi-code: built-in `coder`/`explore`/`plan`
  subagents — `explore` read-only, `plan` without write/shell tools,
  subagents cannot spawn subagents — and `kimi acp` exposing the Agent
  Client Protocol) and the shared `report-tool` core. `TASK.md`, `tests/`,
  `scenario/`, `starter/`, `solution/` are byte-identical to the Claude
  Code / Codex course cores — enforced by the `core-group` check in
  `tools/verify_courses.py`.
- Environment for mechanical verification: macOS (arm64), Python 3.13.
- Commands and results:
  - `python verify.py starter --expect-failure` — exit 0; expected failures
    reproduced.
  - `python verify.py solution` — exit 0; 9/9 tests pass.
  - `python tools/verify_courses.py` — contract satisfied, core identical.
- **Not done:** any run inside Kimi Code. No `kimi` install or account was
  used; every Kimi Code behavior described in the lessons is sourced from
  official documentation, not observed.

## Pending before this course can be called taught-in-tool

- One full agent-taught run-through inside Kimi Code ("start lesson 1"
  through the Lesson 5 checkpoint) on a current release, recording observed
  deviations from `COURSE.md` here — including how the subagents were
  actually invoked in the current UI.
- Whether a free-tier Kimi account lasts the whole course is unverified.

## Deviation log

(none yet — no live run has happened)
