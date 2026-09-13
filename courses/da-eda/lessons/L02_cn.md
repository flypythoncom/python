---
id: course-da-eda-l02
type: course
title: "挑战 02：先定答案"
summary: "先勾出 results.json 的键、类型与舍入规则，再让 Agent 写 eda.py。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "先定义答案再让 Agent 生成：动手写 `eda.py` 之前先勾出 `results.json` 的键、类型和舍入规则。"
  - title: "契约先行"
    body: "定清楚 `total_revenue` 怎么舍入、`revenue_by_region` 键长什么样、`rows_total` 等于输入行数——套件比对的是精确数字。"
  - title: "完成标准"
    body: "你的草图列出 `results.json` 每个键和它的来源列。"
---

# 挑战 02：先定答案

**判卷：** 自我声明 · **积分：** 10

动手实现之前，先写下 `results.json` 的结构：有哪些键、什么类型、
什么舍入规则。`TASK.md` 定义的是*形式*——每个值"什么叫对"由你在
让 Agent 生成代码之前先想清楚。

这门课要消灭的反模式就是："Agent 写了代码、打印了点东西、上线吧。"
EDA 只有数字可核查才算数。

**检查点：** 你已写下期望键清单，并能解释每个键的含义。自我声明；
用 `python verify.py progress` 记录。
