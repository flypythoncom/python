---
id: course-agent-rules-l02
type: course
title: "确定唯一真源"
summary: "AGENTS.md 成为 Agent 唯一阅读的文件；其余都只能是指针或副本——先决定，再写下来。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "定出唯一真源：`AGENTS.md` 是 Agent 真正读的文件，其余规则文件只能是薄指针或逐字节副本。"
  - title: "指针还是副本"
    body: "指针最多 10 个非空行且引用 `AGENTS.md`；副本与真源逐字节一致。其余都是 `diverged`。写下你自己仓库里每个文件会被判成哪类。"
  - title: "完成标准"
    body: "你的决定落了字：谁是真源，其余文件允许装什么。"
---

# 确定唯一真源

## 目标

AGENTS.md 成为 Agent 唯一阅读的文件；其余都只能是指针或副本——先决定，再写下来。

## 课程内容

读仓库自己的 AGENTS.md 与 `templates/AGENT_RULES.example.md`。本课程强制的决定是：AGENTS.md 是真源（AAIF 治理、Agent 原生的标准）；CLAUDE.md 与 .cursorrules 只能指向它。把你仓库的决定写成一句话——那句话就是你的契约。

## 练习

- 列出你的哪些规则文件在复述规则而不是指向真源
- 让 Agent 点评这句话里的歧义

## 检查点

本课的命令运行通过，并且你能用自己的话回答下面的问题（由 Agent
提问、你作答——这就是关口）：

1. 本课跑了哪条命令，它判定了什么？
2. 一开始什么失败了、为什么——用你自己的话说？
3. 下次再信任类似的改动之前，你会先检查什么？

## 预期证据

命令输出记录与你的回答。
