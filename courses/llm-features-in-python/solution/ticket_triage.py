"""Support-ticket triage with a language model (reference solution).

The model is any callable ``client(messages) -> str``. The course ships a
``ReplayClient`` that returns recorded replies, so everything runs offline
and deterministically. The feature code treats every reply as untrusted
input: it validates structured output, allowlists tool calls, retries with
the validation error fed back, falls back to a human instead of guessing,
and measures itself with an eval that divides by every case.
../TASK.md defines the contract.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

FIELDS = ("category", "priority", "summary", "needs_human")
SUMMARY_LIMIT = 120
DEFAULT_MIN_ACCURACY = 0.8
TYPE_NAMES = {"str": str, "int": int, "float": float, "bool": bool}
FENCE = re.compile(r"^```[A-Za-z]*\s*\n(.*?)\n?```$", re.DOTALL)


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


def _decode_object(raw: str) -> dict:
    if not isinstance(raw, str):
        raise TriageError("reply must be text")
    text = raw.strip()
    fenced = FENCE.match(text)
    if fenced:
        text = fenced.group(1).strip()
    try:
        value = json.loads(text)
    except ValueError as error:
        raise TriageError(f"reply is not valid JSON: {error}") from None
    if not isinstance(value, dict):
        raise TriageError("reply must be a JSON object")
    return value


def _validate(value: dict, categories: list[str]) -> dict:
    for field in FIELDS:
        if field not in value:
            raise TriageError(f"missing field: {field}")
    for field in value:
        if field not in FIELDS:
            raise TriageError(f"unexpected field: {field}")
    category = value["category"]
    if not isinstance(category, str) or category not in categories:
        raise TriageError(f"category must be one of {', '.join(categories)}; got {category!r}")
    priority = value["priority"]
    if isinstance(priority, bool) or not isinstance(priority, int) or not 1 <= priority <= 4:
        raise TriageError(f"priority must be an integer from 1 to 4; got {priority!r}")
    summary = value["summary"]
    if not isinstance(summary, str) or not summary.strip():
        raise TriageError("summary must be a non-empty string")
    if len(summary.strip()) > SUMMARY_LIMIT:
        raise TriageError(f"summary must be at most {SUMMARY_LIMIT} characters")
    if not isinstance(value["needs_human"], bool):
        raise TriageError(f"needs_human must be true or false; got {value['needs_human']!r}")
    return {
        "category": category,
        "priority": priority,
        "summary": summary.strip(),
        "needs_human": value["needs_human"],
    }


def parse_triage(raw: str, categories: list[str]) -> dict:
    """Parse and validate one model reply into the four triage fields."""
    return _validate(_decode_object(raw), categories)


def run_tool_call(call: dict, tools: dict) -> tuple[str, object]:
    """Run an allowlisted tool with validated arguments; return (name, result)."""
    if set(call) != {"tool", "arguments"}:
        raise ToolCallError('a tool call must have exactly the keys "tool" and "arguments"')
    name, arguments = call["tool"], call["arguments"]
    if not isinstance(name, str) or name not in tools:
        raise ToolCallError(f"unknown tool: {name!r}")
    if not isinstance(arguments, dict):
        raise ToolCallError(f"tool {name}: arguments must be an object")
    parameters = tools[name]["parameters"]
    for key in arguments:
        if key not in parameters:
            raise ToolCallError(f"tool {name}: unexpected argument {key}")
    for key, kind in parameters.items():
        if key not in arguments:
            raise ToolCallError(f"tool {name}: missing argument {key}")
        value = arguments[key]
        if (isinstance(value, bool) and kind is not bool) or not isinstance(value, kind):
            raise ToolCallError(f"tool {name}: argument {key} must be {kind.__name__}")
    return name, tools[name]["function"](**arguments)


def _fallback(ticket_text: str) -> dict:
    return {
        "category": None,
        "priority": None,
        "summary": ticket_text.strip()[:SUMMARY_LIMIT],
        "needs_human": True,
    }


def triage(
    ticket_text: str,
    client,
    *,
    categories: list[str],
    tools: dict | None = None,
    max_attempts: int = 2,
    max_tool_calls: int = 3,
) -> dict:
    """Triage one ticket: validate, run tool calls, retry, or fall back."""
    tools = tools or {}
    messages = build_messages(ticket_text, categories, tools)
    attempts = 0
    tool_calls = 0
    while attempts < max_attempts:
        raw = client(messages)
        messages.append({"role": "assistant", "content": raw})
        try:
            value = _decode_object(raw)
            if "tool" in value:
                if tool_calls >= max_tool_calls:
                    break
                name, output = run_tool_call(value, tools)
                tool_calls += 1
                messages.append({"role": "tool", "name": name, "content": json.dumps(output, ensure_ascii=False)})
                continue
            result = _validate(value, categories)
        except TriageError as error:
            attempts += 1
            messages.append({
                "role": "user",
                "content": f"Your reply was rejected: {error}. Reply again following the format exactly.",
            })
            continue
        attempts += 1
        result.update(attempts=attempts, tool_calls=tool_calls, fallback=False)
        return result
    result = _fallback(ticket_text)
    result.update(attempts=attempts, tool_calls=tool_calls, fallback=True)
    return result


def evaluate(cases: list[dict], client_for, *, categories: list[str], tools: dict | None = None) -> dict:
    """Run every case and score it against its expected label."""
    correct = 0
    fallbacks = 0
    failures = []
    for case in cases:
        result = triage(case["ticket"], client_for(case), categories=categories, tools=tools)
        expected = case["expected"]
        if result["fallback"]:
            fallbacks += 1
            failures.append({"id": case["id"], "reason": "fallback to a human"})
        elif result["category"] == expected["category"] and result["needs_human"] == expected["needs_human"]:
            correct += 1
        else:
            failures.append({
                "id": case["id"],
                "reason": f"expected {expected['category']}/needs_human={expected['needs_human']}, "
                          f"got {result['category']}/needs_human={result['needs_human']}",
            })
    total = len(cases)
    return {
        "total": total,
        "schema_valid": total - fallbacks,
        "correct": correct,
        "fallbacks": fallbacks,
        "accuracy": round(correct / total, 3) if total else 0.0,
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
