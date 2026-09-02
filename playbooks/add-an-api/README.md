---
id: add-a-python-api
type: playbook
title: Add or Change a Python API
summary: Define the public contract first, then implement and verify success, error, and compatibility behavior.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Add or Change a Python API

1. Write request, response, status, authentication, idempotency, and error
   contracts before selecting implementation details.
2. Separate domain logic from transport code; validate data at the boundary.
3. Add contract tests for one success, each meaningful failure, permissions,
   and malformed input. Test generated schemas when clients depend on them.
4. Decide whether the change is additive, deprecating, or breaking. Document a
   migration path for every breaking change.
5. Apply explicit timeouts and cancellation to downstream calls. Do not expose
   provider errors or secrets directly to clients.
6. Verify the API through the same network boundary a real client uses, then
   inspect logs and state changes.
