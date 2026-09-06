---
id: example-mcp-server
type: example
title: Model Context Protocol (MCP) 工具服务
summary: 构建符合 2026-07-28 无状态规范的 MCP 工具服务，实现无需 initialize 握手的 JSON-RPC 2.0 分发、参数校验、错误隔离与 input_required 多轮交互。
lang: zh-CN
content_version: 2
status: reviewed
reviewed_on: 2026-09-06
---

# Model Context Protocol (MCP) 工具服务

Model Context Protocol (MCP) 是连接 AI 模型与外部工具及数据的开放标准。
2026-07-28 规范以无状态为原则：移除了 `initialize` 握手与 `Mcp-Session-Id` 会话，
协议版本由每个请求通过 `_meta` 自描述，服务端主动发起的 elicitation 被替换为
`input_required` 多轮交互流程。

该规范下的生产级 MCP 服务端必须解析标准 JSON-RPC 2.0 请求，在没有任何握手的前提
下直接响应 `tools/list` 与 `tools/call`，校验工具入参，优雅捕获执行异常，并允许
工具通过 `resultType: "input_required"` 的结果向客户端请求补充输入——客户端携带
`inputResponses` 重试同一请求即可完成交互。

```bash
python examples/mcp-server/verify.py starter --expect-failure
python examples/mcp-server/verify.py solution
```

第一条命令复现朴素 starter 的预期失败；第二条命令验证符合契约的 solution。
把 [TASK_cn.md](TASK_cn.md) 提交给 coding agent，让其仅修改 `starter/mcp_server.py` 并运行：

```bash
python examples/mcp-server/verify.py starter
```

完整的迁移背景（2026-07-28 移除、废弃与强化的内容）见
[将 Python MCP 服务端迁移到 2026-07-28 规范](../../guides/mcp/migrate-2026-07-28_cn.md)。
