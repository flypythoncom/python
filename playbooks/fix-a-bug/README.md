---
id: fix-a-python-bug
type: playbook
title: Fix a Python Bug with a Regression Test
summary: Reproduce the behavior, constrain the cause, make the smallest fix, and prove the regression stays fixed.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Fix a Python Bug with a Regression Test

1. Record the observed behavior, expected behavior, smallest input that fails,
   and affected user path in a [task contract](../../templates/TASK_CONTRACT.md).
2. Add one test that fails for the reported reason. If it does not fail before
   the change, it is not yet regression evidence.
3. Ask the coding agent to inspect the call path and propose the smallest
   plausible cause. Do not authorize an unrelated refactor.
4. Change only the behavior required by the contract. Preserve public error
   forms unless the contract explicitly changes them.
5. Run the new test, the nearest test suite, then the full deterministic suite.
6. Review the diff for widened scope, hidden exception handling, new network or
   filesystem effects, and missing edge cases.
7. Re-run the original user path and record commands and results in the
   [verification template](../../templates/VERIFICATION.md).

Practice the complete loop with the
[product slug example](../../examples/product-slug/README.md).
