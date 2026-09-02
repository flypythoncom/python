"""Robust JSON-RPC 2.0 Model Context Protocol (MCP) server with schema validation and error isolation."""

from __future__ import annotations

from typing import Any, Callable


class MCPServer:
    def __init__(self) -> None:
        self.tools: dict[str, dict[str, Any]] = {}

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
        if not isinstance(request, dict) or request.get("jsonrpc") != "2.0" or "method" not in request:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id") if isinstance(request, dict) else None,
                "error": {"code": -32600, "message": "Invalid Request"},
            }

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
            params = request.get("params")
            if not isinstance(params, dict) or "name" not in params:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": "Invalid params: missing tool name"},
                }

            tool_name = params["name"]
            if tool_name not in self.tools:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "isError": True,
                        "content": [{"type": "text", "text": "Tool not found"}],
                    },
                }

            tool = self.tools[tool_name]
            args = params.get("arguments", {})
            if not isinstance(args, dict):
                args = {}

            # Validate required schema arguments
            required_props = tool["inputSchema"].get("required", [])
            for required_key in required_props:
                if required_key not in args:
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "isError": True,
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Missing required argument: {required_key}",
                                }
                            ],
                        },
                    }

            try:
                output = tool["handler"](args)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": str(output)}]},
                }
            except Exception as exc:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "isError": True,
                        "content": [{"type": "text", "text": f"Error: {exc}"}],
                    },
                }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": "Method not found"},
        }
