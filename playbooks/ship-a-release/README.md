---
id: ship-a-python-release
type: playbook
title: Ship a Python Release
summary: Produce a traceable package or service release and verify the real deployed behavior and rollback path.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Ship a Python Release

1. Select the exact commit; confirm tests, version, changelog, migrations,
   configuration, and compatibility from that commit.
2. Build artifacts once in a clean environment and inspect their contents.
3. Publish or deploy with least-privilege credentials. Record artifact digest,
   deployment identity, and configuration version.
4. Verify installation or the production user path, not merely command success.
5. Check health, logs, data changes, and critical integrations.
6. If acceptance fails, stop rollout and use the documented rollback. Announce
   availability only after the verified artifact is reachable.
