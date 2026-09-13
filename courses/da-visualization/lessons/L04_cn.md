---
id: course-da-visualization-l04
type: course
title: "挑战 04：数字与图一致"
summary: "summary.json 对照真值校验；图与 JSON 不一致就是失败的图。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "双套件：`summary.json` 对真值——East 12334.94、North 14294.7、South 11200.48、总计 37830.12、45 天。"
  - title: "JSON 是审计层"
    body: "图上的数和 JSON 不一致就是失败的图——两者对不上时几乎总是 JSON 对。"
  - title: "完成标准"
    body: "`summary.json` 每个数字都对得上数据集真值，且都能追溯到它的聚合。"
---

# 挑战 04：数字与图一致

**判卷：** 客观——双套件 · **积分：** 10

套件用数据集真值校验 `summary.json`（East 12334.94、North 14294.7、
South 11200.48、总计 37830.12、45 天）。图里呈现的数字和 JSON 不一致，
就是失败的图——JSON 才是可审计的那一层。

`python verify.py starter --expect-failure` 现在必须退出非零；
`python verify.py solution` 必须全绿。

**检查点：** 两道门禁都过。用 `python verify.py progress` 取客观
认领码。
