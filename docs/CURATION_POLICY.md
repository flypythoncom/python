# FlyPython curation policy

This policy defines what belongs in the FlyPython catalog, what evidence a
resource needs, and how maintainers review changes. It is the reference for
resource proposals and catalog pull requests.

## Scope

FlyPython catalogs durable resources for Python learning and Python-based AI
agent development. The catalog favors material that helps readers build skills
or use a maintained tool safely. It is not a general link directory, product
launch feed, or hosting location for unrelated applications.

Current learning paths are:

- `foundations`
- `web-apis`
- `automation`
- `ai-agents`

## Source priority

Review sources in this order:

1. Official documentation
2. Official standards
3. Official project repositories or sites

The current `source_type` values are `official-docs`, `official-standard`, and
`official-project`. A new source type requires a schema and policy change in
the same pull request.

Secondary tutorials, affiliate pages, copied lists, thin SEO pages, and
unmaintained mirrors are excluded unless the policy is deliberately expanded.

## Required catalog fields

`_data/resources.yml` is the canonical source. It contains a `catalog` object
and a `resources` list.

The `catalog` object records:

- `reviewed_on`
- `status`
- `paths`, where every path has `id`, `title_en`, `title_zh`, `summary_en`,
  `summary_zh`, and `order`

Every resource records:

- Identity: `id`, `path`, `title`, `url`
- Classification: `source_type`, `level`, `language`
- Editorial rationale: `why_en`, `why_zh`
- Review state: `reviewed_on`, `status`
- Access and safety: `requires_key`, `risk`
- Editorial selection: `featured`

Allowed classifications are:

| Field | Values |
| --- | --- |
| `path` | `foundations`, `web-apis`, `automation`, `ai-agents` |
| `source_type` | `official-docs`, `official-standard`, `official-project` |
| `level` | `beginner`, `intermediate`, `advanced`, `all-levels` |
| `language` | `en`, `zh`, `multilingual` |
| `status` | `active` |
| `risk` | `low`, `medium` |
| `requires_key`, `featured` | Boolean |

IDs must be stable, lowercase, and unique. A rename needs an explicit migration
plan because external links or generated anchors may depend on the old ID.
Review dates use ISO `YYYY-MM-DD` format.

## Acceptance criteria

A resource is eligible when all of these are true:

- Its URL is canonical and controlled by the official publisher or project.
- Its purpose fits one learning path.
- The English and Chinese rationales are factual, specific, and human-reviewed.
- Access requirements, API keys, paid tiers, and material safety risks are
  represented accurately.
- Its license and ownership are clear enough for the claims the catalog makes.
- The maintainer can verify the resource on the stated review date.

Do not describe a project as production-ready without current maintenance,
licensing, security, and adoption evidence. Popularity alone is not enough.

## Editorial rules

Write short, original rationales that explain why the resource is useful in its
assigned path. Do not copy marketing claims or large passages from the source.
Do not use an LLM or web-search API to generate descriptions or classifications.
A human reviewer remains responsible for each statement.

English and Chinese views must come from the same catalog record. A translation
should preserve the meaning and limits of the source, not add new claims.

Self-promotion must be disclosed. Maintainers assess it under the same criteria
as every other proposal.

## Link verification

Internal validation runs on every pull request. External-link fetching runs only
on the scheduled or manually dispatched GitHub Actions workflow.

A 404 or 410 from the canonical resource is strong removal evidence. A 403, 429,
timeout, or transient 5xx is a review-needed result, not proof that the resource
is gone. DNS, connection, TLS, invalid-URL, and redirect-protocol failures make
the automated audit fail, but they are still not enough on their own to remove a
resource. Retry with rate limits and record the observation date. Link checks
must refuse private, loopback, link-local, multicast, cloud-platform, and cloud
metadata targets, including redirect destinations.

## Review cadence and removal

Run the external-link audit weekly. Perform an editorial review when a resource
changes ownership, becomes unmaintained, introduces a material safety concern,
or receives a substantiated report.

Remove a resource when it is permanently unavailable, outside the catalog scope,
materially misleading, malicious, or no longer meets the acceptance criteria.
The pull request should preserve the reason and evidence in its description.
Do not silently replace a resource with an unrelated alternative under the same
stable ID.

## Permissions and attribution

This repository currently does not grant a general license to reuse its content
or code. Public visibility is not permission to copy, redistribute, or relicense
repository material. Contributors must submit only material they have the right
to submit and must preserve required notices.

Third-party content keeps its original terms. A catalog entry may link to and
factually describe a third-party resource, but it must not copy or relicense that
resource.
