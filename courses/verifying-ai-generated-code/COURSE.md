---
id: course-verify-ship
type: course
title: "From \"it runs\" to \"it ships\": verifying AI-generated code"
summary: Build the release-evidence machine your AI-written project is missing — a ship check that runs the tests, parses what actually ran, refuses zero-test projects, and writes an honest delivery record.
lang: en-US
content_version: 3
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-verify-ship
  name_en: It runs is not evidence
  name_zh: 能跑不是证据
  requires: All five checkpoints claimed (L01–L05)
course_id: course-verify-ship
---

# From "it runs" to "it ships": verifying AI-generated code

> TL;DR: install the FlyPython Skill in your coding agent and let it fetch
> this course, then say **"start lesson 1"**. (Lesson files arrive via
> the Skill — you download nothing by hand.) You finish with `ship_check.py`: one command that
> turns "the demo worked" into a written delivery record — command, exit
> code, parsed test count, a verdict that refuses projects with no tests,
> and an explicit unverified list. Tool-agnostic; Python standard library
> only.

## What you build

A release-evidence builder for small AI-written Python projects. Given a
project directory with a `ship.json`, it runs the configured check command,
parses how many tests actually ran and whether they passed, and writes an
atomic `SHIP-RECORD.json` with an honest verdict:

| Skin | State | Data |
| --- | --- | --- |
| `scenario/green-project/` | two passing tests + declared unverified items | `ship.json`, `calc.py`, `tests/` |
| `scenario/red-project/` | one deliberately wrong expectation | the regression under study |
| `scenario/no-tests/` | zero tests — the state that must never pass | empty `tests/` |

## Teaching contract (read this first, agent)

- **Audience:** a project owner shipping AI-written Python who cannot yet
  answer "what proves this release?" with a file instead of a memory.
- **Prerequisites:** Python 3.11+ on PATH and any coding agent (taught and
  reviewed with Claude Code 2.x and Codex CLI 0.x; reviewed 2026-09-12).
  Standard library only.
- **Lesson order:** L01 → L05; never skip the checkpoint.
- **Teaching style:** work from the files in this folder; quote the contract
  line you satisfy; smallest change per failing test; no new dependencies;
  never edit `solution/` or the scenario projects; ask before touching
  unnamed files.
- **When to stop:** a lesson is done when its checkpoint command runs and
  the learner can explain what failed and why.
- **`verify.py`:** `python verify.py starter --expect-failure` reproduces the
  seven listed failures; `python verify.py solution` passes 10/10.
- **Honesty rules:** the record's "unverified" list is the point — never
  present a passing record as proof of more than it contains.

## What this course does NOT cover

Deployment platforms, CI services, performance testing, or staging
environments. The product-quality guide on flypython.com covers the wider
release checklist; this course builds the evidence core.


## Badge contract

- Badge: **It runs is not evidence Badge** (badge id `course-verify-ship`) - earned by claiming all five checkpoints.
- Challenges: L01-L05 checkpoints, 10 points each; +50 course-badge bonus when all five are claimed on flypython.com.
- Evidence: `python verify.py` - L03 (bounded change) and L04 (verify & review) are objectively gated by the suite; L01/L02/L05 are learner-attested.
- Submission: each passed checkpoint prints a deterministic claim code; record it on flypython.com against your account. Self-reported evidence, never a certificate.

## Folder map


`COURSE.md`/`COURSE_cn.md`, bilingual `lessons/`, `scenario/` projects,
`TASK.md`/`TASK_cn.md` (the code contract), `starter/`, `solution/`,
`tests/` (10 tests), `verify.py`, `REVIEW.md`.

## Evidence and licensing

`REVIEW.md` records the run-through state. Code is MIT; prose is CC BY 4.0
(see repository `LICENSE`). Teaching drift goes to the `course-feedback`
issue form.
