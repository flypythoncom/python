---
id: course-claude-code-l01
type: course
title: "第 1 课：装好 Claude Code、装上 FlyPython Skill、让 Agent 取回课程"
summary: "先把 Claude Code 跑起来，装好 FlyPython Skill 并打开联网权限，让 Agent 取回本课文件——你不下载任何东西，然后让 starter 的失败变得客观。"
lang: zh-CN
content_version: 2
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "考你能不能先复现故障再谈修复：`python verify.py starter --expect-failure` 必须打印出那组具名失败测试。重点是让失败变成客观证据，而不是修好它。"
  - title: "把失败名当成契约读"
    body: "每个失败的测试名都对应 `TASK.md` 里的一行——比如 `test_non_numeric_amount_is_invalid` 对应契约的『非数值的 numeric_field 值』。如果有名字对不上契约，那处漂移值得注意。"
  - title: "完成标准"
    body: "你能说清楚这九个测试各自证明了什么、为什么 starter 装不出来。然后 `python verify.py` 就会显示本检查点的认领码。"
---

# 第 1 课：装好 Claude Code、装上 FlyPython Skill、让 Agent 取回课程

## 目标

本课结束时，Claude Code 已经跑起来、FlyPython Skill 已装好（联网权限已
打开），Agent 已把本课文件取回你的工作目录——你没有手动下载任何
东西。文件夹就位后，你运行课程的客观检查命令，并解释「starter
失败」在测试名里的含义。本课不改任何代码。

## 第 1 步——把 Claude Code 跑起来

安装 Claude Code CLI
（`npm install -g @anthropic-ai/claude-code`），新建一个空工作目录，
在里面运行 `claude`。

## 第 2 步——（可选）预装 FlyPython Skill

这一步可选：第 3 步的开课句子会直接从 URL 读取 Skill，不装也能上课——预装只是省掉一次权限往返。

把 Skill 存为项目级技能——在工作目录里运行：

```bash
mkdir -p .claude/skills/flypython
curl -s https://flypython.com/skills/flypython/SKILL.md -o .claude/skills/flypython/SKILL.md
```

（全项目通用的个人副本：在 `~/.claude/skills/` 下执行同样命令。）
Claude Code 通过权限提示访问网络——它请求 fetch 或 curl 时批准即可。
如果你在禁网的沙箱里运行，就自己在终端跑 curl，把文件粘贴过去。

Skill 只是一个文件，在每个工具里都一样：它告诉 Agent 如何为你
授权、取课程文件、验证、提交认领码。

## 第 3 步——让 Agent 取回本课文件（你不下载）

在工作目录里新开一个会话/对话/线程，粘贴这一句话：

> Read https://flypython.com/skills/flypython/SKILL.md and start the FlyPython course `hands-on-python-with-claude-code`.

Agent 会给你一个授权链接和一组短码。打开链接、登录、核对码与
Agent 显示的一致后点「允许」，然后对 Agent 说「好了」。它取一次
token，把本课文件写到 `courses/hands-on-python-with-claude-code/`。

**前提**：这些课程需要一个能执行命令**并且**能联网的编码 Agent。
只能聊天的网页 AI 做不了。

## 为什么有这一课

大多数 AI 写的 Python 死法相同：演示输入没问题，真实输入一到，脚本
在第 3 行崩溃——或者更糟，悄悄算出一个错误的数字。修复不是从更好的
提示词开始，而是从把"它坏了"变成一条任何人运行都能得到同样结果的
命令开始。

## 热身（2 分钟）

打开 `starter/report_tool.py` 从头读一遍。它看起来很像样：带 docstring
的函数、类型标注、命令行入口。这正是 AI 生成代码的典型样子——表面
干净，行为缺失。然后打开 `TASK.md` 放在手边。

## 本课内容

本课文件现在已经位于 `courses/hands-on-python-with-claude-code/`——你这边没有发生任何下载。
让 Agent 先只读不动手：

**“读 COURSE.md——它是本文件夹的教学契约。再读 TASK.md 和
starter/report_tool.py。不要改任何文件。告诉我测试期望哪些行为、
starter 缺了哪些。”**

趁它读的时候，运行学员命令——整个课程你只需要这一条检查命令：

```bash
python verify.py
```

你会看到 starter 复现五类真实世界故障，外加两个端到端后果——共七个具名失败测试——并与测试名一一对应：

| 失败的测试 | 现实含义 |
| --- | --- |
| `test_load_json_records_returns_list_of_dicts` | 工具只认 CSV；API 场景直接崩溃 |
| `test_unsupported_suffix_raises_value_error` | 上传 `.xlsx` 得到一坨看不懂的报错，而不是清晰的拒绝 |
| `test_invalid_records_are_isolated_with_reasons` | 一个空单元格让整次运行中止——既没有部分报告，也没有原因 |
| `test_group_totals_are_rounded_to_two_decimals` | 报告里 `0.1 + 0.2` 打印成 `0.30000000000000004` |
| `test_write_report_creates_missing_parent_directories` | 工具无法写入新建的输出目录 |
| `test_run_scenario_writes_report_file`、`test_main_prints_summary_and_returns_zero` | 以上问题在端到端层面的体现 |

想看缺失行为对应的失败测试名，维护者命令会打印它们：

```bash
python verify.py starter --expect-failure
```

（参考答案 `solution/` 是给维护者证明目标可达用的。你不需要运行
它，它也从来不是完成标准——你的实现（`starter/`）才是。）这一对命令就是整个课程的完成证据。

## 练习

选一个你最有代入感的皮肤（`excel-report`、`data-monitor` 或
`api-tool`），打开它的数据文件，找出会被拒绝的行。在运行任何命令
之前，写下每个坏行会触发哪条测试，然后对照上面的表格检查。

## 检查点

在课程文件夹里运行 `python verify.py`。不看材料能回答下面三个
问题即算通过：

1. 哪五个行为把 starter 和 solution 区分开？其中哪两个失败测试是它们的端到端后果？
2. `python verify.py` 为什么故意以非零退出——它在报告什么状态？
   为什么这是成功条件而不是报错？
3. 你在练习里找到的那一行会让 starter 崩溃、被隔离，还是悄悄
   通过？

本检查点的认领码已经在默认命令的输出里——能回答这些问题之后再
提交。

## 预期证据

两条命令的输出记录，加上你对三个问题的回答。保存好，第 4 课会再次
用到。
