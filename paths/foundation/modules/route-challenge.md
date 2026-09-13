---
id: path-foundation-challenge
type: path
title: "Route challenge: dual-agent, double-verified"
summary: Foundation path capstone — run the same task through any two of the six path agents and verify both outputs yourself.
lang: en-US
content_version: 2
status: reviewed
reviewed_on: 2026-09-13
---

# Route challenge: dual-agent, double-verified

**Points:** 200 · **Type:** project · **Evidence:** objective (`verify.py`)

The final challenge of the Foundation path: prove you can drive **two
different** agents through the same task — and verify both results yourself.

## The task

Pick a real small task you care about (suggestion: "a CLI that counts the
lines, words, and bytes of a file" or reuse any scenario skin from the path
courses: `hands-on-python-with-claude-code`, `hands-on-with-openai-codex`,
`hands-on-with-cursor`, `hands-on-with-deepseek-harness`,
`hands-on-with-kimi-code`, `hands-on-with-zcode`, `agent-rules-single-source`,
`verifying-ai-generated-code`).

Choose **any two** of the six agent tools this path teaches (Claude Code,
Codex app, Cursor, DeepSeek Harness, Kimi Code, ZCode). Then:

1. **Round one — agent A.** In a fresh folder, write a `TASK.md`
   describing the contract (inputs, outputs, edge cases, done = tests pass),
   drive your first agent to implement it, and add a `verify.py`-style
   check that passes on the result.
2. **Round two — agent B.** Same task, fresh folder, same `TASK.md`.
   Drive a *different* agent to implement it independently — do not copy
   round one's code.
3. **Double verification.** Run your objective check against **both**
   implementations. Record what differed: structure, edge-case handling,
   test coverage, anything that surprised you.

## What to record

- Both folders kept intact (they are your evidence).
- A short note: which agent's output needed fewer corrections, and *why you
  believe that* — this is the skeptical-review habit from the
  `verifying-ai-generated-code` course applied across tools.

## Checkpoint

Complete when:

- Both implementations exist and your objective check passes on each.
- Your comparison note names at least one concrete difference with evidence
  (a file, a test, a command output).
- The two agents were genuinely different tools — not two sessions of the
  same one.

The claim for this challenge is recorded against the Foundation path badge —
200 points toward **Agent User**. Self-reported evidence, never a certificate.
