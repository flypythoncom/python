---
id: course-agent-rules-l04
type: course
title: "验证并接入流程"
summary: "证明验证器双向通过、跑完三个皮肤，然后把检查器接入你仓库的审查环。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "双套件加接线：两个方向都验证、三个皮肤都跑，然后把检查器接进你真正的评审环。"
  - title: "两个方向"
    body: "starter 在坏 scenario 上必须失败、在干净 scenario 上必须通过——`--expect-failure` 和普通运行告诉你自己在哪一侧。"
  - title: "接到咬得动的地方"
    body: "没人运行的检查器等于没人读的规则文件：把它加进你某个仓库的 pre-commit 或 CI，记下它第一次抓到了什么。"
---

# 验证并接入流程

## 目标

证明验证器双向通过、跑完三个皮肤，然后把检查器接入你仓库的审查环。

## 课程内容

运行 `python verify.py starter`（你改完后 11/11）与 `python verify.py solution`。然后真正用起来：把检查器指向你自己的仓库根目录并读报告。接入审查——pre-commit 钩子、CI 步骤或清单条目——让漂移大声失败。

## 练习

- 人工审查 diff：每处改动都必须有测试逼着
- 记录检查器不能证明什么（它读文件；看不见 Agent 行为）

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。
