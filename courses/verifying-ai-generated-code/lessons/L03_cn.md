---
id: course-verify-ship-l03
type: course
title: "按测试逐组构建 ship check"
summary: "解析、判定、未验证清单、原子写入、退出码——一次一组失败测试。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "`python verify.py starter`——实现 `run_checks`、`build_record`、`write_record`、`run_project`、`main`，套件全绿。"
  - title: "要解析不要猜"
    body: "`ran` 来自 `Ran N tests in ...`——解析 unittest 的汇总行。`ran == 0` 时无论退出码如何 `result` 都是 'no-tests'，退出码非零是 'failed'，否则 'ok'。"
  - title: "原子写加退出码"
    body: "`write_record` 用同级临时文件加 `os.replace` 并创建父目录；`main` 打印 `all_passed=... checks=...`，全过返回 0 否则 1，用法错误返回 2。"
---

# 按测试逐组构建 ship check

## 目标

解析、判定、未验证清单、原子写入、退出码——一次一组失败测试。

## 课程内容

对 Agent 说：“按 TASK.md 修改 starter/ship_check.py，一次只处理一组失败测试：先解析，再判定，再未验证清单，再原子写入，最后 CLI 退出码。每组之后给我看 diff。”

## 练习

- 每组之后运行 PYTHONPATH=starter python -m unittest discover -s tests -v
- 绝不允许为了过测试而弱化判定

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。
