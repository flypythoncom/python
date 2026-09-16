---
id: course-da-eda
type: course
title: Exploratory Data Analysis with an Agent
summary: A challenge course — point your agent at a messy shop export and produce a verified EDA summary (results.json) whose numbers are checked against ground truth. First non-stdlib course in the catalog; pandas is managed with uv.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-da-eda
  name_en: EDA Challenger
  name_zh: 探索分析挑战者
  requires: All five checkpoints claimed (L01–L05)
course_id: course-da-eda
---

# Exploratory Data Analysis with an Agent

> TL;DR: this is a **challenge course** — you solve it, your agent is the
> tool. Point it at `scenario/shop-export/transactions.csv` (142 messy
> rows), implement the contract in `starter/eda.py`, and finish with a
> `results.json` whose numbers are objectively checked against ground
> truth. Optional guided mode: `COURSE.md` + `lessons/` still work as an
> agent-taught path if you want a tour instead of a challenge.

## What you build

A pandas script that loads a real-world-messy transactions export, cleans
it (duplicates, unparseable amounts, bad dates), and writes a verified
summary: clean row counts, total revenue, revenue by region, top category,
date range.

## Setup — lesson zero is the environment

This is the first course in the catalog that leaves the standard library:

```bash
cd courses/da-eda
uv sync            # or: pip install -r requirements.txt
```

`verify.py` checks for pandas and prints this hint if it is missing.

## Challenges (checkpoints)

| # | Challenge | Gate |
| --- | --- | --- |
| L01 | What messy data looks like — profile the CSV before touching code | self-attested |
| L02 | Define the answer first — write down the expected results.json shape | self-attested |
| L03 | Clean and summarize — implement `clean_transactions` + `summarize` | objective (starter suite) |
| L04 | Check against ground truth — both suites green | objective (both suites) |
| L05 | Run it on your own data — swap in an export you actually have | self-attested |

## Badge contract

- Badge: **EDA Challenger** (badge id `da-eda`) — earned by claiming all
  five checkpoints.
- Challenges: L01–L05, 10 points each; +50 course-badge bonus when all
  five are claimed on flypython.com.
- Evidence: `python verify.py` — L03 and L04 are objectively
  gated by the suite; L01/L02/L05 are learner-attested.
- Submission: each test-passed checkpoint prints a deterministic claim code; a reflection checkpoint prints one only after you answer its questions and run `python verify.py --attest ID`;
  record it on flypython.com against your account. Self-reported
  evidence, never a certificate.

## What this course does NOT cover

Visualization (see `da-visualization`), reporting (see `da-report`),
statistics theory, SQL, or notebooks. The dataset is synthetic but the
quality issues are the ones you will meet in real exports.

## Folder map

```
COURSE.md / COURSE_cn.md   this file (EN / 中文)
lessons/L01.md … L05.md    challenge notes (each has an _cn.md pair)
scenario/shop-export/      transactions.csv (messy input data)
TASK.md / TASK_cn.md       the contract your code must satisfy
starter/eda.py             the deliberately unfinished implementation
solution/eda.py            the reviewed solution
tests/test_eda.py          the contract suite (read-only)
verify.py                  objective pass/fail + claim codes
requirements.txt           pinned pandas dependency
REVIEW.md                  maintainer run-through record
```

## Evidence and licensing

Reviewed content: `REVIEW.md` records the run-through. Code is
MIT-licensed; lesson prose is CC BY 4.0 (see repository `LICENSE`).
