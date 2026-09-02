# Runnable examples

These examples are deliberately small. Each one has a task contract, a broken
starter, a completed solution, and a verifier so you can practice an AI-coding
loop without trusting generated code on sight.

- [Product slug regression](product-slug/README.md): reproduce a text-boundary bug, ask an agent for the smallest fix, and verify the solution. Standard library only; about three minutes.
- [Untrusted payload validation](pydantic-validation/README.md): handle messy camelCase and snake_case inputs, dirty amount strings, and structured error responses.
- [MCP tool server](mcp-server/README.md): build a standard JSON-RPC 2.0 Model Context Protocol tool server with schema validation and isolated runtime errors.
- [Async batch fetcher](async-fetcher/README.md): control concurrency with Semaphore, back off and retry transient HTTP failures, and collect structured results.

[中文索引](README_cn.md)
