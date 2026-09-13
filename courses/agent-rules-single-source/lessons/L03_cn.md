---
id: course-agent-rules-l03
type: course
title: "按测试驱动一次有边界的变更"
summary: "让 starter 依次识别真源、指针、副本与漂移——一次一组失败测试。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "门控是 `python verify.py starter`——实现 `load_rule_files`、`is_pointer`、`check_directory`、`main`，十一个测试全绿。"
  - title: "分类顺序很关键"
    body: "`AGENTS.md` 缺失或为空产出 `missing-source` 且 `ok=false`。其余文件分 `pointer`、`copy`、`diverged`——先判指针和副本再判漂移，没有任何漂移或缺失项时 `ok` 才为真。"
  - title: "输出形态"
    body: "`main` 打印 `ok=... files=... diverged=...`，仅当 ok 时退出 0——参数错误打印用法到 stderr 并返回 2。"
---

# 按测试驱动一次有边界的变更

## 目标

让 starter 依次识别真源、指针、副本与漂移——一次一组失败测试。

## 课程内容

对 Agent 说：“按 TASK.md 修改 starter/rules_check.py，一次只处理一组失败测试：先指针识别，再真源要求，再副本/漂移分类，最后 CLI 退出码。每组之后给我看 diff。”

## 练习

- 每组之后运行 PYTHONPATH=starter python -m unittest discover -s tests -v
- 拒绝任何触碰 tests/、solution/ 或 scenario/ 的改动

## 检查点

本课的命令运行通过，并且你能用自己的话回答下面的问题（由 Agent
提问、你作答——这就是关口）：

1. 本课跑了哪条命令，它判定了什么？
2. 一开始什么失败了、为什么——用你自己的话说？
3. 下次再信任类似的改动之前，你会先检查什么？

## 预期证据

命令输出记录与你的回答。
