# Maintainer run-through record

## 2026-09-12 — contract verification (mechanical)

- Environment: macOS (arm64), Python 3.13; repository clean checkout on
  branch `feat/0.0.3-courses-and-radar`.
- Commands and results:
  - `python verify.py starter --expect-failure` — exit 0; all seven expected
    failure names reproduced (JSON loading, unsupported suffix, row
    isolation, rounding, parent directories, scenario report, CLI summary).
  - `python verify.py solution` — exit 0; 9/9 tests pass.
  - All three skins exercised end to end through `run_scenario` in the test
    suite (`excel-report`, `data-monitor`, `api-tool`); report totals and
    group sums recomputed by hand against the scenario data files.
- Not verified in this pass: teaching quality with a live agent session.

## Pending before the public course drop

- One full agent-taught run-through with Claude Code 2.x ("start lesson 1"
  through Lesson 5 checkpoint), recording observed deviations from
  COURSE.md here. This recording doubles as the demo-video source material
  per the 0.0.3 plan §4.5.
- Course status remains `reviewed` for content and code; the agent-teaching
  sample is tracked as launch evidence, not a content blocker.

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

## Deviation log

### 2026-09-13 — agent solvability run (challenge mode, not taught mode)

- Agent: Devin (SWE-2 Max), CLI session on macOS arm64, system Python
  3.14 (stdlib only — this course needs no third-party deps).
- Method: implemented `starter/report_tool.py` from `TASK.md` and the
  test expectations only; did not read or copy `solution/`.
- Result: `python verify.py starter` exits 0 (all nine tests);
  `verify.py progress` printed all five claim codes (l03/l04
  `[passed]`, l01/l02/l05 `[attest]`).
- Observed deviations: none — contract landed on the first pass. All
  three scenario skins (csv/json inputs, invalid-row isolation,
  rounding, atomic write into a fresh directory) were exercised.
- Limitations: challenge-mode run (TASK.md → tests), not the taught
  COURSE.md walkthrough — teaching quality remains separately pending.
- Starter restored to the deliberately-unfinished state after the run
  (`--expect-failure` verified again).
