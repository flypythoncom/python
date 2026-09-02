---
id: write-llm-evals
type: playbook
title: Write Deterministic Evals for LLMs and Agents
summary: Build regression test suites for LLM prompt changes and tool-calling agents with golden datasets and schema assertions.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Write Deterministic Evals for LLMs and Agents

1. Curate a versioned golden dataset of real user inputs covering happy paths,
   adversarial prompts, ambiguous edge cases, and known regressions.
2. Define deterministic boundary assertions before adding semantic judges:
   validate JSON Schema conformity, required fields, and disallowed tokens.
3. Test tool-calling parameters against strict type contracts; assert that
   tool selections match expected capabilities without hallucinated arguments.
4. Separate cheap local unit tests from live model evaluations. Use recorded
   fixture responses for fast CI runs and run live evals on scheduled batches.
5. Record benchmark pass rates, token counts, and latency before and after
   any prompt or model migration. Never ship prompt changes without comparing diffs.
6. Guard against flaky evals by establishing tolerance thresholds and isolating
   temperature/seed parameters during regression checks.
