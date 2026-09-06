# Guides

Guides explain the engineering decisions behind reliable Python products. Start
with the outcome you need:

- [Use Python well with AI Coding](ai-coding/workflow.md): give a coding agent enough context, constrain the change, test behavior, and review side effects.
- [Context budgeting and bounded tasks](ai-coding/context-budget.md): maximize agent accuracy with strict attention budgeting, clear contracts, and automated verification.
- [Build a Python product that can be changed safely](python-engineering/product-quality.md): turn a script into a product with contracts, boundaries, observability, and a release path.
- [Modern Python typing in practice](python-engineering/modern-typing.md): use Protocol, TypedDict, generics, and static type checking as machine-enforced contracts.
- [Reliable async Python patterns](python-engineering/async-patterns.md): avoid event loop blocking, leverage TaskGroup, and manage concurrency with Semaphore.
- [Migrate a Python MCP server to 2026-07-28](mcp/migrate-2026-07-28.md): remove the initialize handshake, adopt the input_required round-trip, and drop deprecated features.

For task-sized instructions, use the [playbooks](../playbooks/README.md). For
code you can run immediately, use the [examples](../examples/README.md).

[中文索引](README_cn.md)
