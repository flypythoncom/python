---
id: product-slug-example
type: example
title: Three-minute AI-coding change
summary: Reproduce a Python text-boundary bug, make a bounded fix, and verify it with the standard library.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Three-minute AI-coding change

This exercise shows the full evidence chain: a contract, a failing example, a
bounded implementation, and an automated check. It needs only Python 3.11+.

```bash
python examples/product-slug/verify.py starter --expect-failure
python examples/product-slug/verify.py solution
```

The first command must report an expected failure; the second must pass four
tests. Then give [TASK.md](TASK.md) to a coding agent, ask it to edit only
`starter/product_slug.py`, and run:

```bash
python examples/product-slug/verify.py starter
```

Compare the patch with `solution/product_slug.py`. The goal is not to reproduce
the same syntax; it is to satisfy the same contract with a small, readable diff.
