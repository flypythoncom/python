---
id: product-slug-example
type: example
title: 3 分钟完成一次 AI Coding 修改
summary: 复现 Python 文本边界 Bug，完成范围明确的修复，并只用标准库验证结果。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# 3 分钟完成一次 AI Coding 修改

这个练习展示完整证据链：任务契约、稳定失败、边界明确的实现和自动检查。只需要
Python 3.11+。

```bash
python examples/product-slug/verify.py starter --expect-failure
python examples/product-slug/verify.py solution
```

第一条命令应报告“预期失败”，第二条命令应通过 4 项测试。然后把 [TASK_cn.md](TASK_cn.md)
交给 coding agent，要求它只修改 `starter/product_slug.py`，最后运行：

```bash
python examples/product-slug/verify.py starter
```

可以和 `solution/product_slug.py` 对照。目标不是复制相同语法，而是用小而可读的 diff
满足同一份契约。
