# AI Coding Agent Rules (Cursor / Windsurf / Copilot / Claude)

## Core Working Rules

1. **Explicit Boundaries**: Do not modify files outside the specific task scope.
2. **Contract First**: Read existing type definitions, schemas, and test assertions before proposing changes.
3. **No Phantom Code**: Every code modification must be backed by an executable test or verifier command.
4. **Preserve Integrity**: Do not delete unrelated comments, docstrings, or formatting unless explicitly requested.
5. **Standard Tooling**: Prefer modern standard tooling (Python 3.11+, uv, pytest, ruff, mypy).

## Change Verification Protocol

Before declaring a task done:
1. Run local tests: `pytest`
2. Run static analysis: `ruff check` and `mypy`
3. Verify git diff: Ensure zero unintended side effects or modified global state.
