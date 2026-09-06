---
id: structured-pipeline-example
type: example
title: Resilient batch data pipeline
summary: Build an isolated, bounded data batch processing pipeline with error recovery using the standard library.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Resilient batch data pipeline

This exercise demonstrates handling batches of semi-structured input safely: isolating failures, validating field types, and generating structured summaries without crashing. It needs only Python 3.11+.

```bash
python examples/structured-pipeline/verify.py starter --expect-failure
python examples/structured-pipeline/verify.py solution
```

The first command must report expected failure (unhandled exceptions, missing batch guardrails); the second must pass all tests.
Then provide [TASK.md](TASK.md) to your coding agent (Cursor, Windsurf, Claude Code) and ask it to fix `starter/pipeline.py`.
Verify with:

```bash
python examples/structured-pipeline/verify.py starter
```
