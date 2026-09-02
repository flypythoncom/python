---
id: python-modern-typing
type: guide
title: Modern Python Typing in Practice
summary: Use explicit Python types as machine-checkable contracts for reliable AI-assisted engineering.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Modern Python Typing in Practice

In the AI-coding era, type hints are not cosmetic annotations. They serve as
machine-readable boundary contracts that constrain LLM code generation and catch
regressions before execution.

## 1. Structural subtyping with Protocol

Avoid rigid inheritance hierarchies for test doubles and service adapters.
Use `typing.Protocol` to define lightweight behavioral interfaces:

```python
from typing import Protocol

class DataRepository(Protocol):
    def get_by_id(self, item_id: str) -> dict | None: ...
    def save(self, item_id: str, data: dict) -> None: ...
```

A mock class or real database driver satisfies `DataRepository` without subclassing,
making unit tests fast and decoupling domain logic from storage implementations.

## 2. Strong boundary contracts with TypedDict and Pydantic

When dealing with untrusted JSON from external APIs, use `typing.TypedDict` for internal
shapes and [Pydantic documentation](https://pydantic.dev/docs/validation/latest/get-started/)
models for boundary deserialization and validation.

```python
from typing import TypedDict

class UserProfile(TypedDict):
    user_id: int
    username: str
    is_active: bool
```

## 3. Generic types for reusable containers

Use `typing.TypeVar` or modern PEP 695 generics (`class Container[T]: ...` in Python 3.12+)
to retain type safety through caches, queues, and API wrappers rather than falling back to `Any`.

## 4. Static verification in development and CI

Type annotations provide value only when enforced. Run static type checkers like
[Mypy documentation](https://mypy.readthedocs.io/en/stable/) or Pyright in your CI pipeline,
and configure pre-commit hooks to block untyped public APIs.

Refer to the official [Python typing documentation](https://typing.python.org/en/latest/)
for authoritative reference on Python's type system specifications.
