"""Contract tests for the ticket-triage LLM feature."""

from __future__ import annotations

import contextlib
import io
import json
import unittest
from pathlib import Path

import ticket_triage

COURSE_ROOT = Path(__file__).resolve().parent.parent
SCENARIO_ROOT = COURSE_ROOT / "scenario"
CATEGORIES = ["billing", "shipping", "returns", "account", "other"]


def reply(**overrides) -> str:
    value = {"category": "billing", "priority": 2, "summary": "Charged twice.", "needs_human": True}
    value.update(overrides)
    return json.dumps({key: item for key, item in value.items() if item is not ...})


def lookup_tools(calls: list) -> dict:
    def lookup_order(order_id):
        calls.append(order_id)
        return {"status": "in transit"}

    return {"lookup_order": {"function": lookup_order, "parameters": {"order_id": str}}}


class ParseTriageTest(unittest.TestCase):
    def test_parse_accepts_a_valid_reply(self) -> None:
        self.assertEqual(
            ticket_triage.parse_triage(reply(), CATEGORIES),
            {"category": "billing", "priority": 2, "summary": "Charged twice.", "needs_human": True},
        )

    def test_parse_strips_a_markdown_fence(self) -> None:
        fenced = "```json\n" + reply(category="returns") + "\n```"
        self.assertEqual(ticket_triage.parse_triage(fenced, CATEGORIES)["category"], "returns")

    def test_parse_rejects_an_unknown_category_naming_the_field(self) -> None:
        with self.assertRaises(ticket_triage.TriageError) as caught:
            ticket_triage.parse_triage(reply(category="login"), CATEGORIES)
        self.assertIn("category", str(caught.exception))

    def test_parse_rejects_bad_priorities(self) -> None:
        for bad in ("high", 0, 5, 2.5, True):
            with self.subTest(priority=bad):
                with self.assertRaises(ticket_triage.TriageError) as caught:
                    ticket_triage.parse_triage(reply(priority=bad), CATEGORIES)
                self.assertIn("priority", str(caught.exception))

    def test_parse_rejects_missing_extra_and_mistyped_fields(self) -> None:
        cases = {
            "summary": reply(summary=...),
            "confidence": reply(confidence=0.9),
            "needs_human": reply(needs_human="yes"),
        }
        for field, raw in cases.items():
            with self.subTest(field=field):
                with self.assertRaises(ticket_triage.TriageError) as caught:
                    ticket_triage.parse_triage(raw, CATEGORIES)
                self.assertIn(field, str(caught.exception))
        for raw in ("Sure! Category: billing.", "[]", reply(summary="x" * 121)):
            with self.subTest(raw=raw[:20]):
                with self.assertRaises(ticket_triage.TriageError):
                    ticket_triage.parse_triage(raw, CATEGORIES)


class ToolCallTest(unittest.TestCase):
    def test_unregistered_tool_is_refused(self) -> None:
        calls: list = []
        with self.assertRaises(ticket_triage.ToolCallError) as caught:
            ticket_triage.run_tool_call(
                {"tool": "issue_refund", "arguments": {"order_id": "A-1"}}, lookup_tools(calls)
            )
        self.assertIn("issue_refund", str(caught.exception))
        self.assertEqual(calls, [])

    def test_tool_arguments_are_validated_before_the_call(self) -> None:
        calls: list = []
        tools = lookup_tools(calls)
        bad_calls = {
            "order_id": {"tool": "lookup_order", "arguments": {"order_id": 1002}},
            "amount": {"tool": "lookup_order", "arguments": {"order_id": "A-1", "amount": 49.0}},
        }
        for name, call in bad_calls.items():
            with self.subTest(argument=name):
                with self.assertRaises(ticket_triage.ToolCallError) as caught:
                    ticket_triage.run_tool_call(call, tools)
                self.assertIn(name, str(caught.exception))
        self.assertEqual(calls, [])
        self.assertEqual(
            ticket_triage.run_tool_call({"tool": "lookup_order", "arguments": {"order_id": "A-1"}}, tools),
            ("lookup_order", {"status": "in transit"}),
        )


