---
id: course-da-visualization
type: course
title: Data Visualization with an Agent
summary: Challenge course — turn a clean sales dataset into three spec'd charts plus a summary.json whose numbers are verified against the data. Charts must be generated from data, never hardcoded.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-da-visualization
  name_en: Visualization Challenger
  name_zh: 可视化挑战者
  requires: All five checkpoints claimed (L01–L05)
course_id: course-da-visualization
---

# Data Visualization with an Agent

> TL;DR: challenge course — you solve, the agent is your tool. Turn
> `scenario/sales-clean/sales_daily.csv` into three spec'd PNG charts and
> a `summary.json`. Verification checks the files exist, are valid PNGs,
> and that the numbers match the dataset. It does **not** judge
> aesthetics — say so honestly anywhere you show the output.

## What you build

A matplotlib script that produces `out/revenue_by_region.png`,
`out/daily_revenue.png`, `out/revenue_histogram.png`, and
`out/summary.json` — the machine-checkable half of "here are my charts".

## Setup

```bash
cd courses/da-visualization
uv sync            # pandas + matplotlib (or: pip install -r requirements.txt)
```

## Challenges (checkpoints)

| # | Challenge | Gate |
| --- | --- | --- |
| L01 | A chart is packaged evidence — what does each chart claim? | self-attested |
| L02 | Spec first — write down which numbers each chart must show | self-attested |
| L03 | Three charts and a summary — implement the contract | objective (starter suite) |
| L04 | Numbers match the charts — both suites green | objective (both suites) |
| L05 | Honest boundary — what verification cannot see | self-attested |

## Badge contract

- Badge: **Visualization Challenger** (badge id `da-visualization`) —
  all five checkpoints claimed.
- Challenges: L01–L05, 10 points each; +50 course-badge bonus on
  flypython.com.
- Evidence: `python verify.py progress` — L03/L04 objective, L01/L02/L05
  attested. Self-reported evidence, never a certificate.

## What this course does NOT cover

Chart design, dashboards, seaborn/plotly, interactive charts. The Agg
backend is deliberate: charts are evidence artifacts, not a UI.

## Folder map

```
COURSE.md / COURSE_cn.md   this file (EN / 中文)
lessons/L01.md … L05.md    challenge notes (each has an _cn.md pair)
scenario/sales-clean/      sales_daily.csv (clean input)
TASK.md / TASK_cn.md       the contract
starter/charts.py          unfinished implementation
solution/charts.py         reviewed solution
tests/test_charts.py       contract suite (read-only)
verify.py                  objective pass/fail + claim codes
requirements.txt           pinned pandas + matplotlib
REVIEW.md                  maintainer run-through record
```

Code is MIT-licensed; prose is CC BY 4.0 (see repository `LICENSE`).
