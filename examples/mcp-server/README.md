---
id: example-mcp-server
type: example
title: Model Context Protocol (MCP) Tool Server
summary: Build a stateless 2026-07-28 MCP tool server with JSON-RPC 2.0 dispatch, no initialize handshake, schema validation, error isolation, and the input_required round-trip.
lang: en-US
content_version: 2
status: reviewed
reviewed_on: 2026-09-06
---

# Model Context Protocol (MCP) Tool Server

The Model Context Protocol (MCP) connects AI models and agents to external tools and data.
The 2026-07-28 specification is stateless-first: the `initialize` handshake and
`Mcp-Session-Id` sessions were removed, requests self-describe their protocol version
through `_meta`, and server-initiated elicitation was replaced by a multi-round-trip
`input_required` flow.

A production MCP server under this specification must parse standard JSON-RPC 2.0
requests, answer `tools/list` and `tools/call` directly without any prior handshake,
validate arguments, handle execution errors gracefully, and let a tool request additional
client input through a result with `resultType: "input_required"` that the client
completes by retrying the same call with `inputResponses`.

```bash
python examples/mcp-server/verify.py starter --expect-failure
python examples/mcp-server/verify.py solution
```

The first command reports the expected failure from the naive starter.
The second verifies the compliant solution. Give [TASK.md](TASK.md) to a coding agent,
ask it to fix only `starter/mcp_server.py`, and run:

```bash
python examples/mcp-server/verify.py starter
```

For the full migration background — what was removed, deprecated, and hardened in
2026-07-28 — read [Migrate a Python MCP server to the 2026-07-28 specification](../../guides/mcp/migrate-2026-07-28.md).
