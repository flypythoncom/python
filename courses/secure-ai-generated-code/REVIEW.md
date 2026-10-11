# Maintainer run-through record

## 2026-10-11 — contract verification (mechanical)

- Environment: Linux x86_64, Python 3.12.3, standard library only; Ruff
  0.16.10 for the Lesson 4 static-scan step.
- Sources for the flaw classes and the password-hash parameters: the
  Python `sqlite3`, `pathlib`, `hashlib`, `hmac`, `secrets`, and `pickle`
  documentation, MITRE CWE-89/22/798/916/759/502, and the OWASP Password
  Storage Cheat Sheet (PBKDF2-HMAC-SHA256 at 600 000 iterations). The
  course uses PBKDF2 because it is in the standard library; the OWASP
  preference for Argon2id is stated in `COURSE.md`.
- Commands and results:
  - `python verify.py starter --expect-failure` — exit 0; the ten expected
    failure names reproduced (the symlink test is excluded from the list
    because some platforms skip it; on this Linux run it fails on the
    starter too, for eleven failing tests).
  - `python verify.py solution` — exit 0; 16/16 tests pass, none skipped.
  - `python verify.py` — exit 1 on the shipped starter; l03/l04 `[open]`,
    l01/l02/l05 `[pending]` with no code.
  - `python solution/attack_replay.py scenario/team-notes` — `blocked=9/9`,
    exit 0; `scenario/clinic-notes` — `blocked=8/8`, exit 0. The starter
    reports `blocked=0/9` and `blocked=0/8`.
  - `ruff check --select S starter/notes_app.py` on the shipped starter:
    S608 (SQL built from strings), S324 twice (MD5), S301 (`pickle`). It
    does not flag the path join or the hard-coded fallback secret — the
    point Lesson 4 makes. The solution has no S findings.
  - Lesson 3's turn table (failing tests 11 → 9 → 6 → 5 → 3 → 0, replay
    0 → 2 → 4 → 6 → 7 → 9 of 9) was measured by swapping the solution's
    functions into a scratch copy of the starter one flaw class at a time.
  - The Lesson 3 exercise inputs behave as described: `./agenda.txt` reads,
    `agenda.txt/../../secrets.txt` raises `SecurityError`.
  - `python tools/verify_courses.py` — contract satisfied.
- Safety: the suite and the replay harness unpickle a deliberately
  harmless gadget that only creates a directory inside a temporary folder.
  No network, no shell, no files outside the temp folder.

## Pending before this course can be called taught-in-tool

- One full agent-taught run-through ("start lesson 1" through the Lesson 5
  checkpoint) in a named coding agent and version, recording observed
  deviations from `COURSE.md` here. The course is tool-agnostic; no
  agent-taught session has happened yet.
- A security-practitioner review of the lesson wording. The fixes are
  standard-library techniques checked against the sources above; nobody
  with an application-security role has reviewed the course yet.

## Deviation log

### 2026-10-11 — agent solvability run (challenge mode, not taught mode)

- Agent: a Cursor Cloud Agent subagent (Claude Opus 5.5), Linux, Python
  3.12.3, standard library only.
- Method: worked in a copy of the course with `solution/` and this file
  removed; fixed `starter/notes_app.py` from `TASK.md` and the tests only,
  without access to the reference solution.
- Result: 16/16 tests (none skipped) after one edit; `blocked=9/9` and
  `blocked=8/8`; no Ruff S findings on its fixed file. It independently
  re-measured Lesson 3's turn table and got the same numbers.
- Observed deviations and the changes they triggered:
  - `TASK.md` did not say that `hash_password` accepts any iteration count
    while `verify_password` enforces the minimum; the agent inferred it
    from a test. Both TASK files now say it.
  - The token format `base64url(JSON).hex(...)` read ambiguously; both TASK
    files now spell out the literal `.` separator.
  - While checking the agent's notes, the reference solution was found to
    raise `TypeError` (from `hmac.compare_digest`) on a token containing
    non-ASCII characters instead of `SecurityError`. The solution now
    refuses non-ASCII tokens, the TASK files say so, and the tamper test
    includes such a token. The agent's implementation already handled it.
  - `COURSE.md` said plain `python verify.py` exits non-zero "while l03 and
    l04 are open"; it actually exits non-zero until l01/l02/l05 are also
    attested. Wording corrected in `COURSE.md`/`COURSE_cn.md`.
- Not changed, recorded for the next review: `TASK.md` sets no upper bound
  on the iteration count read from a stored hash, so a hostile stored
  value could make `verify_password` slow; SQLite's `lower()` folds only
  ASCII, so case-insensitive search does not fold `É`.
- Limitations: challenge-mode run (TASK.md → tests), not the taught
  COURSE.md walkthrough; teaching quality remains pending.
