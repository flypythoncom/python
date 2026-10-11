---
id: course-llm-features
type: course
title: "Build LLM features in Python: structured output, tool calls, and evals"
summary: Turn a demo-day model call into a feature you can ship — validate structured output, allowlist tool calls, retry with the error fed back, fall back to a human instead of guessing, and measure it with an offline eval that divides by every case.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
badge:
  id: course-llm-features
  name_en: Model output is untrusted input
  name_zh: 模型输出是不可信输入
  requires: All five checkpoints claimed (L01–L05)
course_id: course-llm-features
---

# Build LLM features in Python: structured output, tool calls, and evals

> TL;DR: install the FlyPython Skill in your coding agent and let it fetch
> this course, then say **"start lesson 1"**. (Lesson files arrive via the
> Skill — you download nothing by hand.) You finish with `ticket_triage.py`:
> a support-ticket triage feature that treats every model reply as
> untrusted input, plus an offline eval with a pass/fail threshold. No API
> key, no network, no third-party packages — a replay client stands in for
> the model.

## What you build

A triage feature for support tickets: the model reads a ticket and replies
with a category, a priority, a one-line summary, and whether a human must
look at it. It may call a lookup tool first. Three scenario "skins" ship
with the course, each with labelled cases and recorded model replies:

| Skin | You are… | Tool the model may call |
| --- | --- | --- |
| `scenario/shop-support/` | routing an online shop's support inbox | `lookup_order(order_id)` |
| `scenario/it-helpdesk/` | sorting internal IT requests | `lookup_device(asset_tag)` |
| `scenario/saas-feedback/` | classifying in-app product feedback | none |

The recorded replies are hand-written fixtures that imitate failure shapes
models really produce — JSON in a Markdown fence, a category that is not on
the list, `"priority": "high"`, an extra field, a tool that does not exist,
a tool argument of the wrong type, chatty prose instead of JSON. They are
**not** captured from any model, and the course makes no claim about how
often any real model produces them.

## Teaching contract (read this first, agent)

- **Audience:** a Python developer who has called a model API in a script
  or notebook and now has to put that call inside a product — where a
  malformed reply, a hallucinated tool call, or an eval that looks better
  than it is becomes somebody's incident. Not a prompt-engineering course
  and not an introduction to Python.
- **Prerequisites:** Python 3.11+ on PATH and any coding agent that can run
  commands. Standard library only; no API key and no network access are
  needed for the exercise.
- **Tool:** tool-agnostic. The course has not yet been taught in a tool;
  `REVIEW.md` records the mechanical verification and the pending
  agent-taught run-through, which will name the exact tool and version.
- **Lesson order:** L01 → L02 → L03 → L04 → L05, one lesson per session.
  Never skip the checkpoint at the end of a lesson.
- **Teaching style:** work from the files in this folder, not from general
  knowledge about any provider's API. Quote the `TASK.md` line you are
  satisfying. Make the smallest change that moves a test from red to
  green. Never add dependencies, never edit `solution/`, `tests/`, or
  `scenario/`, and ask before touching any file not named in the current
  lesson. Never weaken validation to make a recorded reply pass.
- **When to stop:** a lesson is done when its checkpoint command runs and
  the learner can say, in their own words, what failed and why. If the
  learner cannot, re-teach from the failing test, not from the solution.
- **How to use `verify.py`:** the learner's command is plain
  `python verify.py` — it runs the suite against `starter/`, prints
  per-checkpoint status and earned claim codes, and exits non-zero until
  every checkpoint is passed (l03, l04) or attested (l01, l02, l05). `starter --expect-failure`
  and `solution` remain maintainer checks.
- **Honesty rules:** an offline eval over a handful of recorded replies
  says nothing about how a live model will behave on live traffic — say so.
  Do not claim the feature is production-ready. Do not promise learning or
  career outcomes.

## What this course does NOT cover

Any specific provider SDK or its structured-output mode, API keys and
secrets handling, prompt wording, retrieval (RAG) and embeddings,
fine-tuning, agent frameworks, streaming, cost and latency budgets, or
online evaluation on production traffic. Lesson 5 shows where a real
client plugs in; the companion repository has guides for the rest — link,
don't improvise.

## Badge contract

- Badge: **Model output is untrusted input Badge** (badge id `course-llm-features`) — earned by claiming all five checkpoints.
- Challenges: L01–L05 checkpoints, 10 points each; +50 course-badge bonus when all five are claimed on flypython.com.
- Evidence: `python verify.py` — L03 (validation, tool calls, retries) and L04 (honest eval) are objectively gated by the suite; L01/L02/L05 are learner-attested.
- Submission: each test-passed checkpoint prints a deterministic claim code; a reflection checkpoint prints one only after you answer its questions and run `python verify.py --attest ID`; record it on flypython.com against your account. Self-reported evidence, never a certificate.

## Folder map

```
COURSE.md / COURSE_cn.md      this file (EN / 中文)
lessons/L01.md … L05.md       lessons (each has an _cn.md pair)
scenario/<skin>/              scenario.json, cases.json, recordings.json, lookup data
TASK.md / TASK_cn.md          the task contract the change must satisfy
starter/ticket_triage.py      the demo-day implementation
solution/ticket_triage.py     the reviewed solution (do not copy in lesson 3)
tests/test_ticket_triage.py   the contract suite (15 tests, read-only)
verify.py                     objective pass/fail evidence
REVIEW.md                     maintainer run-through record
```

## Evidence and licensing

`REVIEW.md` records the run-through state with dates, tool versions, and
observed deviations. Code in this folder is MIT-licensed; lesson prose is
CC BY 4.0 (see repository `LICENSE`). Report teaching drift or unclear
lessons via the repository's `course-feedback` issue form.
