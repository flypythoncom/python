from __future__ import annotations

import unittest

from mcp_server import MCPServer

try:
    from mcp_server import InputRequired
except ImportError:  # The starter does not implement the 2026-07-28 flow yet.
    InputRequired = None  # type: ignore[assignment]


def require_confirmation(args: dict, responses: dict | None = None) -> str:
    answer = str((responses or {}).get("confirm", "")).strip().lower()
    if answer != "yes":
        raise InputRequired(
            [{"id": "confirm", "prompt": "Type 'yes' to confirm deletion."}]
        )
    return "deleted"


class TestMCPServer(unittest.TestCase):
    def setUp(self) -> None:
        self.server = MCPServer()
        self.server.register_tool(
            name="calculate_sum",
            description="Add two numbers together",
            schema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
            handler=lambda args, responses=None: str(args["a"] + args["b"]),
        )
        self.server.register_tool(
            name="risky_operation",
            description="An operation that can fail",
            schema={"type": "object"},
            handler=lambda args, responses=None: 1 / 0,  # Deliberate ZeroDivisionError
        )

    def test_tools_list_returns_schemas(self) -> None:
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
        })
        self.assertEqual(resp["jsonrpc"], "2.0")
        self.assertEqual(resp["id"], 1)
        tools = resp["result"]["tools"]
        self.assertEqual(len(tools), 2)
        names = {t["name"] for t in tools}
        self.assertEqual(names, {"calculate_sum", "risky_operation"})

    def test_tools_call_success(self) -> None:
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "calculate_sum", "arguments": {"a": 10, "b": 25}},
        })
        self.assertEqual(resp["id"], 2)
        self.assertEqual(resp["result"]["content"][0]["text"], "35")

    def test_tools_call_missing_required_argument(self) -> None:
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "calculate_sum", "arguments": {"a": 10}},
        })
        self.assertTrue(resp["result"]["isError"])
        self.assertIn("Missing required argument: b", resp["result"]["content"][0]["text"])

    def test_tools_call_handles_runtime_exception(self) -> None:
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "risky_operation", "arguments": {}},
        })
        self.assertTrue(resp["result"]["isError"])
        self.assertIn("division by zero", resp["result"]["content"][0]["text"])

    def test_invalid_request_structure(self) -> None:
        resp = self.server.handle_request({"method": "tools/list"})  # Missing jsonrpc: 2.0
        self.assertIn("error", resp)
        self.assertEqual(resp["error"]["code"], -32600)

    def test_initialize_removed_returns_method_not_found(self) -> None:
        # The 2026-07-28 specification removed the initialize handshake:
        # requests are stateless and tool methods must be answered directly.
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 5,
            "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {}},
        })
        self.assertEqual(resp["error"]["code"], -32601)
        self.assertIn("removed", resp["error"]["message"])

    def test_protocol_version_validated_per_request(self) -> None:
        # Requests self-describe their protocol version through _meta.
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/list",
            "_meta": {"protocolVersion": "2025-06-18"},
        })
        self.assertIn("error", resp)
        self.assertEqual(resp["error"]["code"], -32600)

    def test_tools_call_input_required_round_trip(self) -> None:
        if InputRequired is None:
            self.skipTest("implementation lacks the 2026-07-28 input_required flow")
        self.server.register_tool(
            name="confirm_delete",
            description="Delete a resource after explicit confirmation",
            schema={"type": "object"},
            handler=require_confirmation,
        )

        first = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {"name": "confirm_delete", "arguments": {}},
        })
        self.assertEqual(first["result"]["resultType"], "input_required")
        self.assertEqual(first["result"]["requests"][0]["id"], "confirm")

        second = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 8,
            "method": "tools/call",
            "params": {
                "name": "confirm_delete",
                "arguments": {},
                "inputResponses": {"confirm": "YES"},
            },
        })
        self.assertEqual(second["result"]["content"][0]["text"], "deleted")


if __name__ == "__main__":
    unittest.main()
