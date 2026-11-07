# Consuming FlyPython content

This repository owns the source content; flypython.com owns presentation,
navigation, search, and product conversion. A website release deliberately
pins one repository commit instead of maintaining an editable copy.

`catalog.json` is the stable machine-readable resource catalog. The website may
render path titles, summaries, resource rationales, levels, access requirements,
review dates, and safety metadata from the export.

`content-manifest.json` indexes reviewed first-party guides and playbooks with
localized titles, summaries, paths, versions, review dates, and SHA-256 hashes.
For example, the repository owns the paired AI-coding workflow sources:

- `guides/ai-coding/workflow.md`
- `guides/ai-coding/workflow_cn.md`

A website may render these Markdown files from the same pinned commit. It may
adapt navigation and presentation, but should not maintain a second editable
copy of their claims or steps.

## Pin an immutable revision

Consumers must use a full commit SHA:

```text
https://raw.githubusercontent.com/flypythoncom/python/<full-commit-sha>/catalog.json
```

Record the revision and checksum in the consumer repository:

```json
{
  "repository": "flypythoncom/python",
  "commit": "<full-commit-sha>",
  "catalogSha256": "<sha256>",
  "contentManifestSha256": "<sha256>"
}
```

Do not fetch `master` during a production build. A deliberate sync command
should download the pinned export, verify the checksum and schema version, and
write a generated local cache used by the normal website build. A failed sync
must leave the last accepted catalog unchanged.

## Contract

The current exports all have `schema_version: 1`. They are described by
[`schema/catalog-v1.schema.json`](../schema/catalog-v1.schema.json),
[`schema/content-manifest-v1.schema.json`](../schema/content-manifest-v1.schema.json),
and [`schema/radar-v1.schema.json`](../schema/radar-v1.schema.json)
(`radar.json`, the Project Radar export, is the third pinned artifact a
consumer should record alongside the other two).

- A schema-version change may require consumer code changes.
- A content-only change keeps the same schema version.
- Resource IDs are stable consumer keys.
- `order` is only meaningful within a resource's `path`.
- English and Chinese rationales come from the same resource record.
- Consumers may choose a subset, but must not silently rewrite catalog claims.
- Consumers should show `reviewed_on`, `requires_key`, and `risk` wherever those
  facts materially affect a user's decision.
- Consumers must verify every rendered first-party file against the checksum in
  `content-manifest.json` and use the matching locale rather than translating it.

## Update flow

1. Merge and validate a content or catalog change in this repository.
2. Regenerate and commit both affected JSON exports with the same change.
3. Select the exact merged commit and compute both export SHA-256 values.
4. Update the website's catalog lock and generated cache in one focused change.
5. Run website content, rendering, accessibility, and link checks.
6. Deploy the website and verify that it exposes the pinned catalog revision.

This keeps catalog review independent from website presentation while avoiding
two separately maintained copies of the same resource content.

## Course registry v1

`course-registry.json` is an additive public contract consumed at the same full
commit as the content manifest. It contains `courses` (English/Chinese website
metadata), `contracts` (course ID, public salt, ordered checkpoints, objective
gates and legacy aliases), and `agentToolCourseIds`. Public salts are not
secrets and claim codes remain self-reported evidence.

Edit `courses/<slug>/website.json` for display fields, ordering, aliases and
agent-tool classification. The schema is `schemas/course-website.schema.json`.
Manifest ID/version/review date come from COURSE.md; claim fields come from
literal verifier constants parsed with AST, never by executing the verifier.
Run `make generate PYTHON=.venv/bin/python`; CI fails on drift, missing metadata,
missing bilingual lessons, duplicate IDs/aliases or unsupported verifier gates.
The website owns Pro records and curated route allocation. New public courses
must have five checkpoints for the current website contract. Historical display
badge IDs are retained (some differ from the verifier course ID).

Coach P / 小P老师 is an AI teaching style executed by the learner's own agent
and model. Updated course editorial dates do not complete pending REVIEW.md
teaching trials. See the website 0.1.3 plan FP-1301/FP-1303 for the authorized scope.
