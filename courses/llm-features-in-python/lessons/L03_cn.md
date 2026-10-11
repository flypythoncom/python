---
id: course-llm-features-l03
type: course
title: "第 3 课：校验、工具白名单、重试——一次一组"
summary: "用四个有界轮次把 starter 推到全绿——解析器、工具关口、重试与兜底循环、评测——并亲眼看到一处修复暴露出旧代码藏着的 bug。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
hints:
  - title: "本检查点考察什么"
    body: "starter 通过你监督的改动让十五个测试全绿——`python verify.py` 只在 starter 套件变绿后显示本检查点的码。"
  - title: "预期会有一个测试变红"
    body: "解析器那一轮之后，`test_tool_result_is_fed_back_to_the_model` 会失败。旧循环靠宽松解析来发现工具调用；严格的解析器会拒绝它们。循环必须先解码、再判断。"
  - title: "绝不为通过而放松"
    body: "录好的回复校验不过时，修法永远不是接受它。测试和录音都是只读的；动的是代码。"
---

# 第 3 课：校验、工具白名单、重试——一次一组

## 目标

starter 通过四个有界轮次让十五个测试全绿，并且不看 solution 你也讲得清
每一个 diff——包括中途变红的那一个测试。

## 为什么有这节课

最诱人的做法是一句「把它改健壮」。你会得到一个大 diff：处处包
`try/except`、看着差不多就接受、有些测试因为错误的理由通过。四个有界
轮次，各自钉在第 2 课的一个契约决定上，才能让每一行都讲得清。

## 本课内容

开一个新的 Agent 会话，说：

**“按 TASK.md 改 starter/ticket_triage.py，每轮只做一个函数：先
parse_triage，再 run_tool_call，再 triage，最后 evaluate。每轮之后跑
`python verify.py starter`，给我看 diff，等我确认再做下一轮。不要改
tests/、solution/ 或 scenario/。”**

预期失败数这样变化：

| 哪一轮之后 | 失败数 | 改了什么 |
| --- | --- | --- |
| 开始 | 12 | — |
| `parse_triage` | 9 | 四个解析器测试通过；**一个原本通过的测试变红** |
| `run_tool_call` | 7 | 白名单与参数检查 |
| `triage` | 3 | 带反馈重试、兜底、工具调用上限，以及修好的工具路径 |
| `evaluate` | 0 | 分母、兜底计数，以及两个端到端测试 |

第一轮之后变红的那个测试，是整门课最有价值的时刻。
`test_tool_result_is_fed_back_to_the_model` 之前能过，只是因为 starter 的
`triage` 把每条回复都交给一个接受任意 JSON 的解析器，再去找 `tool` 键。
严格的解析器会拒绝工具调用——它不是分诊答案。修法属于 `triage`（先解码
对象，再按 `tool` 分支），而不是放松解析器。如果 Agent 提议让
`parse_triage` 重新接受工具调用，拒绝它，并指向契约。

每一轮都守住这些边界：

- 只动 `starter/ticket_triage.py`。`tests/`、`solution/`、`scenario/` 里的
  任何 diff 都拒绝。
- `triage` 里不许有裸 `except:`，也不许 `except Exception`——循环只捕获
  `TriageError`（`ToolCallError` 是它的子类），别的都不捕获。client 抛
  异常是另一类问题，必须保持可见。
- 错误信息要点名字段或参数。「无效」不算信息。
- 兜底绝不猜分类。
- 只用标准库。

## 练习

`triage` 那一轮之后，读一读重试时发出的消息。在课程文件夹里运行下面的
命令，读第二次调用的最后一条消息：

```bash
python -c "import sys; sys.path.insert(0, 'starter'); import ticket_triage as t; c = t.ReplayClient(['{\"category\": \"login\", \"priority\": 2, \"summary\": \"x\", \"needs_human\": false}', '{\"category\": \"account\", \"priority\": 2, \"summary\": \"x\", \"needs_human\": false}']); print(t.triage('cannot log in', c, categories=['account', 'other'])); print(c.calls[1][-1])"
```

用一句话解释：为什么正是这条消息让重试值得做。

## 检查点

运行 `python verify.py`。本检查点的码只在 starter 套件全绿时出现。不看
材料能回答即算通过：

1. 解析器那一轮之后哪个测试变红了？为什么修法在 `triage` 而不在
   `parse_triage`？
2. 你的 `run_tool_call` 在调用函数之前到底检查了什么、按什么顺序？
3. 为什么循环只捕获 `TriageError`？

## 预期证据

一次全绿的 `python verify.py starter`、四个 diff，以及你对那个先红后绿的
测试的解释。
