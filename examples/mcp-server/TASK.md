# Task contract: minimal MCP JSON-RPC tool server

Change only `starter/mcp_server.py`.

- Implement `MCPServer` class:
  - `register_tool(name: str, description: str, schema: dict, handler: Callable[[dict], str]) -> None`
  - `handle_request(request: dict) -> dict`: Processes a JSON-RPC 2.0 request dict and returns a response dict.
- JSON-RPC 2.0 compliance:
  - Must check `"jsonrpc": "2.0"` and preserve request `"id"`.
  - Return error `-32600` (Invalid Request) if request is not a valid dict or lacks `method` or `jsonrpc != "2.0"`.
  - Return error `-32601` (Method not found) if method is unknown.
- Supported methods:
  - `"tools/list"`: returns `{"result": {"tools": [{"name": ..., "description": ..., "inputSchema": ...}, ...]}}`.
  - `"tools/call"`: accepts `params: {"name": ..., "arguments": ...}`.
    - If tool not registered: returns `{"result": {"isError": True, "content": [{"type": "text", "text": "Tool not found"}]}}`.
    - If required argument missing: returns `{"result": {"isError": True, "content": [{"type": "text", "text": "Missing required argument: <arg>"}]}}`.
    - On handler success: returns `{"result": {"content": [{"type": "text", "text": str(output)}]}}`.
    - On handler exception: catch and return `{"result": {"isError": True, "content": [{"type": "text", "text": f"Error: {e}"}]}}`.

Done means `python examples/mcp-server/verify.py starter` exits successfully.
