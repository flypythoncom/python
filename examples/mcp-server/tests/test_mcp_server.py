from __future__ import annotations

import unittest

from mcp_server import MCPServer


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
            handler=lambda args: str(args["a"] + args["b"]),
        )
        self.server.register_tool(
            name="risky_operation",
            description="An operation that can fail",
            schema={"type": "object"},
            handler=lambda args: 1 / 0,  # Deliberate ZeroDivisionError
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


if __name__ == "__main__":
    unittest.main()
