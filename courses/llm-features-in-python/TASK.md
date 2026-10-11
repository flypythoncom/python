# Task contract: ticket triage with a language model

Change only `starter/ticket_triage.py`. Standard library only. Never modify
`tests/`, `solution/`, or `scenario/`. `ReplayClient`, `build_messages`,
`load_scenario`, and `main` are provided and already correct; the work is in
the four functions below. A *client* is any callable
`client(messages) -> str`; every string it returns is untrusted input.

- `parse_triage(raw, categories) -> dict`:
  - Strip surrounding whitespace and one surrounding Markdown code fence
    (```` ``` ```` or ```` ```json ````) before parsing.
  - The reply must be a JSON **object** with exactly the fields
    `category`, `priority`, `summary`, `needs_human` — a missing field or an
    extra field raises `TriageError` naming that field.
  - `category` is one of *categories*; `priority` is an `int` from 1 to 4
    (`bool` and `float` are rejected); `summary` is a non-empty string of at
    most 120 characters after stripping; `needs_human` is a `bool`.
  - Every rejection raises `TriageError` whose message names the offending
    field. Non-JSON text and non-object JSON also raise `TriageError`.
  - Return exactly the four fields, with `summary` stripped.
- `run_tool_call(call, tools) -> (name, result)`:
  - *tools* maps a tool name to
    `{"function": callable, "parameters": {name: type}}` — it is the
    allowlist.
  - *call* must have exactly the keys `tool` and `arguments`. An
    unregistered tool name raises `ToolCallError` naming the tool.
  - *arguments* must have exactly the declared parameter names, each an
    instance of its declared type (`bool` is not accepted for `int`).
    Missing, unexpected, or mistyped arguments raise `ToolCallError` naming
    the argument. The tool function is never called on a refused call.
  - Return `(name, function(**arguments))`.
- `triage(ticket_text, client, *, categories, tools=None, max_attempts=2, max_tool_calls=3) -> dict`:
  - Start from `build_messages(...)`. After each reply, append
    `{"role": "assistant", "content": raw}`.
  - A reply that decodes to an object with a `tool` key is a tool call. On
    success, append `{"role": "tool", "name": name, "content": json.dumps(result)}`
    and ask the client again; successful tool calls do not count as
    attempts. `tool_calls` counts only calls that ran. A tool call that
    would exceed *max_tool_calls* is not run and ends in the fallback.
  - Any rejected reply — invalid answer or refused tool call — counts as one
    attempt and appends `{"role": "user", "content": ...}` that contains the
    `TriageError` message, then asks again.
  - A valid answer returns the four fields plus `attempts` (rejected replies
    + 1), `tool_calls`, and `fallback: False`.
  - After *max_attempts* rejected replies, return the fallback:
    `{"category": None, "priority": None, "summary": ticket_text.strip()[:120], "needs_human": True}`
    plus `attempts` (the number of rejected replies), `tool_calls`, and
    `fallback: True`. Never guess a category.
- `evaluate(cases, client_for, *, categories, tools=None) -> dict`:
  - Run `triage` for every case with `client_for(case)`. A case is correct
    when `category` and `needs_human` both match `case["expected"]`.
  - Return `total` (every case), `correct`, `fallbacks`,
    `schema_valid` (`total - fallbacks`), `accuracy`
    (`round(correct / total, 3)`, `0.0` for no cases), and `failures`: one
    `{"id", "reason"}` per incorrect or fallback case, in case order.
  - Never skip a case: the denominator is every case you were given.

`python ticket_triage.py <scenario-dir> [--min-accuracy X]` prints
`accuracy=… correct=N/T fallbacks=F min_accuracy=…`, one line per failure,
and returns 0 when `accuracy >= min_accuracy`, else 1; usage errors return 2.
The threshold defaults to the scenario's `min_accuracy`.

Done means `python verify.py starter` exits 0 with all fifteen tests
passing.
