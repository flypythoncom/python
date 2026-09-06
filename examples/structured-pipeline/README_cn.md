---
id: structured-pipeline-example
type: example
title: 鲁棒批处理数据流水线
summary: 使用标准库实现具备错误隔离、类型校验与批处理统计的鲁棒数据流水线。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# 鲁棒批处理数据流水线

本练习演示如何安全处理半结构化批量数据：隔离坏数据避免级联崩溃、严格校验输入字段、产出结构化汇总报告。仅依赖 Python 3.11+ 标准库。

```bash
python examples/structured-pipeline/verify.py starter --expect-failure
python examples/structured-pipeline/verify.py solution
```

第一条命令应报告“预期失败”（未处理异常、缺少批处理护栏）；第二条命令应全部通过。
随后将 [TASK_cn.md](TASK_cn.md) 提供给 Coding Agent（Cursor、Windsurf、Claude Code 等），要求其修复 `starter/pipeline.py`。
使用以下命令验证：

```bash
python examples/structured-pipeline/verify.py starter
```
