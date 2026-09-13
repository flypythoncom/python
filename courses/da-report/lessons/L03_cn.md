---
id: course-da-report-l03
type: course
title: "挑战 03：构建并渲染报告"
summary: "metrics 原样透传，先 # 标题再按序 ## 小节，金额两位小数。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "`python verify.py starter`——`load_inputs`、`build_report`、`render_markdown`、`write_report`、`main` 全绿。"
  - title: "透传不重算"
    body: "`metrics` 原样携带输入——套件精确比对数字，重算出不同结果的报告是 bug 不是特色。"
  - title: "输出形态要精确"
    body: "`render_markdown` 先输出 `# <标题>` 再按序输出 `## <小节>`；金额两位小数字形如 `33347.89`；`report.json` 用 UTF-8、缩进 2、结尾换行。"
---

# 挑战 03：构建并渲染报告

**判卷：** 客观——starter 套件 · **积分：** 10

在 `starter/report.py` 里实现契约。注意：

- 重新计算指标而不是原样传递输入——套件对数字是精确比对。
- 标题偏离规格——`## Data quality`、`## Findings`、`## Appendix`，
  顺序固定。
- 数字格式：`33347.89` 必须以两位小数出现。

**检查点：** `python verify.py starter` 退出 0。用
`python verify.py` 取认领码。
