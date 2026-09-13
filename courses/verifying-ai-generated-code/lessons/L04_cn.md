---
id: course-verify-ship-l04
type: course
title: "像怀疑者一样读记录"
summary: "绿、红、零测试是三件不同的事——证明你能分辨，并说清记录不能证明什么。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "双套件加怀疑者式读记录：绿、红、零测试产出不同判定——证明你分得清。"
  - title: "三个皮肤都跑"
    body: "对 green-project、red-project、no-tests 运行 `run_project`，分别得到 ok、failed、no-tests——拿契约核对每个 `SHIP-RECORD.json`，不要凭记忆。"
  - title: "记录证不了什么"
    body: "写一句绿色记录覆盖不了的事（比如测试本身写得好不好）——这句话就是本课。"
---

# 像怀疑者一样读记录

## 目标

绿、红、零测试是三件不同的事——证明你能分辨，并说清记录不能证明什么。

## 课程内容

对三个场景项目各跑一次完成的检查。逐份读 SHIP-RECORD.json：同一条命令，三种判定。`unverified` 清单不是免责声明——它是你主张的边界。审查 diff 里没有测试逼着的改动；用 `--verified-on` 确认记录可复现。

## 练习

- 人工核对：每份记录里 all_passed 是否与 exit_code 和 result 一致？
- 写下三行证据笔记：已验证 / 未验证 / 已知局限

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。
