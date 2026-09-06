# 可运行示例

这些示例规模都很小。每一个都包含任务契约、带有缺陷的 starter、完整的 solution 以及
自动化验证脚本，让你可以在不盲目信任生成的代码的前提下练习 AI-coding 循环。

- [商品 Slug 边界回归](product-slug/README_cn.md)：复现文本边界 Bug，要求 Agent 给出最小修复，并验证方案。仅依赖标准库，约需 3 分钟。
- [不可信数据清洗校验](pydantic-validation/README_cn.md)：处理驼峰与下划线混杂入参、带符号金额清洗与结构化错误响应。
- [MCP 工具服务](mcp-server/README_cn.md)：构建符合 2026-07-28 无状态规范的 MCP 服务端：无需 initialize 握手、参数校验、错误隔离与 input_required 多轮交互。
- [受控并发异步抓取器](async-fetcher/README_cn.md)：使用 Semaphore 限制最大并发，对瞬时网络故障进行指数退避重试并聚合结构化结果。
- [鲁棒批处理数据流水线](structured-pipeline/README_cn.md)：使用标准库实现具备错误隔离、字段校验与统计汇总的安全批处理流水线。

[English index](README.md)
