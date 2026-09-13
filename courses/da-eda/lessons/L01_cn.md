---
id: course-da-eda-l01
type: course
title: "挑战 01：脏数据长什么样"
summary: "动手写 pandas 之前先给商店导出数据画像：完全重复、无法解析的金额、一条坏日期——先把脏数清楚。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "先画像再写码：打开 `scenario/shop-export/transactions.csv`，亲手找出脏数据——完全重复行、解析不了的金额、一条坏日期。"
  - title: "先数一遍"
    body: "记下总行数和每类缺陷大约多少——套件比对的就是这些数，提前知道就是优势。"
  - title: "完成标准"
    body: "你能说出三类缺陷，以及各自大概有多脏。"
---

# 挑战 01：脏数据长什么样

**判卷：** 自我声明 · **积分：** 10

写代码之前先给输入做画像。打开
`scenario/shop-export/transactions.csv`（或让你的 Agent 来做），亲自
找出这些脏东西：

- 一共多少行？有多少完全重复行？
- 哪些 `amount` 值不是数字？
- 哪些 `date` 值不是日期？

**检查点：** 不跑测试套件也能说出三个数——总行数、重复数、不可解析
值数。用 `python verify.py` 记录你的认领（L01 为自我声明）。
