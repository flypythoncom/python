# 任务契约：极简 MCP JSON-RPC 工具服务

仅修改 `starter/mcp_server.py`。

- 实现 `MCPServer` 类：
  - `register_tool(name: str, description: str, schema: dict, handler: Callable[[dict], str]) -> None`
  - `handle_request(request: dict) -> dict`：处理 JSON-RPC 2.0 请求字典并返回响应字典。
- JSON-RPC 2.0 规范要求：
  - 必须校验 `"jsonrpc": "2.0"` 并保留请求中的 `"id"`。
  - 请求格式非法、缺少 `method` 或 `jsonrpc != "2.0"` 时返回错误码 `-32600`（Invalid Request）。
  - 请求未注册的方法时返回错误码 `-32601`（Method not found）。
- 支持的核心方法：
  - `"tools/list"`：返回 `{"result": {"tools": [{"name": ..., "description": ..., "inputSchema": ...}, ...]}}`。
  - `"tools/call"`：接收 `params: {"name": ..., "arguments": ...}`。
    - 工具未找到：返回 `{"result": {"isError": True, "content": [{"type": "text", "text": "Tool not found"}]}}`。
    - 缺少 schema 中声明的必填参数：返回 `{"result": {"isError": True, "content": [{"type": "text", "text": "Missing required argument: <arg>"}]}}`。
    - 执行成功：返回 `{"result": {"content": [{"type": "text", "text": str(output)}]}}`。
    - 执行异常：捕获并返回 `{"result": {"isError": True, "content": [{"type": "text", "text": f"Error: {e}"}]}}`。

完成标准：`python examples/mcp-server/verify.py starter` 成功退出。
