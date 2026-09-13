---
id: course-da-report
type: course
title: From Analysis to Report with an Agent
summary: Challenge course — turn a verified EDA summary into a structured report (report.json + report.md) where every number traces back to its input. Verification checks structure and number consistency, not writing quality.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-da-report
  name_en: Report Challenger
  name_zh: 分析报告挑战者
  requires: All five checkpoints claimed (L01–L05)
course_id: course-da-report
---

# From Analysis to Report with an Agent

> TL;DR: challenge course — turn `scenario/analysis-pack/results.json`
> into `out/report.json` + `out/report.md`. The contract: every number in
> the report traces back to its input unchanged. Verification checks
> structure and numeric consistency; it does not grade prose.

## What you build

A report generator: load verified inputs → build a structured report
dict → render Markdown → write both artifacts. The structured JSON is
the auditable layer; the Markdown is for humans.

## Setup

```bash
cd courses/da-report
# Standard library only — nothing to install.
```

## Challenges (checkpoints)

| # | Challenge | Gate |
| --- | --- | --- |
| L01 | A report is a contract with the reader | self-attested |
| L02 | Structure before prose | self-attested |
| L03 | Build and render the report | objective (starter suite) |
| L04 | Numbers traceable to inputs | objective (both suites) |
| L05 | What report verification cannot see | self-attested |

## Badge contract

- Badge: **Report Challenger** (badge id `da-report`) — all five
  checkpoints claimed.
- Challenges: L01–L05, 10 points each; +50 course-badge bonus on
  flypython.com.
- Evidence: `python verify.py progress` — L03/L04 objective, L01/L02/L05
  attested. Self-reported evidence, never a certificate.

## What this course does NOT cover

Templates engines (Jinja), PDF export, styling, or editorial quality.
The suite verifies structure and numbers — good writing stays your job.

## Folder map

```
COURSE.md / COURSE_cn.md   this file (EN / 中文)
lessons/L01.md … L05.md    challenge notes (each has an _cn.md pair)
scenario/analysis-pack/    results.json (verified input)
TASK.md / TASK_cn.md       the contract
starter/report.py          unfinished implementation
solution/report.py         reviewed solution
tests/test_report.py       contract suite (read-only)
verify.py                  objective pass/fail + claim codes
REVIEW.md                  maintainer run-through record
```

Code is MIT-licensed; prose is CC BY 4.0 (see repository `LICENSE`).
