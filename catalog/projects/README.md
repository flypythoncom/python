# Python Project Radar

FlyPython recommends current Python projects only after a maintainer reviews
the project’s source, maintenance state, license, documentation, release
history, and practical user value. This directory is intentionally not seeded
with unverified or AI-generated recommendations.

## Reviewed Projects Radar

| Project | Category | Status | Primary Rationale & Evidence | Risk / Safety Note | Review Date |
| --- | --- | --- | --- | --- | --- |
| [uv](https://github.com/astral-sh/uv) | Tooling & Packaging | `stable` | Extremely fast Cargo/Rust-based package and project manager. Replaces pip, pip-tools, venv, and pyenv with lockfile determinism. | Actively maintained by Astral; requires trusting binary wheels. | 2026-09-02 |
| [ruff](https://github.com/astral-sh/ruff) | Code Quality | `stable` | 10-100x faster linter and formatter. Unifies Flake8, Black, isort, and pyupgrade rules into a single config. | Drop-in Black compatibility; syntax parse differences are rare. | 2026-09-02 |
| [fastapi](https://github.com/fastapi/fastapi) | Web & APIs | `stable` | Production-standard ASGI framework with automatic OpenAPI docs, Pydantic validation, and dependency injection. | Ensure background tasks handle errors properly; use async endpoints responsibly. | 2026-09-02 |
| [pydantic-ai](https://github.com/pydantic/pydantic-ai) | AI Agents | `rising` | Model-agnostic agent framework prioritizing type-safe structured outputs, dependency injection, and testability. | Rapidly evolving API surface; pin minor versions. | 2026-09-02 |
| [instructor](https://github.com/jxnl/instructor) | AI Tools | `stable` | Production standard for extracting structured JSON from LLMs using Pydantic models with retry validation. | Requires API keys for target LLM providers. | 2026-09-02 |
| [polars](https://github.com/pola-rs/polars) | Data & Pipelines | `stable` | High-performance DataFrame library built in Rust on Apache Arrow with lazy query optimization. | API differs from pandas; memory layout is columnar. | 2026-09-02 |
| [marimo](https://github.com/marimo-team/marimo) | Interactive Notebooks | `rising` | Reactive, pure-Python notebook stored as standard executable `.py` files with deterministic state execution. | Requires modern browser environment; replaces Jupyter workflow. | 2026-09-02 |

## Submission & Lifecycle States

Use the [project proposal form](../../.github/ISSUE_TEMPLATE/project-proposal.yml)
to suggest a project. An accepted record will use one of these lifecycle states:
`new`, `rising`, `stable`, `major-update`, `experimental`, or `archived`. “New”
describes a recent reviewed discovery, not an unverified quality claim.
