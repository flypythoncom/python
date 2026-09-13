---
id: course-cursor
type: course
title: Hands-on with Cursor
summary: The verified Python workflow — task contract, bounded change, objective verify.py evidence — taught hands-on in Cursor, where Agent mode runs the loop and you supervise diffs and project rules.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-13
badge:
  id: course-cursor
  name_en: Reproduce with Cursor in the loop
  name_zh: Cursor 协同复现
  requires: All five checkpoints claimed (L01–L05)
course_id: course-cursor
---

# Hands-on with Cursor

> TL;DR: download this folder, open it as a project in Cursor, open an Agent
> chat, and say **"start lesson 1"**. You finish with a working report tool,
> a reproducible pass/fail command, and the Cursor workflow: Agent/Ask/Plan
> modes, `.cursor/rules` project rules, and diff review. The exercise core is
> the same one the Claude Code and Codex courses use — only the tool you
> drive changes.

## What you build

A small Python report tool that reads messy real-world data (CSV or JSON),
isolates invalid rows instead of crashing, aggregates valid rows, and writes
its report atomically. Three scenario "skins" ship with the course so you can
practice on a domain you recognize:

| Skin | You are… | Data |
| --- | --- | --- |
| `scenario/excel-report/` | turning a weekly orders export into a region summary | `orders.csv` |
| `scenario/data-monitor/` | checking service latency numbers from your servers | `metrics.csv` |
| `scenario/api-tool/` | summarizing ticket data pulled from an internal API | `tickets.json` |

All three run through the same code and the same tests. The skills —
contracts, error isolation, rounding, atomic writes, verification — are the
actual product; the skins just make them concrete.

## Teaching contract (read this first, agent)

If you are the Cursor agent teaching this course, follow these rules:

- **Audience:** a project owner who has working-with-AI experience but is
  stuck on reliability — the script runs, then breaks on real data. Not a
  Python beginner tutorial; not a prompt-engineering course.
- **Prerequisites:** Python 3.11+ on PATH and the Cursor editor installed
  and signed in. No packages to install — the course is standard library
  only. Agent usage limits on the learner's plan are unverified at authoring
  time — see `REVIEW.md`.
- **Tool:** authored against Cursor as documented at cursor.com/docs
  (Agent/Ask/Plan modes, `.cursor/rules/*.mdc` project rules with
  `description`/`globs`/`alwaysApply` front matter, diff review). A live
  teaching run-through is pending — `REVIEW.md` records what has and has
  not been exercised. A Cursor major release triggers a course re-review.
- **Lesson order:** L01 → L02 → L03 → L04 → L05, one lesson per session.
  Never skip the checkpoint at the end of a lesson.
- **Teaching style:** work from the files in this folder, not from general
  knowledge. Quote the exact contract line you are satisfying. Make the
  smallest change that moves a test from red to green. Never add
  dependencies, never edit `solution/`, and ask before touching any file
  not named in the current lesson. Read `AGENTS.md` in the repository root
  if one exists — Cursor reads it too.
- **When to stop:** a lesson is done when its checkpoint command runs and
  the learner can say, in their own words, what failed and why. If the
  learner cannot, re-teach from the failing test, not from the solution.
- **How to use `verify.py`:** run it in the integrated terminal, or let the
  Agent run it — `python verify.py starter --expect-failure` must reproduce
  the listed failures; `python verify.py solution` must pass. "Done" means
  the starter implementation passes the same suite after the learner's
  bounded change.
- **Honesty rules:** say what you did not verify. Do not claim the code is
  production-ready. Do not promise learning or career outcomes.

## What this course does NOT cover

Cursor installation, pricing plans, model selection, MCP setup, team/admin
features, or selling anything. For those, the companion repository has
guides and playbooks — link, don't improvise.

## Badge contract

- Badge: **Reproduce with Cursor in the loop Badge** (badge id `course-cursor`) — earned by claiming all five checkpoints.
- Challenges: L01–L05 checkpoints, 10 points each; +50 course-badge bonus when all five are claimed on flypython.com.
- Evidence: `python verify.py progress` — L03 (bounded change) and L04 (verify & review) are objectively gated by the suite; L01/L02/L05 are learner-attested.
- Submission: each passed checkpoint prints a deterministic claim code; record it on flypython.com against your account. Self-reported evidence, never a certificate.

## Folder map

```
COURSE.md / COURSE_cn.md   this file (EN / 中文)
lessons/L01.md … L05.md    lessons (each has an _cn.md pair)
scenario/<skin>/           data files and scenario.json per skin
TASK.md / TASK_cn.md       the task contract the change must satisfy
starter/report_tool.py     the deliberately unfinished implementation
solution/report_tool.py    the reviewed solution (do not copy in lesson 3)
tests/test_report_tool.py  the contract suite (read-only)
verify.py                  objective pass/fail evidence
REVIEW.md                  maintainer run-through record
```

## Evidence and licensing

The course folder is reviewed content: `REVIEW.md` records the last
run-through with dates, tool versions, and observed deviations. Code in this
folder is MIT-licensed; lesson prose is CC BY 4.0 (see repository `LICENSE`).
Report teaching drift or unclear lessons via the repository's
`course-feedback` issue form.
