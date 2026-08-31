# FlyPython repository guide

## Mission

This repository is the broad, community-maintained resource catalog behind
FlyPython. Keep `flypython.com` focused on editorial learning paths and a small
featured set; keep this repository focused on the larger reviewed catalog and
its contribution workflow.

## Content rules

- Prefer official documentation and primary sources.
- Every catalog entry must include a stable ID, path, source type, level,
  rationale, review date, status, and any key or safety requirements.
- Do not call a project production-ready without current maintenance, licensing,
  security, and adoption evidence.
- Do not use an LLM or web-search API to generate resource descriptions.
  Descriptions and classifications require human review.
- Keep English and Chinese pages generated from the same canonical resource
  data. Do not hand-copy the full catalog into multiple Markdown files.
- Treat HTTP 403, 429, and transient 5xx responses as review-needed states, not
  automatic proof that a resource is broken.

## Change workflow

- Work on a feature branch and preserve unrelated contributor changes.
- Run the repository validation workflow before committing.
- Keep external-link checks read-only, rate-limited, retryable, and blocked from
  private or loopback network targets.
- Do not add API keys, tokens, analytics IDs, or generated reports to git.
- After merge, verify the GitHub Pages deployment and the production domain.

## Review priorities

1. Content accuracy and source quality.
2. Deterministic generation and bilingual parity.
3. Build, schema, link, accessibility, and SEO checks.
4. Clear contribution and licensing boundaries.
