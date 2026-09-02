---
id: example-mcp-server
type: example
title: Model Context Protocol (MCP) Tool Server
summary: Build a safe, compliant JSON-RPC 2.0 MCP tool server with parameter validation and structured error boundaries.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Model Context Protocol (MCP) Tool Server

The Model Context Protocol (MCP) connects AI models and agents to external tools and data.
A production MCP server must parse standard JSON-RPC 2.0 requests, list available tool
schemas via `tools/list`, validate arguments, handle execution errors gracefully, and
prevent uncaught exceptions from breaking the communication stream.

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
