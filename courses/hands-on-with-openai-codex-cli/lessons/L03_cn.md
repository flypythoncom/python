---
id: course-codex-cli-l03
type: course
title: "第 3 课：按测试驱动一次有边界的变更"
summary: "监督 Codex 完成七个小 diff——最小变更、不新增依赖、一次一组失败测试。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "`python verify.py starter` 九测全绿。监督 Codex 做小步修改：`load_records`、`build_report`、`write_report`、`main`——每条指令只推一组失败。"
  - title: "套件断言的坑"
    body: "布尔值不是数字——在 `int` 判断前先排除 `bool`。分组总计两位小数；全部行非法时 `total = valid + invalid` 仍须成立。"
  - title: "原子写"
    body: "同级临时文件加 `os.replace`；成功不留 `.tmp`。如果 Codex 直接写目标文件，那就是你要驳回的 diff。"
---

# 第 3 课：按测试驱动一次有边界的变更

## 目标

监督 Codex 完成七个小 diff——最小变更、不新增依赖、一次一组失败测试。

## 课程内容

对 Codex 说：“按 TASK.md 修改 starter/report_tool.py，一次只处理一组失败测试；每组完成后跑测试套件、给我看 diff，再继续。”失败数应逐组下降 7 → 5 → 4 → 3 → 2 → 0。它若改 `tests/`、`solution/` 或 `scenario/`——停下来问为什么。它想改测试？答案是不。

## 练习

- 每组之后运行 PYTHONPATH=starter python -m unittest discover -s tests -v
- 只剩端到端测试时，最后一组自己写

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。第 4 课会再次用到。
