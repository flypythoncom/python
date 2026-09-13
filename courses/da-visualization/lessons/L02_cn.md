---
id: course-da-visualization-l02
type: course
title: "挑战 02：先写规格，再画图"
summary: "在打开 matplotlib 之前写清每张图吃哪个聚合、summary.json 必须装什么。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "先规格后图表：每张 PNG 吃哪个聚合、输入多少行、`summary.json` 必须有什么——都在打开 matplotlib 之前。"
  - title: "把数字写下来"
    body: "135 行、45 天、3 个地区——套件拿 `summary.json` 对真值，你的规格就是你批改 Agent 的参考答案。"
  - title: "完成标准"
    body: "你的规格列出每个输出文件和它必须携带的精确数字。"
---

# 挑战 02：先写规格，再画图

**判卷：** 自我声明 · **积分：** 10

画图之前先写规格：每张图吃哪个聚合结果、输入有多少行、
`summary.json` 必须含什么。你的 Agent 会很乐意渲染出*某种东西*——
你要做的是定义它必须渲染的数字。

**检查点：** 你已写下规格，把每个输出文件映射到它的聚合来源。
自我声明；用 `python verify.py` 记录。
