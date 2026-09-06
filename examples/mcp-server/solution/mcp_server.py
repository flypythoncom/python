"""Stateless MCP tool server aligned with the 2026-07-28 specification.

The 2026-07-28 specification is stateless-first: the initialize/initialized
handshake and Mcp-Session-Id sessions were removed, so every request is
self-describing and tools/list or tools/call must be answered directly.
Server-initiated requests (including elicitation) were replaced by a
multi-round-trip flow: a tool that needs client input returns a result with
resultType "input_required", and the client retries the same call with the
answers attached in params.inputResponses.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

SUPPORTED_PROTOCOL_VERSION = "2026-07-28"

ToolHandler = Callable[..., Any]


class InputRequired(Exception):
    """Raised by a handler that cannot finish without additional client input.

    Carries the requests the client must answer. The server converts this into
    a tools/call result with resultType "input_required"; the client retries
    the same request with the answers in params.inputResponses.
    """

    def __init__(self, requests: list[dict[str, Any]]) -> None:
        super().__init__("tool execution needs additional client input")
        self.requests = requests


class MCPServer:
    def __init__(self) -> None:
        self.tools: dict[str, dict[str, Any]] = {}

    def register_tool(
        self,
        name: str,
        description: str,
        schema: dict[str, Any],
        handler: ToolHandler,
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

        # initialize was removed by the 2026-07-28 specification: requests are
        # stateless and there is no handshake to complete before tool calls.
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": "Method not found: initialize was removed by the stateless 2026-07-28 specification",
                },
            }

        # Requests self-describe their protocol version through _meta.
        meta = request.get("_meta")
        if isinstance(meta, dict):
            version = meta.get("protocolVersion")
            if version is not None and version != SUPPORTED_PROTOCOL_VERSION:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32600,
                        "message": f"Invalid Request: unsupported protocol version {version!r}; this server speaks {SUPPORTED_PROTOCOL_VERSION}",
                    },
                }

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

            input_responses = params.get("inputResponses")
            if not isinstance(input_responses, dict):
                input_responses = {}

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
                output = tool["handler"](args, input_responses)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": str(output)}]},
                }
            except InputRequired as exc:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "resultType": "input_required",
                        "requests": exc.requests,
                        "content": [
                            {
                                "type": "text",
                                "text": "Additional client input is required before this tool can finish.",
                            }
                        ],
                    },
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
