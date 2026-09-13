---
id: course-da-visualization-l03
type: course
title: "挑战 03：三张图与摘要"
summary: "在 starter/charts.py 实现契约——Agg 先于 pyplot、日期先解析、真 PNG 字节。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "`python verify.py starter`——`load_sales`、`summary`、三个画图函数和 `main` 全绿。"
  - title: "Agg 要在 pyplot 之前"
    body: "`matplotlib.use('Agg')` 必须先于导入 pyplot 执行，否则在没有显示器的机器上直接死。`date` 也要先解析——对未解析字符串 `groupby` 是按字典序排的。"
  - title: "必须是真 PNG"
    body: "套件查的是 magic bytes 不是文件存不存在——用 `savefig` 写到契约点名的 `out/` 路径，`summary.json` 用 UTF-8、缩进 2、结尾换行。"
---

# 挑战 03：三张图与摘要

**判卷：** 客观——starter 套件 · **积分：** 10

在 `starter/charts.py` 里实现契约。驱动 Agent 时的要点：

- `matplotlib.use("Agg")` 必须在导入 pyplot *之前*执行，否则在没有
  显示器的机器上直接崩。
- 在未解析的字符串列上 `groupby("date")` 会按字典序排——先解析日期。
- 测试检查 PNG 魔数：不是真 PNG 的文件会失败。

**检查点：** `python verify.py starter` 退出 0。用
`python verify.py` 取认领码。
