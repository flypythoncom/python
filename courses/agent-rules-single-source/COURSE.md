---
id: course-agent-rules
type: course
title: One source of truth for agent rules
summary: Stop maintaining diverging AGENTS.md, CLAUDE.md, and .cursorrules files — build a checker that proves your repository has exactly one rule source, taught hands-on with your coding agent.
lang: en-US
content_version: 3
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-agent-rules
  name_en: Measure the drift
  name_zh: 规则漂移检测
  requires: All five checkpoints claimed (L01–L05)
course_id: course-agent-rules
---

# One source of truth for agent rules

> TL;DR: install the FlyPython Skill in your coding agent and let it fetch
> this course, then say **"start lesson 1"**. (Lesson files arrive via
> the Skill — you download nothing by hand.) You finish with a working rule-consistency checker
> (`rules_check.py`) that fails CI the moment a rule file drifts from
> AGENTS.md — plus the single-source setup applied to your own repository.
> Tool-agnostic by design: Claude Code, Codex CLI, and Cursor all read these
> files.

## What you build

A standard-library-only checker that enforces the contract used by this very
repository: `AGENTS.md` must exist and be non-empty, and every other
recognized rule file (`CLAUDE.md`, `.cursorrules`) must either be a thin
pointer that defers to it or an exact copy of it. Anything else is drift,
reported with a reason and a failing exit code. Three scenario repositories
ship with the course:

| Skin | State | Data |
| --- | --- | --- |
| `scenario/thin-pointer/` | healthy: AGENTS.md + two pointer files | pointer-style CLAUDE.md, .cursorrules |
| `scenario/single-copy/` | healthy: AGENTS.md + exact copy | duplicated rule text |
| `scenario/drifted/` | broken: .cursorrules restates stale rules | a real drift to catch |

## Teaching contract (read this first, agent)

- **Audience:** anyone maintaining rule files for more than one agent tool —
  you have felt the pain of three files disagreeing about one behavior.
- **Prerequisites:** Python 3.11+ on PATH and any coding agent (taught and
  reviewed with Claude Code 2.x and Codex CLI 0.x; reviewed 2026-09-12 —
  tool-agnostic by design). Standard library only.
- **Lesson order:** L01 → L05; never skip the checkpoint.
- **Teaching style:** work from the files in this folder; quote the contract
  line you satisfy; smallest change per failing test; no new dependencies;
  never edit `solution/`; ask before touching unnamed files.
- **When to stop:** a lesson is done when its checkpoint command runs and the
  learner can explain what failed and why.
- **`verify.py`:** `python verify.py starter --expect-failure` reproduces the
  six listed failures; `python verify.py solution` passes 11/11.
- **Honesty rules:** say what you did not verify; no guarantees about agent
  obedience — the checker reports file state, not agent behavior.

## What this course does NOT cover

Which rules to write (see the repository's `templates/AGENT_RULES.example.md`
and the AGENTS.md guide on flypython.com), multi-repo setups, or
machine-policy enforcement. The checker is deliberately narrow: one
directory, three file names, one truth.


## Badge contract

- Badge: **Measure the drift Badge** (badge id `course-agent-rules`) - earned by claiming all five checkpoints.
- Challenges: L01-L05 checkpoints, 10 points each; +50 course-badge bonus when all five are claimed on flypython.com.
- Evidence: `python verify.py` - L03 (bounded change) and L04 (verify & review) are objectively gated by the suite; L01/L02/L05 are learner-attested.
- Submission: each passed checkpoint prints a deterministic claim code; record it on flypython.com against your account. Self-reported evidence, never a certificate.

## Folder map


`COURSE.md`/`COURSE_cn.md`, bilingual `lessons/`, `scenario/` repositories,
`TASK.md`/`TASK_cn.md` (the code contract), `starter/`, `solution/`, `tests/`
(11 tests), `verify.py`, `REVIEW.md`.

## Evidence and licensing

`REVIEW.md` records the run-through state. Code is MIT; prose is CC BY 4.0
(see repository `LICENSE`). Teaching drift goes to the `course-feedback`
issue form.