class TriageTest(unittest.TestCase):
    def test_tool_result_is_fed_back_to_the_model(self) -> None:
        calls: list = []
        client = ticket_triage.ReplayClient([
            json.dumps({"tool": "lookup_order", "arguments": {"order_id": "A-2"}}),
            reply(category="shipping", needs_human=False),
        ])
        result = ticket_triage.triage("Where is A-2?", client, categories=CATEGORIES, tools=lookup_tools(calls))
        self.assertEqual(result["category"], "shipping")
        self.assertEqual(result["tool_calls"], 1)
        self.assertEqual(calls, ["A-2"])
        tool_message = client.calls[1][-1]
        self.assertEqual(tool_message["role"], "tool")
        self.assertEqual(json.loads(tool_message["content"]), {"status": "in transit"})

    def test_invalid_reply_is_retried_with_the_error_fed_back(self) -> None:
        client = ticket_triage.ReplayClient([reply(category="login"), reply(category="account")])
        result = ticket_triage.triage("Cannot log in", client, categories=CATEGORIES)
        self.assertEqual(result["category"], "account")
        self.assertEqual(result["attempts"], 2)
        self.assertFalse(result["fallback"])
        feedback = client.calls[1][-1]
        self.assertEqual(feedback["role"], "user")
        self.assertIn("category", feedback["content"])

    def test_repeated_invalid_replies_fall_back_to_a_human(self) -> None:
        client = ticket_triage.ReplayClient(["Sure! It's billing.", "Category: billing"])
        result = ticket_triage.triage("asdf", client, categories=CATEGORIES, max_attempts=2)
        self.assertEqual(
            result,
            {"category": None, "priority": None, "summary": "asdf", "needs_human": True,
             "attempts": 2, "tool_calls": 0, "fallback": True},
        )

    def test_tool_call_budget_ends_in_the_fallback(self) -> None:
        calls: list = []
        lookup = json.dumps({"tool": "lookup_order", "arguments": {"order_id": "A-2"}})
        client = ticket_triage.ReplayClient([lookup, lookup, lookup])
        result = ticket_triage.triage(
            "Where is A-2?", client, categories=CATEGORIES, tools=lookup_tools(calls), max_tool_calls=2
        )
        self.assertTrue(result["fallback"])
        self.assertIsNone(result["category"])
        self.assertEqual(result["tool_calls"], 2)
        self.assertEqual(result["attempts"], 0)
        self.assertEqual(calls, ["A-2", "A-2"])


class EvaluateTest(unittest.TestCase):
    def test_accuracy_divides_by_every_case_and_counts_fallbacks(self) -> None:
        replies = {
            "a": [reply(category="billing", needs_human=True)],
            "b": [reply(category="shipping", needs_human=False)],
            "c": ["not json", "still not json"],
            "d": [reply(category="other"), "nope"],
        }
        cases = [
            {"id": "a", "ticket": "charged twice", "expected": {"category": "billing", "needs_human": True}},
            {"id": "b", "ticket": "where is it", "expected": {"category": "shipping", "needs_human": False}},
            {"id": "c", "ticket": "???", "expected": {"category": "other", "needs_human": True}},
            {"id": "d", "ticket": "refund", "expected": {"category": "returns", "needs_human": True}},
        ]
        report = ticket_triage.evaluate(
            cases, lambda case: ticket_triage.ReplayClient(replies[case["id"]]), categories=CATEGORIES
        )
        self.assertEqual(report["total"], 4)
        self.assertEqual(report["correct"], 2)
        self.assertEqual(report["fallbacks"], 1)
        self.assertEqual(report["schema_valid"], 3)
        self.assertEqual(report["accuracy"], 0.5)
        self.assertEqual([failure["id"] for failure in report["failures"]], ["c", "d"])


class MainTest(unittest.TestCase):
    def run_main(self, argv: list[str]) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            code = ticket_triage.main(argv)
        return code, output.getvalue()

    def test_shop_support_eval_is_reported_below_threshold(self) -> None:
        code, output = self.run_main([str(SCENARIO_ROOT / "shop-support")])
        self.assertEqual(code, 1)
        self.assertIn("accuracy=0.750 correct=6/8 fallbacks=1", output)

    def test_it_helpdesk_eval_passes_its_threshold(self) -> None:
        code, output = self.run_main([str(SCENARIO_ROOT / "it-helpdesk")])
        self.assertEqual(code, 0)
        self.assertIn("accuracy=0.833 correct=5/6 fallbacks=1", output)

    def test_missing_argument_prints_usage(self) -> None:
        self.assertEqual(self.run_main([])[0], 2)


if __name__ == "__main__":
    unittest.main()
