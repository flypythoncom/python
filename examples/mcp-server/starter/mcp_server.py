"""Naive MCP server implementation that crashes on missing tools and lacks schema validation."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class MCPServer:
    def __init__(self) -> None:
        self.tools: dict[str, Any] = {}

    def register_tool(
        self,
        name: str,
        description: str,
        schema: dict[str, Any],
        handler: Callable[[dict[str, Any]], str],
    ) -> None:
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": schema,
            "handler": handler,
        }

    def handle_request(self, request: Any) -> dict[str, Any]:
        # Naive: does not check jsonrpc version or error handling
        req_id = request.get("id")
        method = request["method"]

        if method == "tools/list":
            tools_list = [
                {
                    "name": t["name"],
                    "description": t["description"],
                    "inputSchema": t["inputSchema"],
                }
                for t in self.tools.values()
            ]
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools_list}}

        if method == "tools/call":
            params = request["params"]
            tool_name = params["name"]
            # Will crash if tool doesn't exist or handler raises
            tool = self.tools[tool_name]
            output = tool["handler"](params["arguments"])
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": str(output)}]},
            }

        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
