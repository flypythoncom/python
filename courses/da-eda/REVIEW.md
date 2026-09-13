# Maintainer run-through — da-eda

- Date: 2026-09-12
- Reviewed with: mechanical verification (this course ships no teaching
  contract beyond guided mode)
- `python verify.py starter --expect-failure`: reproduces the intended
  unfinished state — all twelve contract tests fail on NotImplementedError.
- `python verify.py solution`: all twelve tests pass.
- `python verify.py progress`: deterministic claim codes; L03/L04
  objective, L01/L02/L05 attested.
- Agent solvability run (challenge-model gate): **done 2026-09-13**.
  Agent: Devin (SWE-2 Max), CLI session on macOS arm64, repo venv with
  pandas. Method: implemented `starter/eda.py` from `TASK.md` only —
  drop_duplicates, `to_numeric`/`to_datetime` with `errors="coerce"`,
  groupby sums, merged stats into results.json — did not read or copy
  `solution/`. Result: `python verify.py starter` exits 0 (all twelve
  tests); `verify.py progress` printed all five claim codes. Deviations:
  none — solvable in one pass; cleaning order (dedupe before counting
  bad parses) matters and the contract pins the expected counts, which
  disambiguates it. Limitations: single run, single agent; results.json
  was written into `scenario/shop-export/` per the contract (already
  git-ignored/shipped — verify by `git status` staying clean).
  Starter restored to the deliberately-unfinished state after the run.
