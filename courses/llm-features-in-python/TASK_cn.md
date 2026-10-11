# 任务契约：用语言模型做工单分诊

只修改 `starter/ticket_triage.py`。仅用标准库。绝不修改 `tests/`、
`solution/` 或 `scenario/`。`ReplayClient`、`build_messages`、
`load_scenario` 和 `main` 已经提供且正确；要做的是下面四个函数。
*client* 是任意可调用对象 `client(messages) -> str`；它返回的每个字符串
都是不可信输入。

- `parse_triage(raw, categories) -> dict`：
  - 解析前去掉首尾空白，以及外面包着的一层 Markdown 代码围栏
    （```` ``` ```` 或 ```` ```json ````）。
  - 回复必须是一个 JSON **对象**，且恰好包含 `category`、`priority`、
    `summary`、`needs_human` 四个字段——缺字段或多字段都抛出点名该字段的
    `TriageError`。
  - `category` 属于 *categories*；`priority` 是 1 到 4 的 `int`（`bool`
    和 `float` 都拒绝）；`summary` 去掉首尾空白后是非空、最多 120 个字符的
    字符串；`needs_human` 是 `bool`。
  - 每一种拒绝都抛出 `TriageError`，消息里点名出错的字段。非 JSON 文本和
    非对象 JSON 也抛 `TriageError`。
  - 只返回这四个字段，`summary` 去掉首尾空白。
- `run_tool_call(call, tools) -> (name, result)`：
  - *tools* 把工具名映射到
    `{"function": callable, "parameters": {name: type}}`——它就是白名单。
  - *call* 必须恰好有 `tool` 和 `arguments` 两个键。未登记的工具名抛出
    点名该工具的 `ToolCallError`。
  - *arguments* 必须恰好是声明的参数名，且每个值都是声明类型的实例
    （`int` 参数不接受 `bool`）。缺参数、多参数、类型错都抛出点名该参数
    的 `ToolCallError`。被拒绝的调用绝不调用工具函数。
  - 返回 `(name, function(**arguments))`。
- `triage(ticket_text, client, *, categories, tools=None, max_attempts=2, max_tool_calls=3) -> dict`：
  - 从 `build_messages(...)` 开始。每收到一条回复，追加
    `{"role": "assistant", "content": raw}`。
  - 解码后是带 `tool` 键的对象的回复是工具调用。成功时追加
    `{"role": "tool", "name": name, "content": json.dumps(result)}` 再问一次
    client；成功的工具调用不算尝试次数。`tool_calls` 只统计真正执行过的
    调用。会超出 *max_tool_calls* 的那次工具调用不执行，直接进入兜底。
  - 任何被拒绝的回复——无效答案或被拒的工具调用——计一次尝试，并追加一条
    包含 `TriageError` 消息的 `{"role": "user", "content": ...}`，然后再问。
  - 有效答案返回四个字段，外加 `attempts`（被拒回复数 + 1）、`tool_calls`
    和 `fallback: False`。
  - 被拒回复达到 *max_attempts* 次后，返回兜底结果：
    `{"category": None, "priority": None, "summary": ticket_text.strip()[:120], "needs_human": True}`，
    外加 `attempts`（被拒回复的次数）、`tool_calls` 和 `fallback: True`。
    绝不猜一个分类。
- `evaluate(cases, client_for, *, categories, tools=None) -> dict`：
  - 对每个用例用 `client_for(case)` 跑 `triage`。`category` 与
    `needs_human` 都与 `case["expected"]` 一致才算正确。
  - 返回 `total`（全部用例）、`correct`、`fallbacks`、
    `schema_valid`（`total - fallbacks`）、`accuracy`
    （`round(correct / total, 3)`，没有用例时为 `0.0`），以及 `failures`：
    每个错误或兜底的用例一条 `{"id", "reason"}`，按用例顺序。
  - 绝不跳过用例：分母是你拿到的全部用例。

`python ticket_triage.py <scenario-dir> [--min-accuracy X]` 打印
`accuracy=… correct=N/T fallbacks=F min_accuracy=…`，每个失败一行；
`accuracy >= min_accuracy` 时返回 0，否则 1；用法错误返回 2。阈值缺省为
场景的 `min_accuracy`。

完成的标准是 `python verify.py starter` 以 0 退出且全部十五个测试通过。
