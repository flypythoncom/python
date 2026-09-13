# 学习路线

学习路线把挑战课程串成徽章路线。每条路线一个文件夹，包含机器可校验的
`path.json` 契约与双语的模块、挑战文档。

- [Agent 工具基础](foundation/)——驱动 Claude Code 与 Codex CLI，写出单一
  真源规则文件，并亲手验证 Agent 的产出。模块：一个入门模块、四门实战
  课程，以及一个双 Agent 路线挑战（200 分）。
- [用 Agent 做数据分析](data-analysis/)——对真实数据集完成清洗、探索、
  可视化与报告。模块：`da-eda`、`da-visualization`、`da-report` 三门课程，
  外加一个端到端综合项目（200 分）。

## 约定

- `path.json` 是契约：模块顺序、课程引用、积分与徽章定义。
  `python tools/verify_paths.py` 会把每条路线与 `courses/` 中实际存在的
  课程对照校验。
- 模块文档（`modules/*.md`）必须在同一次变更中附带 `_cn.md` 配对。
- 路线综合项目自带 `TASK.md`/`TASK_cn.md`、starter 输入、审核过的
  `solution/` 与守卫路线徽章的 `verify.py`。
- 积分只来自 `verify.py` 判卷通过并经认领码记录的检查点；徽章是
  自我报告的本地证据，绝不是证书。

引导式体验可继续在 [flypython.com](https://flypython.com/) 上进行。
