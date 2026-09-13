# Maintainer run-through — da-visualization

- Date: 2026-09-12
- `python verify.py starter --expect-failure`: reproduces the intended
  unfinished state — all five contract tests fail.
- `python verify.py solution`: all five tests pass; three valid PNGs and
  summary.json written to out/.
- `python verify.py progress`: deterministic claim codes; L03/L04
  objective, L01/L02/L05 attested.
- Agent solvability run (challenge-model gate): **done 2026-09-13**.
  Agent: Devin (SWE-2 Max), CLI session on macOS arm64, repo venv with
  pandas + matplotlib. Method: implemented `starter/charts.py` from
  `TASK.md` only (Agg backend, groupby sums, three fig.savefig +
  summary.json), did not read or copy `solution/`. Result:
  `python verify.py starter` exits 0; `verify.py progress` printed all
  five claim codes (l03/l04 `[passed]`). Deviations: none — solvable in
  one pass; the only trap is forgetting `matplotlib.use("Agg")` before
  pyplot import, which TASK.md states plainly. Limitations: single run;
  the suite checks PNG validity and JSON numbers, not chart quality —
  consistent with the L05 "what verification cannot see" lesson.
  Starter restored to the deliberately-unfinished state after the run.
