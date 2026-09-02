# Playbooks

Playbooks turn recurring Python work into reviewable steps with an explicit
definition of done.

| Task | Use it when | Proof of completion |
| --- | --- | --- |
| [Fix a bug with a regression test](fix-a-bug/README.md) | Behavior is wrong or has regressed | Reproduction fails before the fix and passes after it |
| [Add or change an API](add-an-api/README.md) | A public HTTP or library contract changes | Contract, errors, tests, and compatibility are verified |
| [Integrate an external API](integrate-an-external-api/README.md) | Python calls a third-party service or model | Timeouts, failures, credentials, and test doubles are covered |
| [Upgrade dependencies](upgrade-dependencies/README.md) | Runtime or packages need updating | Lockfile, tests, advisories, and runtime smoke check pass |
| [Ship a release](ship-a-release/README.md) | A package or service is ready to publish | Artifact, changelog, deployment, and rollback are verified |

[中文索引](README_cn.md)
