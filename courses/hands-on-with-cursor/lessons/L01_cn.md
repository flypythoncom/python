---
id: course-cursor-l01
type: course
title: "第 1 课：装好 Cursor、装上 FlyPython Skill、让 Agent 取回课程"
summary: "先把 Cursor 跑起来，装好 FlyPython Skill 并打开联网权限，让 Agent 取回本课文件——你不下载任何东西，然后让 starter 的失败变得客观。"
lang: zh-CN
content_version: 2
status: reviewed
reviewed_on: 2026-09-13
hints:
  - title: "本检查点考察什么"
    body: "先复现失败再动手修：`python verify.py` 必须把 l03 和 l04 显示为 `[open]`（`starter --expect-failure` 会打印点名测试）。在 Cursor 里，Agent 模式是干活的地方——但命令仍然是证据。"
  - title: "Ask 与 Agent 的区别"
    body: "Ask 模式只回答问题、不碰文件；Agent 模式会读文件、改代码、跑命令。本课只需要 Agent 读——明确告诉它不要改任何文件。"
  - title: "完成的标志"
    body: "你能说出套件证明了哪九种行为、为什么 starter 伪造不出来。`python verify.py` 随即显示本检查点的认领码。"
---

# 第 1 课：装好 Cursor、装上 FlyPython Skill、让 Agent 取回课程

## 目标

本课结束时，Cursor 已经跑起来、FlyPython Skill 已装好（联网权限已
打开），Agent 已把本课文件取回你的工作目录——你没有手动下载任何
东西。文件夹就位后，你运行课程的客观检查命令，并解释「starter
失败」在测试名里的含义。本课不改任何代码。

## 第 1 步——把 Cursor 跑起来

安装 Cursor，然后 `File → Open Folder`
打开一个空工作目录。

## 第 2 步——装 FlyPython Skill（含联网权限）

把 Skill 存为项目规则：

```bash
mkdir -p .cursor/rules
curl -s https://flypython.com/skills/flypython/SKILL.md -o .cursor/rules/flypython.mdc
```

开一个对话并确认处于 **Agent** 模式——这个模式才能读文件、跑命令。
Agent 模式抓取 URL 需要批准——被询问时批准。如果你的环境禁网，
就自己跑 curl，把文件粘贴过去。

Skill 只是一个文件，在每个工具里都一样：它告诉 Agent 如何为你
授权、取课程文件、验证、提交认领码。

## 第 3 步——让 Agent 取回本课文件（你不下载）

在工作目录里新开一个会话/对话/线程，粘贴这一句话：

> Read https://flypython.com/skills/flypython/SKILL.md and start the FlyPython course `hands-on-with-cursor`.

Agent 会给你一个授权链接和一组短码。打开链接、登录、核对码与
Agent 显示的一致后点「允许」，然后对 Agent 说「好了」。它取一次
token，把本课文件写到 `courses/hands-on-with-cursor/`。

**前提**：这些课程需要一个能执行命令**并且**能联网的编码 Agent。
只能聊天的网页 AI 做不了。

## 为什么有这一课

AI 写的 Python 大多是同一种死法：演示输入能跑，真实输入一到，脚本
在第 3 行崩掉——或者更糟，悄悄算出一个错的数。修复不从更好的
提示词开始，而从把「坏了」变成一条任何人都能跑、且得到相同答案的
命令开始。在 Cursor 里，Agent 模式就在它要验证的代码旁边跑这条
命令。

## 热身（2 分钟）

在编辑器里打开 `starter/report_tool.py`，从头读到尾。它看起来很
合理：带 docstring 的函数、类型标注、CLI。这正是 AI 生成代码的
样子——表面干净、行为缺失。现在打开 `TASK.md`，放在手边。

## 本课内容

本课文件现在已经位于 `courses/hands-on-with-cursor/`——你这边没有发生任何下载。
让 Agent 先只读不动手：

**“读 COURSE.md——它是本文件夹的教学契约。再读 TASK.md 和
starter/report_tool.py。不要改任何文件。告诉我测试期望哪些行为、
starter 缺了哪些。”**

趁它读的时候，运行学员命令——整个课程你只需要这一条检查命令：

```bash
python verify.py
```

你会看到 starter 复现出四类真实世界故障，对应到测试名：

| 失败的测试 | 真实含义 |
| --- | --- |
| `test_load_json_records_returns_list_of_dicts` | 工具只处理 CSV；API 场景直接崩 |
| `test_unsupported_suffix_raises_value_error` | 一个 `.xlsx` 上传变成莫名其妙的崩溃，而不是清楚的拒绝 |
| `test_invalid_records_are_isolated_with_reasons` | 一个空单元格中止整个运行——没有部分报告，没有原因 |
| `test_group_totals_are_rounded_to_two_decimals` | `0.1 + 0.2` 在报告里打印成 `0.30000000000000004` |
| `test_write_report_creates_missing_parent_directories` | 工具无法写进新建的输出目录 |
| `test_run_scenario_writes_report_file`、`test_main_prints_summary_and_returns_zero` | 上述问题的端到端后果 |

想看缺失行为对应的失败测试名，维护者命令会打印它们：

```bash
python verify.py starter --expect-failure
```

（参考答案 `solution/` 是给维护者证明目标可达用的。你不需要运行
它，它也从来不是完成标准——你的实现（`starter/`）才是。）这一对命令是整门课的完成
证据。

## 练习

挑一个你最有代入感的场景皮肤（`excel-report`、`data-monitor` 或
`api-tool`），打开它的数据文件，找出会被拒绝的行。先不看运行
结果，写下每个坏行会触发哪个测试，再对照上面的表自查——并让
Agent 确认，而不是让它修。

## 检查点

在课程文件夹里运行 `python verify.py`。不看材料能回答下面三个
问题即算通过：

1. 哪四个行为把 starter 和 solution 区分开？
2. `python verify.py` 为什么故意以非零退出——它在报告什么状态？
   为什么这是成功条件而不是报错？
3. 你在练习里找到的那一行会让 starter 崩溃、被隔离，还是悄悄
   通过？

本检查点的认领码已经在默认命令的输出里——能回答这些问题之后再
提交。

## 预期证据

默认命令的完整输出记录，加你的三个答案。保留好——第 4 课还会
用到。
