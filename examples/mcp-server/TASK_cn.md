# 任务契约：无状态 MCP JSON-RPC 工具服务（2026-07-28 规范）

仅修改 `starter/mcp_server.py`。

- 实现 `MCPServer` 类：
  - `register_tool(name: str, description: str, schema: dict, handler: Callable) -> None`
  - `handle_request(request: dict) -> dict`：处理 JSON-RPC 2.0 请求字典并返回响应字典。
- JSON-RPC 2.0 规范要求：
  - 必须校验 `"jsonrpc": "2.0"` 并保留请求中的 `"id"`。
  - 请求格式非法、缺少 `method` 或 `jsonrpc != "2.0"` 时返回错误码 `-32600`（Invalid Request）。
  - 请求未注册的方法时返回错误码 `-32601`（Method not found）。
- 2026-07-28 无状态行为：
  - `initialize` 必须返回 `-32601`，消息中说明它已被 2026-07-28 无状态规范移除；工具调用前没有任何握手。
  - 若请求携带 `_meta.protocolVersion` 且不等于 `"2026-07-28"`，返回 `-32600`（Invalid Request）；协议版本由每个请求自描述。
- 支持的核心方法：
  - `"tools/list"`：返回 `{"result": {"tools": [{"name": ..., "description": ..., "inputSchema": ...}, ...]}}`。
  - `"tools/call"`：接收 `params: {"name": ..., "arguments": ..., "inputResponses": {...}?}`，并以 `handler(arguments, inputResponses)` 调用工具。
    - 工具未找到：返回 `{"result": {"isError": True, "content": [{"type": "text", "text": "Tool not found"}]}}`。
    - 缺少 schema 中声明的必填参数：返回 `{"result": {"isError": True, "content": [{"type": "text", "text": "Missing required argument: <arg>"}]}}`。
    - 工具抛出 `InputRequired(requests)`：返回 `{"result": {"resultType": "input_required", "requests": <requests>, "content": [{"type": "text", "text": "Additional client input is required before this tool can finish."}]}}`。客户端携带 `params.inputResponses` 重试同一请求。
    - 执行成功：返回 `{"result": {"content": [{"type": "text", "text": str(output)}]}}`。
    - 其他执行异常：捕获并返回 `{"result": {"isError": True, "content": [{"type": "text", "text": f"Error: {e}"}]}}`。
- 提供 `InputRequired(Exception)`，带 `requests` 属性，让工具能够向客户端请求补充输入。

完成标准：`python examples/mcp-server/verify.py starter` 成功退出。
