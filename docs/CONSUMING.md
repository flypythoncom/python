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

Both current exports have `schema_version: 1`. They are described by
[`schema/catalog-v1.schema.json`](../schema/catalog-v1.schema.json) and
[`schema/content-manifest-v1.schema.json`](../schema/content-manifest-v1.schema.json).

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
