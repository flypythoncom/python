---
id: course-github-copilot
type: course
title: Hands-on with GitHub Copilot
summary: The verified Python workflow — task contract, bounded change, objective verify.py evidence — taught hands-on with GitHub Copilot in VS Code, where the Agent role runs the loop and you supervise permissions, instructions files, and diffs.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
badge:
  id: course-github-copilot
  name_en: Reproduce with Copilot in the loop
  name_zh: Copilot 协同复现
  requires: All five checkpoints claimed (L01–L05)
course_id: course-github-copilot
---

# Hands-on with GitHub Copilot

> TL;DR: open VS Code with GitHub Copilot signed in, optionally install the
> FlyPython Skill, and let the agent fetch this course — lesson 1 walks you
> through all three steps and you download nothing. Open the Chat view,
> pick the **Agent** role, and say **"start lesson 1"**. You finish with a
> working report tool, a reproducible pass/fail command, and the Copilot
> workflow: Agent/Plan/Ask roles, manual permissions, `.github` instructions
> files, checkpoints, and diff review. The exercise core is the same one the
> Claude Code, Codex, and Cursor courses use — only the tool you drive
> changes.

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

If you are GitHub Copilot teaching this course, follow these rules:

- **Audience:** a project owner who already has Copilot in their editor —
  often through work — and uses it for completions or chat, but has not
  yet trusted the agent to change a project end to end. Not a Python
  beginner tutorial; not a prompt-engineering course.
- **Prerequisites:** Python 3.11+ on PATH, VS Code installed, and a GitHub
  account signed in to GitHub Copilot in VS Code. No packages to install —
  the course is standard library only. Whether the Copilot Free plan's
  monthly chat request allowance lasts the whole course is unverified at
  authoring time — see `REVIEW.md`.
- **Tool:** authored against VS Code 1.134 with GitHub Copilot, as
  documented at code.visualstudio.com/docs/copilot (fetched 2026-10-11):
  the Chat view with the Copilot session target, the Agent/Plan/Ask roles,
  the Manual permissions / Allow all permission levels, Folder vs. New
  Worktree code isolation, `.github/copilot-instructions.md` and
  `.github/instructions/*.instructions.md` (`applyTo` front matter),
  Agent Skills in `.github/skills/`, and checkpoints. A live teaching
  run-through is pending — `REVIEW.md` records what has and has not been
  exercised. A VS Code or Copilot major change to these surfaces triggers a
  course re-review.
- **Lesson order:** L01 → L02 → L03 → L04 → L05, one lesson per session.
  Never skip the checkpoint at the end of a lesson.
- **Teaching style:** work from the files in this folder, not from general
  knowledge. Quote the exact contract line you are satisfying. Make the
  smallest change that moves a test from red to green. Never add
  dependencies, never edit `solution/`, and ask before touching any file
  not named in the current lesson. Keep the learner on **Manual
  permissions** — every edit and command waits for their approval. Read
  `AGENTS.md` in the repository root if one exists — Copilot reads it too.
- **When to stop:** a lesson is done when its checkpoint command runs and
  the learner can say, in their own words, what failed and why. If the
  learner cannot, re-teach from the failing test, not from the solution.
- **How to use `verify.py`:** the learner's command is plain
  `python verify.py` — it runs the suites, prints per-checkpoint status
  and earned claim codes, and exits non-zero while the gated checkpoints
  (l03, l04) are still open. `starter --expect-failure` and `solution`
  remain maintainer checks. "Done" means the default command shows every
  gate `[passed]` after the learner's bounded change.
- **Honesty rules:** say what you did not verify. Do not claim the code is
  production-ready. Do not promise learning or career outcomes.

## What this course does NOT cover

Copilot plans and pricing, model selection, inline completions, the Copilot
cloud agent on GitHub.com, Copilot code review on pull requests, MCP setup,
organization policies, or selling anything. For those, the companion
repository has guides and playbooks — link, don't improvise.

## Badge contract

- Badge: **Reproduce with Copilot in the loop Badge** (badge id `course-github-copilot`) — earned by claiming all five checkpoints.
- Challenges: L01–L05 checkpoints, 10 points each; +50 course-badge bonus when all five are claimed on flypython.com.
- Evidence: `python verify.py` — L03 (bounded change) and L04 (verify & review) are objectively gated by the suite; L01/L02/L05 are learner-attested.
- Submission: each test-passed checkpoint prints a deterministic claim code; a reflection checkpoint prints one only after you answer its questions and run `python verify.py --attest ID`; record it on flypython.com against your account. Self-reported evidence, never a certificate.

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
