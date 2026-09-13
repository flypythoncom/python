---
id: course-da-visualization-l01
type: course
title: "挑战 01：图是证据的包装"
summary: "写码前先说出每张 PNG 声明什么——JSON 摘要才是可审计层。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "图表是打包好的证据：写码前先说出每张 PNG 声明什么——`revenue_by_region` 声明地区总计、`daily_revenue` 声明趋势、`revenue_histogram` 声明分布。"
  - title: "先声明后像素"
    body: "数字错了的图是排版精良的谎言——JSON 汇总才是 PNG 必须对得上的可审计层。"
  - title: "完成标准"
    body: "你能说清三条声明，以及各自吃哪个聚合。"
---

# 挑战 01：图是证据的包装

**判卷：** 自我声明 · **积分：** 10

每张图都是关于数字的一种声称。写代码之前，先说出三张规定的图各自
在*声称*什么：

- `revenue_by_region.png` 声称：“各地区总额是 X、Y、Z。”
- `daily_revenue.png` 声称：“每日序列长这样。”
- `revenue_histogram.png` 声称：“行级收入的分布长这样。”

声称要是错了，图越漂亮越糟糕。

**检查点：** 你能说出每张图背后的声称。自我声明；用
`python verify.py progress` 记录。
