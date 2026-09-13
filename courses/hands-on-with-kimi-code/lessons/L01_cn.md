---
id: course-kimi-code-l01
type: course
title: "第 1 课：复现故障，用只读道做勘察"
summary: "在课程文件夹里运行 kimi，让只读的 explore 子代理摸清代码，用 verify.py 让失败变得客观。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-13
hints:
  - title: "本检查点考察什么"
    body: "先复现失败再动手修：`python verify.py starter --expect-failure` 必须打印出点名的失败测试——你自己跑也好、Agent 的 shell 工具跑也好，命令就是证据。"
  - title: "分道，不是一坨"
    body: "Kimi Code 自带内置子代理：`explore` 只读、`plan` 没有写和 shell 工具、`coder` 能读写跑命令。只读的活就放只读道——它弄不坏任何东西。"
  - title: "完成的标志"
    body: "你能说出套件证明了哪九种行为、为什么 starter 伪造不出来。`python verify.py progress` 随即显示本检查点的认领码。"
---

# 第 1 课：复现故障，用只读道做勘察

## 目标

本课结束时，你在课程文件夹里跑起了 `kimi`，运行过课程的客观验证
命令，并能解释「starter 失败」在测试名里的含义。本课不改任何代码。

## 为什么有这节课

AI 写的 Python 大多是同一种死法：演示输入能跑，真实输入一到，脚本
在第 3 行崩掉——或者更糟，悄悄算出一个错的数。修复不从更好的
提示词开始，而从把「坏了」变成一条任何人都能跑、且得到相同答案的
命令开始。Kimi Code 带来一种有用的分工：内置子代理把活分开——
`explore` 只读不写、`plan` 只做规划没有 shell 和写工具、`coder`
负责改代码。用只读道做勘察意味着探索阶段弄不坏任何东西。

## 热身（2 分钟）

打开 `starter/report_tool.py`，从头读到尾。它看起来很合理：带
docstring 的函数、类型标注、CLI。这正是 AI 生成代码的样子——
表面干净、行为缺失。现在打开 `TASK.md`，放在手边。

## 本课内容

在课程文件夹里启动 `kimi`。先要一份只读勘察——`explore` 子代理
能读文件但不能改：

**“用 explore 子代理读 COURSE.md、TASK.md 和
starter/report_tool.py。不要改任何文件。报告测试期望哪些行为、
starter 缺了哪些。”**

趁它读的时候，自己在终端里跑客观验证：

```bash
python verify.py starter --expect-failure
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

然后用同样的方式跑评审过的实现：

```bash
python verify.py solution
```

两条命令都以 0 退出——但含义相反。第一条证明 starter *确实处于
正确的未完成态*；第二条证明目标可达。这一对命令是整门课的完成
证据。

## 练习

挑一个你最有代入感的场景皮肤（`excel-report`、`data-monitor` 或
`api-tool`），打开它的数据文件，找出会被拒绝的行。先不看运行
结果，写下每个坏行会触发哪个测试，再对照上面的表自查——并让
`explore` 确认，而不是让 `coder` 修。

## 检查点

运行 `python verify.py starter --expect-failure` 和
`python verify.py solution`。不看材料能回答下面三个问题即算通过：

1. 哪四个行为把 starter 和 solution 区分开？
2. 为什么「预期失败」是成功条件而不是自相矛盾？
3. 哪个子代理能改文件——哪两个不能？

## 预期证据

两条命令的完整输出记录，加你的三个答案。保留好——第 4 课还会
用到。
