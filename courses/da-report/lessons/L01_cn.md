---
id: course-da-report-l01
type: course
title: "挑战 01：报告是与读者的契约"
summary: "列出报告必须携带哪些数字，以及各自来自 results.json 的哪个字段。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "报告是与读者的契约：列出它必须携带哪些数字——`total_revenue`、`rows_clean`、`top_category`、`revenue_by_region`——以及各自来自 `results.json` 的哪个字段。"
  - title: "先追溯再动笔"
    body: "报告里每个数字都映射到输入包的某个字段；追溯不了的数字不该进报告。"
  - title: "完成标准"
    body: "你的清单把报告里每个数字和来源字段配了对。"
---

# 挑战 01：报告是与读者的契约

**判卷：** 自我声明 · **积分：** 10

报告向读者承诺：“这些数字来自这份数据。”写代码之前，列出你的报告
必须携带的数字——`total_revenue`、`rows_clean`、`top_category`、
`revenue_by_region`——以及它们在 `results.json` 里的出处。

**检查点：** 每个必需数字你都能回溯到来源字段。自我声明；用
`python verify.py` 记录。
