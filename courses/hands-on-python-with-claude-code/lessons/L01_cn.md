---
id: course-claude-code-l01
type: course
title: "第 1 课：先复现故障，再谈修复"
summary: 打开课程文件夹，认识 starter，用 verify.py 把"坏了"变成客观证据——这是"能跑"与"能交付"的分水岭。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "考你能不能先复现故障再谈修复：`python verify.py starter --expect-failure` 必须打印出那组具名失败测试。重点是让失败变成客观证据，而不是修好它。"
  - title: "把失败名当成契约读"
    body: "每个失败的测试名都对应 `TASK.md` 里的一行——比如 `test_non_numeric_amount_is_invalid` 对应契约的『非数值的 numeric_field 值』。如果有名字对不上契约，那处漂移值得注意。"
  - title: "完成标准"
    body: "你能说清楚这九个测试各自证明了什么、为什么 starter 装不出来。然后 `python verify.py progress` 就会显示本检查点的认领码。"
---

# 第 1 课：先复现故障，再谈修复

## 目标

完成本课后，你能运行课程的客观验证命令，用测试名说清"starter 失败"
的含义，并指出缺失的四个产品行为。本课不改任何代码。

## 为什么要有这一课

大多数 AI 写的 Python 死法相同：演示输入没问题，真实输入一到，脚本
在第 3 行崩溃——或者更糟，悄悄算出一个错误的数字。修复不是从更好的
提示词开始，而是从把"它坏了"变成一条任何人运行都能得到同样结果的
命令开始。

## 热身（2 分钟）

打开 `starter/report_tool.py` 从头读一遍。它看起来很像样：带 docstring
的函数、类型标注、命令行入口。这正是 AI 生成代码的典型样子——表面
干净，行为缺失。然后打开 `TASK.md` 放在手边。

## 课程内容

在课程根目录运行客观验证命令：

```bash
python verify.py starter --expect-failure
```

你会看到 starter 复现四类真实世界的故障，并与测试名一一对应：

| 失败的测试 | 现实含义 |
| --- | --- |
| `test_load_json_records_returns_list_of_dicts` | 工具只认 CSV；API 场景直接崩溃 |
| `test_unsupported_suffix_raises_value_error` | 上传 `.xlsx` 得到一坨看不懂的报错，而不是清晰的拒绝 |
| `test_invalid_records_are_isolated_with_reasons` | 一个空单元格让整次运行中止——既没有部分报告，也没有原因 |
| `test_group_totals_are_rounded_to_two_decimals` | 报告里 `0.1 + 0.2` 打印成 `0.30000000000000004` |
| `test_write_report_creates_missing_parent_directories` | 工具无法写入新建的输出目录 |
| `test_run_scenario_writes_report_file`、`test_main_prints_summary_and_returns_zero` | 以上问题在端到端层面的体现 |

再用同样的方式运行已审核的实现：

```bash
python verify.py solution
```

两条命令都退出 0——但含义相反。第一条证明 starter 处于"正确的未完成"
状态；第二条证明目标可达。这一对命令就是整个课程的完成证据。

## 练习

选一个你最有代入感的皮肤（`excel-report`、`data-monitor` 或
`api-tool`），打开它的数据文件，找出会被拒绝的行。在运行任何命令
之前，写下每个坏行会触发哪条测试，然后对照上面的表格检查。

## 检查点

运行 `python verify.py starter --expect-failure` 和
`python verify.py solution`。不看资料回答出以下三问，即通过本课：

1. 分隔 starter 与 solution 的是哪四个行为？
2. 为什么"预期失败"是成功条件而不是矛盾？
3. 你在练习中找到的那一行，对 starter 是崩溃、隔离还是悄悄通过？

## 预期证据

两条命令的输出记录，加上你对三个问题的回答。保存好，第 4 课会再次
用到。
