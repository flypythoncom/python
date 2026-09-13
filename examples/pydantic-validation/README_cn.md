---
id: example-pydantic-validation
type: example
title: 验证不可信边界请求体
summary: 使用字段规范化与结构化错误契约，清洗并验证混乱的外部数据载荷。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# 验证不可信边界请求体

本练习刻意只使用标准库：亲手实现 Pydantic 等校验库自动完成的规范化与验证机制，
让边界规则清晰可见。生产环境中请直接使用 Pydantic——见目录中收录的
[Pydantic 官方文档](https://pydantic.dev/docs/validation/latest/get-started/)。

来自 Webhook、客户端或 LLM 工具调用的数据是不可信的。它们经常携带驼峰与下划线混杂的键名、
带符号的金额字符串或非法的枚举状态。生产级边界验证器必须在容忍合法变体的同时清洗数据，并在
遇到非法输入时返回明确的结构化错误，绝不能抛出未捕获的 500 异常崩溃。

```bash
python examples/pydantic-validation/verify.py starter --expect-failure
python examples/pydantic-validation/verify.py solution
```

第一条命令展示朴素 starter 的预期失败；第二条命令验证健壮的 solution。
把 [TASK_cn.md](TASK_cn.md) 提交给 coding agent，让其仅修改 `starter/validator.py` 并运行：

```bash
python examples/pydantic-validation/verify.py starter
```

---

在 [flypython.com](https://flypython.com/examples/zh/pydantic-validation) 查看本示例的在线版本：可浏览的任务契约、分步说明与每个示例的当前审核状态。
