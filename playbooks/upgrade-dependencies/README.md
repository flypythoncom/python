---
id: upgrade-python-dependencies
type: playbook
title: Upgrade Python Dependencies
summary: Upgrade dependencies in a bounded change with lockfile, compatibility, security, and runtime evidence.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Upgrade Python Dependencies

1. Define the package range, reason, supported Python versions, and rollback.
2. Read upstream release notes and security advisories; identify breaking or
   deprecated behavior before changing the lockfile.
3. Update only the intended direct dependencies and review transitive changes.
4. Run formatting, types, tests, build, and a real runtime smoke check.
5. Review dependency provenance, install scripts, licenses, artifact size, and
   newly requested permissions.
6. Record the resolved versions and user-visible impact. Keep unrelated upgrades
   out of the same change.
