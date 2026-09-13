---
id: course-deepseek-harness-l01
type: course
title: "第 1 课：复现故障，从轨迹里读回来"
summary: "让 Harness 组装的 Agent 跑在课程文件夹上，用 verify.py 让失败变得客观——再读只增轨迹，看清 Agent 到底做了什么。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-13
hints:
  - title: "本检查点考察什么"
    body: "先复现失败再动手修：`python verify.py starter --expect-failure` 必须打印出点名的失败测试——你自己跑也好、Agent 的 shell 工具跑也好，命令就是证据。"
  - title: "一切皆插件"
    body: "DeepSeek Harness 的 Agent 是组装出来的，不是内置的：模型、工具、会话存储、循环本身都是 `cordis.yml` 里接好的插件。某个行为没有，答案通常是插件——不是某个开关。"
  - title: "轨迹就是你的记录"
    body: "每一步都落进可事后检查的只增会话/轨迹日志。读回轨迹才能验证 Agent 实际做了什么——而不是它声称做了什么。"
  - title: "完成的标志"
    body: "你能说出套件证明了哪九种行为、为什么 starter 伪造不出来。`python verify.py progress` 随即显示本检查点的认领码。"
---

# 第 1 课：复现故障，从轨迹里读回来

## 目标

本课结束时，你有一个指向课程文件夹的 DeepSeek Harness 会话，跑过
课程的客观验证命令，并能对照会话轨迹解释「starter 失败」在测试名
里的含义。本课不改任何代码。

## 为什么有这节课

AI 写的 Python 大多是同一种死法：演示输入能跑，真实输入一到，脚本
在第 3 行崩掉——或者更糟，悄悄算出一个错的数。修复不从更好的
提示词开始，而从把「坏了」变成一条任何人都能跑、且得到相同答案的
命令开始。DeepSeek Harness 再加一层：你跑的 Agent 是*组装*出来的
——模型、工具、存储、循环都是 `cordis.yml` 里接好的插件——它走的
每一步都落进可检查、可搜索、可重放的只增轨迹日志。「相信我」变成
「这是轨迹」。

## 热身（2 分钟）

打开 `starter/report_tool.py`，从头读到尾。它看起来很合理：带
docstring 的函数、类型标注、CLI。这正是 AI 生成代码的样子——
表面干净、行为缺失。现在打开 `TASK.md`，放在手边。

## 本课内容

让 Harness 会话跑在课程文件夹里，对 Agent 说：

**“读 COURSE.md——它是本文件夹的教学契约。再读 TASK.md 和
starter/report_tool.py。不要改任何文件。告诉我测试期望哪些行为、
starter 缺了哪些。”**

趁它读的时候，跑客观验证——自己在终端里跑，或通过 Agent 的
shell/沙箱工具跑：

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

然后跑评审过的实现：

```bash
python verify.py solution
```

两条命令都以 0 退出——但含义相反。第一条证明 starter *确实处于
正确的未完成态*；第二条证明目标可达。

现在做 Harness 原生的一步：检查会话轨迹。找到 Agent 读 `TASK.md`、
跑（或被告知）verify 命令、产出总结的那几步。轨迹是只增的——它是
发生之事的底账，也是以后让 Agent 工作可审计的依据。

## 练习

挑一个你最有代入感的场景皮肤（`excel-report`、`data-monitor` 或
`api-tool`），打开它的数据文件，找出会被拒绝的行。先不看运行结果，
写下每个坏行会触发哪个测试，再对照上面的表自查——并在轨迹里找到
Agent 得出相同结论的那一步。

## 检查点

运行 `python verify.py starter --expect-failure` 和
`python verify.py solution`。不看材料能回答下面三个问题即算通过：

1. 哪四个行为把 starter 和 solution 区分开？
2. 为什么「预期失败」是成功条件而不是自相矛盾？
3. 在轨迹的哪里能证明 Agent 确实读过 `TASK.md`？

## 预期证据

两条命令的完整输出记录、你找到的轨迹步骤、加你的三个答案。保留好
——第 4 课还会用到。
