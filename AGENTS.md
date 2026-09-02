# FlyPython repository guide

## Mission

This repository is the broad, community-maintained data catalog behind
FlyPython. It is not a website. Keep `flypython.com` focused on editorial
learning paths, task playbooks, and presentation; keep this repository focused
on reviewed catalog data, its public JSON contract, and its contribution
workflow.

## Content rules

- Prefer official documentation and primary sources.
- Every catalog entry must include a stable ID, path, path-local order, source
  type, level, rationale, review date, status, and any key or safety requirements.
- Do not call a project production-ready without current maintenance, licensing,
  security, and adoption evidence.
- Do not use an LLM or web-search API to generate resource descriptions.
  Descriptions and classifications require human review.
- Keep English and Chinese website output generated from the same canonical
  resource data. Do not hand-copy catalog content into website source files.
- Treat HTTP 403, 429, and transient 5xx responses as review-needed states, not
  automatic proof that a resource is broken.

## Change workflow

- Work on a feature branch and preserve unrelated contributor changes.
- Run the repository validation workflow before committing.
- Regenerate `catalog.json` after source changes and verify it with
  `python tools/export_catalog.py --check`.
- Website consumers must pin a full repository commit and verify the catalog
  checksum. Do not make production builds depend on a moving branch.
- Keep external-link checks read-only, rate-limited, retryable, and blocked from
  private or loopback network targets.
- Do not add API keys, tokens, analytics IDs, or generated reports to git.
- After merge, verify the immutable raw `catalog.json`. Verify flypython.com only
  after a separate, deliberate consumer-version update.

## Review priorities

1. Content accuracy and source quality.
2. Deterministic export and bilingual parity.
3. Schema, consumer-contract, and safe link checks.
4. Clear contribution and licensing boundaries.
