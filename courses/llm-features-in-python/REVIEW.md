# Maintainer run-through record

## 2026-10-11 — contract verification (mechanical)

- Environment: Linux x86_64, Python 3.12.3, standard library only.
- The scenario recordings (`scenario/*/recordings.json`) are hand-written
  fixtures that imitate common reply failures (Markdown fences, invented
  categories, string priorities, prose, out-of-allowlist tool calls). They
  were not captured from any model, and no model API was called while
  authoring or verifying this course.
- Commands and results:
  - `python verify.py starter --expect-failure` — exit 0; the twelve
    expected failure names reproduced; three tests pass on the starter.
  - `python verify.py solution` — exit 0; 15/15 tests pass.
  - `python verify.py` — exit 1 on the shipped starter; l03/l04 `[open]`,
    l01/l02/l05 `[pending]` with no code.
  - Solution eval CLI:

    | Skin | Output | Exit |
    | --- | --- | --- |
    | `shop-support` | `accuracy=0.750 correct=6/8 fallbacks=1 min_accuracy=0.800` | 1 |
    | `it-helpdesk` | `accuracy=0.833 correct=5/6 fallbacks=1 min_accuracy=0.800` | 0 |
    | `saas-feedback` | `accuracy=0.800 correct=4/5 fallbacks=0 min_accuracy=0.800` | 0 |

    The starter prints `accuracy=1.000 correct=5/6` on `it-helpdesk`, the
    contradiction Lesson 1 is built on.
  - Lesson 3's failing-count table (12 → 9 → 7 → 3 → 0) was measured by
    swapping the solution's functions into a scratch copy of the starter
    one group at a time; `test_tool_result_is_fed_back_to_the_model` turns
    red after the parser group, as the lesson says.
  - The Lesson 3 exercise one-liner prints the retry feedback message
    after the `triage` turn.
  - `python tools/verify_courses.py` — contract satisfied.

## Pending before this course can be called taught-in-tool

- One full agent-taught run-through ("start lesson 1" through the Lesson 5
  checkpoint) in a named coding agent and version, recording observed
  deviations from `COURSE.md` here. The course is tool-agnostic; no
  agent-taught session has happened yet.
- Lesson 5 asks learners to apply the pattern to their own model-backed
  feature with a real provider. Whether the contract transfers cleanly to a
  provider's native structured-output or tool-calling API is unverified
  here.

## Deviation log

### 2026-10-11 — agent solvability run (challenge mode, not taught mode)

- Agent: a Cursor Cloud Agent subagent (Claude Opus 5.5), Linux, Python
  3.12.3, standard library only.
- Method: worked in a copy of the course with `solution/` and this file
  removed; implemented `starter/ticket_triage.py` from `TASK.md` and the
  tests only, without access to the reference solution.
- Result: green after one implementation pass (14/14 on the revision it
  was given); the eval CLI printed the same three lines as the solution
  table above.
- Observed deviations and the changes they triggered:
  - `TASK.md` did not define `attempts` in the fallback; the agent inferred
    "number of rejected replies" from a test. `TASK.md`/`TASK_cn.md` now
    state it.
  - `TASK.md` did not say whether a tool call beyond `max_tool_calls` runs,
    or whether refused calls count as `tool_calls`, and no test exercised
    the budget. The contract now says only calls that ran are counted and
    the over-budget call is not run; the new
    `test_tool_call_budget_ends_in_the_fallback` enforces it (suite 14 → 15
    tests, starter failures 11 → 12, lessons updated). The agent's
    implementation passes the new test unchanged.
  - `COURSE.md` said plain `python verify.py` exits non-zero "while l03 and
    l04 are open"; it actually exits non-zero until l01/l02/l05 are also
    attested. Wording corrected in `COURSE.md`/`COURSE_cn.md`.
- Limitations: challenge-mode run (TASK.md → tests), not the taught
  COURSE.md walkthrough; teaching quality remains pending. The agent
  implemented all four functions in one pass, so it did not walk Lesson 3's
  per-turn sequence (that sequence was measured mechanically, above).
