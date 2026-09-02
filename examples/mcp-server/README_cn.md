---
id: example-mcp-server
type: example
title: Model Context Protocol (MCP) 工具服务
summary: 构建规范安全的 JSON-RPC 2.0 MCP 工具服务，实现参数校验与结构化错误边界。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Model Context Protocol (MCP) 工具服务

Model Context Protocol (MCP) 是连接 AI 模型与外部工具及数据的开放标准。
生产级 MCP 服务端必须解析标准 JSON-RPC 2.0 请求，响应 `tools/list` 工具模式定义，
校验工具入参，优雅捕获执行异常，并防止未处理的异常打断传输通信流。

```bash
python examples/mcp-server/verify.py starter --expect-failure
python examples/mcp-server/verify.py solution
```

第一条命令复现朴素 starter 的预期失败；第二条命令验证符合契约的 solution。
把 [TASK_cn.md](TASK_cn.md) 提交给 coding agent，让其仅修改 `starter/mcp_server.py` 并运行：

```bash
python examples/mcp-server/verify.py starter
```
