# Maintainer run-through — da-report

- Date: 2026-09-12
- `python verify.py starter --expect-failure`: reproduces the intended
  unfinished state — all six contract tests fail.
- `python verify.py solution`: all six tests pass; report.md and
  report.json written to out/.
- `python verify.py progress`: deterministic claim codes; L03/L04
  objective, L01/L02/L05 attested.
- Agent solvability run (challenge-model gate): **done 2026-09-13**.
  Agent: Devin (SWE-2 Max), CLI session on macOS arm64, repo venv
  Python 3.x with pandas installed. Method: implemented
  `starter/report.py` from `TASK.md` only (load → build → render →
  write → main), did not read or copy `solution/`. Result:
  `python verify.py starter` exits 0; `verify.py progress` printed all
  five claim codes (l03/l04 `[passed]`, l01/l02/l05 `[attest]`).
  Observed deviations: none — the contract was implementable in one
  pass; the metrics-carry-unchanged rule is the main trap and the
  TASK.md wording makes it explicit. Limitations: single run, single
  agent; the course does not teach *how* to write the report, so this
  verifies solvability, not pedagogy. Starter restored to the
  deliberately-unfinished state after the run (required by
  `--expect-failure`).
