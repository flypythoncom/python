---
id: course-da-report-l04
type: course
title: "挑战 04：数字可回溯到输入"
summary: "report.json 每个指标等于源字段——审计答案是字段名，不是解释。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "双套件：`report.json` 里每个指标等于 `results.json` 里的源值——审计答案是一个字段名，不是一段解释。"
  - title: "追溯之问"
    body: "对报告里每个数字回答『它从哪来』，答案必须是输入字段。哪个答案变成了一句话，那个数字就可疑。"
  - title: "完成标准"
    body: "所有指标逐数字可追溯，且你能说出各自在哪个小节。"
---

# 挑战 04：数字可回溯到输入

**判卷：** 客观——双套件 · **积分：** 10

`report.json` 里的每个指标都必须与 `results.json` 中的来源逐数相等。
本挑战回答的审计问题是：“这个数字从哪来的？”——答案是字段名，
不是一段解释。

`python verify.py starter --expect-failure` 现在必须退出非零；
`python verify.py solution` 必须全绿。

**检查点：** 两道门禁都过。用 `python verify.py` 取客观
认领码。
