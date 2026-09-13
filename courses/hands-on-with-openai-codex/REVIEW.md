# Maintainer run-through record

## 2026-09-13 — content rewrite: CLI course → Codex desktop app course

- Folder renamed `hands-on-with-openai-codex-cli` →
  `hands-on-with-openai-codex`; `course_id` (`course-codex-cli`) and claim
  salt preserved so existing claims and codes remain valid.
- `COURSE.md`/`COURSE_cn.md` and all ten lesson files rewritten against
  the Codex app as documented at developers.openai.com/codex (thread
  model, approval modes, AGENTS.md instruction chain, diff review).
  CLI-specific teaching was removed; `TASK.md`, `tests/`, `scenario/`,
  `starter/`, `solution/` are byte-identical to the Claude Code course
  core (shared-core group `report-tool`, enforced by
  `tools/verify_courses.py`).
- **Not done in this pass:** a live teaching run-through inside the Codex
  desktop app. No Codex account/app session was used; the content is
  authored from official documentation and the previously verified task
  core. Teaching quality in the real app remains pending below.

## 2026-09-12 — contract verification (mechanical)

- Environment: macOS (arm64), Python 3.13; repository clean checkout on
  branch `feat/0.0.3-courses-and-radar`.
- The code core is the reviewed Claude Code course core reused per the 0.0.3
  plan §2.2 ("reuse C1 skins"): same starter/solution/tests contract.
- Commands and results:
  - `python verify.py starter --expect-failure` — exit 0; all seven expected
    failure names reproduced.
  - `python verify.py solution` — exit 0; 9/9 tests pass.
  - All three skins exercised end to end by the shared suite.

## Pending before this rewrite can be called taught-in-tool

- One full agent-taught run-through inside the Codex desktop app
  ("start lesson 1" through the Lesson 5 checkpoint), recording observed
  deviations from `COURSE.md` here; the recording doubles as demo-video
  source material.
- Whether a free ChatGPT tier lasts the whole course is unverified.

## Deviation log

### 2026-09-13 — agent solvability run (challenge mode, not taught mode)

- Agent: Devin (SWE-2 Max), CLI session on macOS arm64, system Python
  3.14 (stdlib only — this course needs no third-party deps).
- Method: implemented `starter/report_tool.py` from `TASK.md` and the
  test expectations only; did not read or copy `solution/`.
- Result: `python verify.py starter` exits 0 (all nine tests);
  `verify.py progress` printed all five claim codes (l03/l04
  `[passed]`, l01/l02/l05 `[attest]`).
- Observed deviations: none — contract landed on the first pass. This
  course shares its task core (TASK/tests/scenario) with
  hands-on-python-with-claude-code, and the same implementation passes
  both suites.
- Limitations: challenge-mode run (TASK.md → tests), not the taught
  COURSE.md walkthrough — teaching quality remains separately pending.
- Starter restored to the deliberately-unfinished state after the run
  (`--expect-failure` verified again).
