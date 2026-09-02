---
id: setup-structured-logging
type: playbook
title: 搭建生产级结构化日志
summary: 配置具备上下文贯穿、敏感数据脱敏与环境隔离的 JSON 结构化日志体系。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# 搭建生产级结构化日志

1. 生产环境统一采用 JSON 格式化输出，本地开发环境采用带色彩的高可读文本；避免随手写 `print()` 或无结构的字符串拼接。
2. 通过 Python 标准库 `contextvars` 将全局唯一的 `request_id` 或 `trace_id` 贯穿所有 HTTP 请求、后台任务与下游远程调用。
3. 规范日志事件数据结构：统一包含 ISO 8601 时间戳、日志级别、Logger 名称、事件标识、Trace ID 及结构化上下文键值对。
4. 在日志处理器中配置敏感字段自动脱敏过滤器（覆盖 `password`、`token`、`authorization`、`api_key` 及用户个人隐私信息）。
5. 仅在服务边界处使用 `exc_info=True` 捕获完整异常堆栈；禁止在多层嵌套的 `try...except` 中重复记录冗余的原始错误堆栈。
6. 在自动化测试中针对日志结构字典字段进行确切断言，而非脆弱的非结构化子串正则匹配。
