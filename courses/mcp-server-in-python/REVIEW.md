# Maintainer run-through record

## 2026-09-12 — contract verification (mechanical)

- Environment: macOS (arm64), Python 3.13; repository clean checkout on
  branch `feat/0.0.3-courses-and-radar`.
- The code core is the reviewed `examples/mcp-server` contract reused per the 0.0.3 plan §2.2 ("reuse mcp-server example + migration guide").
- Commands and results:
  - `python verify.py starter --expect-failure` — exit 0; all expected
    failure names reproduced.
  - `python verify.py solution` — exit 0; full suite passes.
  - Every `scenario/requests/` wire sample exercised end to end by the suite.
- Not verified in this pass: teaching quality with a live agent session.

## Pending before the public course drop

- One full agent-taught run-through ("start lesson 1" through the Lesson 5
  checkpoint), recording observed deviations from COURSE.md here; the
  recording doubles as demo-video source material.

## Deviation log

### 2026-09-13 — agent solvability run (challenge mode, not taught mode)

- Agent: Devin (SWE-2 Max), CLI session on macOS arm64, system Python
  3.14 (stdlib only — this course needs no third-party deps).
- Method: implemented `starter/mcp_server.py` from `TASK.md` and the
  test expectations only; did not read or copy `solution/`.
- Result: `python verify.py starter` exits 0 (all tests);
  `verify.py progress` printed all five claim codes (l03/l04
  `[passed]`, l01/l02/l05 `[attest]`).
- Observed deviations: none — contract landed on the first pass. The
  stateless 2026-07-28 behaviors (removed `initialize`, per-request
  `_meta.protocolVersion`, `input_required` round-trip) were all
  exercised by the suite.
- Limitations: challenge-mode run (TASK.md → tests), not the taught
  COURSE.md walkthrough — teaching quality remains separately pending.
- Starter restored to the deliberately-unfinished state after the run
  (`--expect-failure` verified again).
