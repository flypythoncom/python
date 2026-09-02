---
id: example-pydantic-validation
type: example
title: Validate Untrusted Boundary Payloads
summary: Parse, sanitize, and validate messy external payloads with field normalization and structured error contracts.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Validate Untrusted Boundary Payloads

External payloads from webhooks, mobile clients, and LLM tool calls are untrusted.
They frequently arrive with mixed camelCase and snake_case keys, dirty currency strings,
or invalid enum states. A production boundary validator must sanitize valid variations
and return structured errors without crashing.

```bash
python examples/pydantic-validation/verify.py starter --expect-failure
python examples/pydantic-validation/verify.py solution
```

The first command reports the expected failures from the naive starter.
The second verifies the robust solution. Give [TASK.md](TASK.md) to a coding agent,
ask it to fix only `starter/validator.py`, and run:

```bash
python examples/pydantic-validation/verify.py starter
```
