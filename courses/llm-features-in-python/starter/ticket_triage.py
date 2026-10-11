"""Support-ticket triage with a language model (starter, incomplete).

The model is any callable ``client(messages) -> str``. The course ships a
``ReplayClient`` that returns recorded replies, so everything runs offline
and deterministically. This starter reproduces the demo-day state: it trusts
whatever JSON the model sends, runs any tool name it is given with whatever
arguments arrive, never retries, crashes instead of falling back, and its
eval quietly skips the cases that crashed.
../TASK.md defines the contract.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

FIELDS = ("category", "priority", "summary", "needs_human")
SUMMARY_LIMIT = 120
DEFAULT_MIN_ACCURACY = 0.8
TYPE_NAMES = {"str": str, "int": int, "float": float, "bool": bool}


class TriageError(ValueError):
    """A model reply that does not satisfy the triage contract."""


class ToolCallError(TriageError):
    """A tool call the application refuses to run."""


class ReplayClient:
    """Offline stand-in for a model API: returns recorded replies in order."""

    def __init__(self, replies: list[str]) -> None:
        self._replies = list(replies)
        self.calls: list[list[dict]] = []

    def __call__(self, messages: list[dict]) -> str:
        self.calls.append([dict(message) for message in messages])
        if not self._replies:
            raise RuntimeError("replay exhausted: the feature asked for more replies than were recorded")
        return self._replies.pop(0)


def build_messages(ticket_text: str, categories: list[str], tools: dict | None = None) -> list[dict]:
    """Return the system and user messages for one ticket."""
    lines = [
        "You triage customer support tickets.",
        "Reply with only a JSON object with exactly these fields:",
        f'  "category": one of {", ".join(categories)}',
        '  "priority": integer 1 (urgent) to 4 (low)',
        f'  "summary": one sentence, at most {SUMMARY_LIMIT} characters',
        '  "needs_human": true or false',
    ]
    for name, spec in sorted((tools or {}).items()):
        parameters = ", ".join(f"{key}: {kind.__name__}" for key, kind in spec["parameters"].items())
        lines.append(
            f'To call the tool {name}({parameters}), reply with only '
            f'{{"tool": "{name}", "arguments": {{...}}}}.'
        )
    return [
        {"role": "system", "content": "\n".join(lines)},
        {"role": "user", "content": ticket_text},
    ]


def parse_triage(raw: str, categories: list[str]) -> dict:
    """Parse one model reply into the triage fields."""
    return json.loads(raw)


def run_tool_call(call: dict, tools: dict) -> tuple[str, object]:
    """Run the tool the model asked for; return (name, result)."""
    name = call["tool"]
    return name, tools[name]["function"](**call["arguments"])


def triage(
    ticket_text: str,
    client,
    *,
    categories: list[str],
    tools: dict | None = None,
    max_attempts: int = 2,
    max_tool_calls: int = 3,
) -> dict:
    """Triage one ticket with the model."""
    tools = tools or {}
    messages = build_messages(ticket_text, categories, tools)
    raw = client(messages)
    messages.append({"role": "assistant", "content": raw})
    reply = parse_triage(raw, categories)
    tool_calls = 0
    if "tool" in reply:
        name, output = run_tool_call(reply, tools)
        tool_calls += 1
        messages.append({"role": "tool", "name": name, "content": json.dumps(output, ensure_ascii=False)})
        raw = client(messages)
        messages.append({"role": "assistant", "content": raw})
        reply = parse_triage(raw, categories)
    reply.update(attempts=1, tool_calls=tool_calls, fallback=False)
    return reply


def evaluate(cases: list[dict], client_for, *, categories: list[str], tools: dict | None = None) -> dict:
    """Run every case and score it against its expected label."""
    answered = 0
    correct = 0
    failures = []
    for case in cases:
        try:
            result = triage(case["ticket"], client_for(case), categories=categories, tools=tools)
        except Exception:
            continue
        answered += 1
        expected = case["expected"]
        if result.get("category") == expected["category"] and result.get("needs_human") == expected["needs_human"]:
            correct += 1
        else:
            failures.append({"id": case["id"], "reason": f"expected {expected['category']}"})
    return {
        "total": len(cases),
        "schema_valid": answered,
        "correct": correct,
        "fallbacks": 0,
        "accuracy": round(correct / answered, 3) if answered else 0.0,
        "failures": failures,
    }


def load_scenario(scenario_dir: str | Path) -> dict:
    """Load scenario.json, cases.json, recordings.json, and lookup tools."""
    directory = Path(scenario_dir)
    config = json.loads((directory / "scenario.json").read_text(encoding="utf-8"))
    cases = json.loads((directory / "cases.json").read_text(encoding="utf-8"))
    recordings = json.loads((directory / "recordings.json").read_text(encoding="utf-8"))
    tools = {}
    for name, spec in config.get("tools", {}).items():
        records = json.loads((directory / spec["data"]).read_text(encoding="utf-8"))
        parameters = {key: TYPE_NAMES[kind] for key, kind in spec["parameters"].items()}
        key_name = next(iter(parameters))

        def lookup(_records=records, _key=key_name, **arguments):
            return _records.get(arguments[_key], {"error": "not found"})

        tools[name] = {"function": lookup, "parameters": parameters}
    return {"config": config, "cases": cases, "replies": recordings["replies"], "tools": tools}


def main(argv: list[str] | None = None) -> int:
    """Evaluate one scenario offline and gate on its accuracy threshold."""
    arguments = sys.argv[1:] if argv is None else argv
    usage = "usage: python ticket_triage.py <scenario-dir> [--min-accuracy 0.8]"
    if len(arguments) not in (1, 3) or (len(arguments) == 3 and arguments[1] != "--min-accuracy"):
        print(usage, file=sys.stderr)
        return 2
    scenario = load_scenario(arguments[0])
    config = scenario["config"]
    if len(arguments) == 3:
        try:
            threshold = float(arguments[2])
        except ValueError:
            print(usage, file=sys.stderr)
            return 2
    else:
        threshold = float(config.get("min_accuracy", DEFAULT_MIN_ACCURACY))
    report = evaluate(
        scenario["cases"],
        lambda case: ReplayClient(scenario["replies"][case["id"]]),
        categories=config["categories"],
        tools=scenario["tools"],
    )
    print(
        f"accuracy={report['accuracy']:.3f} correct={report['correct']}/{report['total']} "
        f"fallbacks={report['fallbacks']} min_accuracy={threshold:.3f}"
    )
    for failure in report["failures"]:
        print(f"  {failure['id']}: {failure['reason']}")
    return 0 if report["accuracy"] >= threshold else 1


if __name__ == "__main__":
    raise SystemExit(main())
