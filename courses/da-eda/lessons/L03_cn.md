---
id: course-da-eda-l03
type: course
title: "挑战 03：清洗与统计"
summary: "实现 load_transactions、clean_transactions、summarize、write_results、main，十二个测试全绿。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "`python verify.py starter`——实现 `load_transactions`、`clean_transactions`、`summarize`、`write_results`、`main`，十二个测试全绿。"
  - title: "经典 EDA 陷阱"
    body: "`to_numeric` 不加 `errors='coerce'` 遇到 'n/a' 直接崩而不是计数；去重必须在原始行上做，否则脏行的完全重复会漏掉；`groupby().sum()` 会静默丢 NaN——清洗前先数缺陷。"
  - title: "契约细节"
    body: "stats 的键必须正好是 `duplicates_removed`、`missing_amount`、`bad_dates`；`total_revenue` 和地区值两位小数；日期输出 ISO `YYYY-MM-DD`。"
---

# 挑战 03：清洗与统计

**判卷：** 客观——starter 套件 · **积分：** 10

在 `starter/eda.py` 里实现 `load_transactions`、`clean_transactions`、
`summarize`、`write_results`、`main`。把 `TASK.md` 当契约驱动你的
Agent；它写的每一行都要过目。

注意这几个经典 EDA 陷阱：

- `to_numeric` 不带 `errors="coerce"` 会在 `n/a` 上崩溃而不是计数。
- 先过滤再去重会漏掉脏行的完全重复。
- `groupby().sum()` 会悄悄丢掉 NaN——清洗*之前*就要数清楚。

**检查点：** `python verify.py starter` 退出 0——12 个测试全过。
用 `python verify.py progress` 打印认领码。
