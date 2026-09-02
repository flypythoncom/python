---
id: example-async-fetcher
type: example
title: Async Batch Fetcher with Bounded Concurrency and Retries
summary: Implement a resilient async task batcher with Semaphore concurrency control, exponential backoff, and error isolation.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Async Batch Fetcher with Bounded Concurrency and Retries

Unbounded async concurrency (`asyncio.gather`) leads to socket exhaustion, 429 rate-limiting,
and cascading server failures. A production batch fetcher must constrain concurrency with a
Semaphore, retry transient failures (429, 503, timeouts) with backoff, fail fast on permanent
errors (400, 404), and isolate individual item failures from crashing the batch.

```bash
python examples/async-fetcher/verify.py starter --expect-failure
python examples/async-fetcher/verify.py solution
```

The first command reports expected failures from the naive starter.
The second verifies the resilient solution. Give [TASK.md](TASK.md) to a coding agent,
ask it to fix only `starter/fetcher.py`, and run:

```bash
python examples/async-fetcher/verify.py starter
```
