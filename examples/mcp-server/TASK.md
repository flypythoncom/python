# Task contract: stateless MCP JSON-RPC tool server (2026-07-28)

Change only `starter/mcp_server.py`.

- Implement `MCPServer` class:
  - `register_tool(name: str, description: str, schema: dict, handler: Callable) -> None`
  - `handle_request(request: dict) -> dict`: Processes a JSON-RPC 2.0 request dict and returns a response dict.
- JSON-RPC 2.0 compliance:
  - Must check `"jsonrpc": "2.0"` and preserve request `"id"`.
  - Return error `-32600` (Invalid Request) if request is not a valid dict or lacks `method` or `jsonrpc != "2.0"`.
  - Return error `-32601` (Method not found) if method is unknown.
- 2026-07-28 stateless behavior:
  - `initialize` must return `-32601` with a message noting it was removed by the stateless 2026-07-28 specification; there is no handshake before tool calls.
  - If a request carries `_meta.protocolVersion` and it is not `"2026-07-28"`, return `-32600` (Invalid Request); requests self-describe their version.
- Supported methods:
  - `"tools/list"`: returns `{"result": {"tools": [{"name": ..., "description": ..., "inputSchema": ...}, ...]}}`.
  - `"tools/call"`: accepts `params: {"name": ..., "arguments": ..., "inputResponses": {...}?}` and calls the handler as `handler(arguments, inputResponses)`.
    - If tool not registered: returns `{"result": {"isError": True, "content": [{"type": "text", "text": "Tool not found"}]}}`.
    - If required argument missing: returns `{"result": {"isError": True, "content": [{"type": "text", "text": "Missing required argument: <arg>"}]}}`.
    - If the handler raises `InputRequired(requests)`: returns `{"result": {"resultType": "input_required", "requests": <requests>, "content": [{"type": "text", "text": "Additional client input is required before this tool can finish."}]}}`. The client retries the same call with answers in `params.inputResponses`.
    - On handler success: returns `{"result": {"content": [{"type": "text", "text": str(output)}]}}`.
    - On any other handler exception: catch and return `{"result": {"isError": True, "content": [{"type": "text", "text": f"Error: {e}"}]}}`.
- Provide `InputRequired(Exception)` with a `requests` attribute so tools can request client input.

Done means `python examples/mcp-server/verify.py starter` exits successfully.
