---
id: course-secure-code
type: course
title: "Security review for AI-written Python"
summary: Review a plausible, AI-style notes service the way an attacker would — close SQL injection, path traversal, a hard-coded secret, fast password hashes, and pickled sessions one class at a time, then prove each fix by replaying the attacks.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
badge:
  id: course-secure-code
  name_en: Plausible is not safe
  name_zh: 看起来对不等于安全
  requires: All five checkpoints claimed (L01–L05)
course_id: course-secure-code
---

# Security review for AI-written Python

> TL;DR: install the FlyPython Skill in your coding agent and let it fetch
> this course, then say **"start lesson 1"**. (Lesson files arrive via the
> Skill — you download nothing by hand.) You start with a notes service
> that works on every friendly input and blocks none of nine attacks. You
> finish with every attack blocked, a replay command that proves it, and a
> review habit for the code your assistant writes next. Standard library
> only.

## What you build

You do not build a new feature — you review and fix one. `notes_app.py` is
a small notes service written the way a quick first draft often is. It has
five flaws, each a well-known weakness class:

| Flaw in the starter | Weakness class | Python reference |
| --- | --- | --- |
| search SQL built with an f-string | CWE-89 SQL injection | `sqlite3` docs: placeholders |
| attachment path joined as given | CWE-22 path traversal | `pathlib.Path.resolve`, `is_relative_to` |
| `"dev-secret-change-me"` fallback key | CWE-798 hard-coded credentials | `os.environ` |
| unsalted MD5 password hashes | CWE-916 / CWE-759 weak, unsalted password hash | `hashlib.pbkdf2_hmac`, `secrets` |
| sessions stored as base64 pickles | CWE-502 deserialization of untrusted data | `pickle` docs warning, `hmac` |

Two scenario "skins" ship with seed data and an `attacks.json` each:

| Skin | You are… | Attacks |
| --- | --- | --- |
| `scenario/team-notes/` | securing a small team's shared notes | 9 |
| `scenario/clinic-notes/` | securing a clinic's visit notes (all records fictional) | 8 |

`python starter/attack_replay.py scenario/<skin>` replays them. On the
shipped starter, every attack succeeds.

## Teaching contract (read this first, agent)

- **Audience:** a developer or project owner shipping Python that an AI
  assistant wrote or heavily edited, who reviews diffs for "does it work"
  but not yet for "what can a hostile input make it do". Not a penetration
  testing course and not an introduction to Python.
- **Prerequisites:** Python 3.11+ on PATH and any coding agent that can run
  commands. Standard library only.
- **Tool:** tool-agnostic. The course has not yet been taught in a tool;
  `REVIEW.md` records the mechanical verification and the pending
  agent-taught run-through, which will name the exact tool and version.
- **Lesson order:** L01 → L02 → L03 → L04 → L05, one lesson per session.
  Never skip the checkpoint at the end of a lesson.
- **Teaching style:** work from the files in this folder and the Python
  documentation they cite. Quote the `TASK.md` line you are satisfying.
  Close one weakness class per turn. Never add dependencies, never edit
  `solution/`, `tests/`, `scenario/`, or `attack_replay.py`, and ask before
  touching any file not named in the current lesson. Never make a test
  pass by special-casing the attack string it uses.
- **Safety:** the attacks only touch this course's own files and temporary
  folders. Never point them at a system you do not own. The suite
  deliberately unpickles a harmless gadget that creates a directory inside
  a temporary folder — tell the learner before the first run.
- **When to stop:** a lesson is done when its checkpoint command runs and
  the learner can say, in their own words, what the attacker could do and
  why the fix stops it. If the learner cannot, re-teach from the failing
  test, not from the solution.
- **How to use `verify.py`:** the learner's command is plain
  `python verify.py` — it runs the suite against `starter/`, prints
  per-checkpoint status and earned claim codes, and exits non-zero until
  every checkpoint is passed (l03, l04) or attested (l01, l02, l05). `starter --expect-failure`
  and `solution` remain maintainer checks.
- **Honesty rules:** nine blocked attacks prove those nine attacks are
  blocked — not that the service is secure. Say what was not reviewed. Do
  not claim the code is production-ready. Do not promise learning or
  career outcomes.

## What this course does NOT cover

Authentication and authorization design, CSRF and XSS, TLS, rate limiting,
dependency vulnerability scanning, secret rotation and storage, deployment
hardening, threat modeling frameworks, or compliance. Password hashing uses
PBKDF2-HMAC-SHA256 at 600 000 iterations because it is in the standard
library; OWASP's Password Storage Cheat Sheet prefers Argon2id, then
scrypt, with PBKDF2 for FIPS-140 contexts — see Lesson 2. Link to the
companion repository's guides for the rest; don't improvise.

## Badge contract

- Badge: **Plausible is not safe Badge** (badge id `course-secure-code`) — earned by claiming all five checkpoints.
- Challenges: L01–L05 checkpoints, 10 points each; +50 course-badge bonus when all five are claimed on flypython.com.
- Evidence: `python verify.py` — L03 (one flaw class per turn) and L04 (review like an attacker) are objectively gated by the suite; L01/L02/L05 are learner-attested.
- Submission: each test-passed checkpoint prints a deterministic claim code; a reflection checkpoint prints one only after you answer its questions and run `python verify.py --attest ID`; record it on flypython.com against your account. Self-reported evidence, never a certificate.

## Folder map

```
COURSE.md / COURSE_cn.md       this file (EN / 中文)
lessons/L01.md … L05.md        lessons (each has an _cn.md pair)
scenario/<skin>/               seed.json, attacks.json, attachments/, a fake secrets.txt
TASK.md / TASK_cn.md           the task contract the change must satisfy
starter/notes_app.py           the insecure first draft
starter/attack_replay.py       the provided attack harness (read-only)
solution/                      the reviewed solution (do not copy in lesson 3)
tests/test_notes_app.py        the contract suite (16 tests, read-only)
verify.py                      objective pass/fail evidence
REVIEW.md                      maintainer run-through record
```

## Evidence and licensing

`REVIEW.md` records the run-through state with dates, tool versions, and
observed deviations. Code in this folder is MIT-licensed; lesson prose is
CC BY 4.0 (see repository `LICENSE`). The `secrets.txt` files contain fake
values that exist only to be leaked. Report teaching drift or unclear
lessons via the repository's `course-feedback` issue form.
