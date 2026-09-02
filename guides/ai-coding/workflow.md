---
id: python-ai-coding-workflow
type: guide
title: Use Python Well with AI Coding
summary: A contract-first workflow for using coding agents to make small, testable, and safe Python changes.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Use Python Well with AI Coding

An AI coding agent can produce syntax and boilerplate quickly, but it does not
automatically understand project boundaries, the real runtime, user risk, or the
definition of done. Good AI coding is not about generating more code. It is
about turning work into small changes that are understandable, verifiable, and
safe to reverse.

Using AI coding and building an AI agent are different things. The first is a
development method; the second is only one kind of product you might build. The
same reliable workflow applies whether the outcome is an API, an automation
script, a data tool, or an agent system.

## 1. Give the task a contract

Before asking a coding agent to modify code, state:

- Outcome: what a user or system will be able to accomplish.
- Current behavior: what happens now.
- Inputs and outputs: formats, boundaries, and error forms.
- Scope: what may change and what must remain untouched.
- Acceptance: the tests, commands, or real actions that must pass.
- Authority: whether network access, dependency installation, commits, pushes,
  or deployments are allowed.

Reusable task template:

```text
Outcome:
Current behavior:
Expected behavior:
Allowed changes:
Out of scope:
Acceptance checks:
Commit/push/deploy authority:
```

An instruction such as “improve this” invites an oversized change. A concrete
contract lets the agent execute without guessing product decisions.

## 2. Require repository inspection first

A reliable Python change starts by checking:

1. `AGENTS.md`, `README.md`, and contribution rules.
2. The Git branch, worktree, and remote state.
3. `pyproject.toml`, the Python version, and dependency locks.
4. The implementation and tests closest to the requested behavior.
5. The real entry point: CLI, API route, job, or browser flow.

Do not let an agent infer implemented behavior from a README, TODO, or filename.
Documentation, code, tests, and runtime evidence must agree.

## 3. Make the Python environment reproducible

AI-generated code is useful only inside a reproducible environment:

- Pin the Python version.
- Use an isolated virtual environment.
- Declare direct dependencies and lock the full dependency graph.
- Do not rely on packages installed globally on one machine.
- Install and test once in a clean environment.

See the official [uv documentation](https://docs.astral.sh/uv/) for a modern
workflow and the [Python venv documentation](https://docs.python.org/3/library/venv.html)
for the underlying environment behavior.

## 4. Make the smallest verifiable change

Ask the coding agent to work at this granularity:

1. Identify one missing or failing behavior.
2. Define the test or observable acceptance point.
3. Change the smallest relevant set of files.
4. Run focused tests.
5. Run the complete affected test scope.
6. Check the diff for unrelated edits.

If a change cannot be summarized in one sentence, it can usually be split
again. Avoid combining an architecture refactor, dependency upgrade, copy
rewrite, and production release in one step.

## 5. Constrain generated code with types, validation, and tests

Python's dynamic nature supports fast work, but it also makes it easy to produce
plausible code with unclear boundaries. Prefer:

- [Python typing](https://typing.python.org/en/latest/) for function and module
  contracts.
- [Pydantic](https://pydantic.dev/docs/validation/latest/get-started/) for
  untrusted inputs.
- [pytest](https://docs.pytest.org/en/stable/) for successful, failing, and edge
  behavior.

Tests should cover normal input, missing or malformed input, timeouts, external
failures, insufficient permission, and side effects that must not occur.

A green test suite proves only that the checked behavior passed. It does not
prove that the requirement was correct or replace runtime acceptance.

## 6. Verify the real entry point

Run what the user will actually use:

- CLI: inspect exit status, standard output, and standard error.
- API: inspect requests, responses, status codes, timeouts, and validation.
- Web: use a real browser and inspect DOM, interaction, requests, and console.
- Automation: use harmless input and check retries, recovery, and idempotency.
- Agent: inspect tool arguments, structured output, permissions, traces, and
  failure boundaries.

Useful primary references include [HTTPX](https://www.python-httpx.org/),
[FastAPI](https://fastapi.tiangolo.com/), and
[Playwright for Python](https://playwright.dev/python/docs/intro).

## 7. Review side effects and authority separately

AI-generated Python often touches files, shells, browsers, networks, databases,
or model tools. Before accepting the change, confirm:

- File targets are precise and cannot overwrite broad user data.
- `subprocess` avoids unnecessary `shell=True` execution.
- Network calls have timeouts, bounded retries, and destination controls.
- Logs and errors do not expose credentials or private data.
- Database changes are auditable and recoverable.
- Agent tools use the least authority and request necessary confirmation.

See the standard-library documentation for
[subprocess](https://docs.python.org/3/library/subprocess.html) and
[pathlib](https://docs.python.org/3/library/pathlib.html).

## 8. Report evidence, not only completion

A complete handoff states:

- What changed and what did not.
- Which tests and acceptance actions actually ran.
- Which outcomes were verified and which remain unknown.
- Whether the work was committed, pushed, or deployed.
- The exact version that can be checked independently.

Recommended definition of done:

```text
[ ] The worktree contains only in-scope changes
[ ] Type, format, and unit checks pass
[ ] Failure paths and boundary inputs were exercised
[ ] The real CLI, API, or browser entry point was verified
[ ] File, network, credential, and database side effects were reviewed
[ ] Documentation matches current implementation
[ ] Commit, remote, and deployment versions can be compared exactly
```

## Next step

Use the repository README to choose primary sources for Python foundations,
Web/API work, automation, or AI-agent development. The catalog helps you choose
reliable context; this workflow helps you decide whether an AI-generated change
is safe to accept.
