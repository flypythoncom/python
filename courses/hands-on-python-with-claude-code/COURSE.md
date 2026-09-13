---
id: course-claude-code
type: course
title: Hands-on Python with Claude Code
summary: An agent-taught course that takes you from a cloned folder to a tested, verified Python report tool using Claude Code — including the task contract, the bounded change, and the objective pass/fail evidence.
lang: en-US
content_version: 3
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-claude-code
  name_en: Reproduce the failure
  name_zh: 复现故障
  requires: All five checkpoints claimed (L01–L05)
course_id: course-claude-code
---

# Hands-on Python with Claude Code

> TL;DR: set up Claude Code, install the FlyPython Skill, and let the agent
> fetch this course — lesson 1 walks you through all three steps and you
> download nothing. Then say **"start lesson 1"**, and the agent teaches you a verified workflow for AI-written Python: task
> contract → smallest change → tests → objective verification. You finish with
> a working report tool, a reproducible pass/fail command, and a pattern you
> can apply to your own project. Claude Code is the tool used in the lessons,
> but the workflow works with any capable coding agent.

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

All three run through the same code and the same tests. The skills — contracts,
error isolation, rounding, atomic writes, verification — are the actual
product; the skins just make them concrete.

## Teaching contract (read this first, agent)

If you are the coding agent teaching this course, follow these rules:

- **Audience:** a project owner who has working-with-AI experience but is stuck
  on reliability — the script runs, then breaks on real data. Not a Python
  beginner tutorial; not a prompt-engineering course.
- **Prerequisites:** Python 3.11+ on PATH, this folder open in the tool,
  and the ability to run shell commands. No packages to install — the course
  is standard library only.
- **Tool:** taught and reviewed with Claude Code 2.x (reviewed 2026-09-12).
  A Claude Code major release triggers a course re-review.
- **Lesson order:** L01 → L02 → L03 → L04 → L05, one lesson per session.
  Never skip the checkpoint at the end of a lesson.
- **Teaching style:** work from the files in this folder, not from general
  knowledge. Quote the exact contract line you are satisfying. Make the
  smallest change that moves a test from red to green. Never add dependencies,
  never edit `solution/`, and ask before touching any file not named in the
  current lesson.
- **When to stop:** a lesson is done when its checkpoint command runs and the
  learner can say, in their own words, what failed and why. If the learner
  cannot, re-teach from the failing test, not from the solution.
- **How to use `verify.py`:** the learner's command is plain
  `python verify.py` — it runs the suites, prints per-checkpoint status
  and earned claim codes, and exits non-zero while the gated checkpoints
  (l03, l04) are still open. `starter --expect-failure` and `solution`
  remain maintainer checks. "Done" means the default command shows every
  gate `[passed]` after the learner's bounded change.- **Honesty rules:** say what you did not verify. Do not claim the code is
  production-ready. Do not promise learning or career outcomes.

## What this course does NOT cover

Installing Claude Code, prompt tricks, multi-file architecture, pandas or
real Excel (`.xlsx`) files, deployment, or selling anything. For those, the
companion repository has guides and playbooks — link, don't improvise.


## Badge contract

- Badge: **Reproduce the failure Badge** (badge id `course-claude-code`) - earned by claiming all five checkpoints.
- Challenges: L01-L05 checkpoints, 10 points each; +50 course-badge bonus when all five are claimed on flypython.com.
- Evidence: `python verify.py` - L03 (bounded change) and L04 (verify & review) are objectively gated by the suite; L01/L02/L05 are learner-attested.
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
