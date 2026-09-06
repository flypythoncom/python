---
id: mcp-2026-07-28-migration
type: guide
title: 将 Python MCP 服务端迁移到 2026-07-28 规范
summary: 面向 2026-07-28 无状态规范更新 Python MCP 服务端，移除 initialize 握手、采用 input_required 多轮交互、放弃废弃特性并强化授权。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-06
---

# 将 Python MCP 服务端迁移到 2026-07-28 规范

2026-07-28 的 Model Context Protocol 规范是 remote MCP 之后最大的一次发布：它彻底
移除了 initialize 握手，用 `input_required` 多轮交互取代服务端主动发起的请求，并
废弃了 roots、sampling 和 logging。MCP 现由 Linux 基金会旗下的 Agentic AI
Foundation 管理，Python SDK 已随规范同步发布。

迁移完成的标准：你的服务端在完全不依赖任何会话状态的情况下响应 `tools/list` 与
`tools/call`，没有任何工具依赖已废弃的服务端主动请求，且授权链路满足新的发行方
（issuer）规则。

## 2026-07-28 改了什么

- **无状态优先（SEP-2575、SEP-2567）。** `initialize`/`initialized` 交互与
  `Mcp-Session-Id` 头被移除。每个请求通过 `_meta` 自描述协议版本、客户端身份与
  能力；需要提前获取能力的客户端可以使用可选的 `server/discover` RPC。
- **多轮交互取代服务端主动请求（SEP-2322）。** `elicitation/create`、
  `sampling/createMessage` 和 `roots/list` 不再保持长连接。需要客户端输入的工具
  返回带 `resultType: "input_required"` 的结果以及待回答的请求；客户端携带
  `inputResponses` 重试原始调用。
- **按请求传递版本与路由头（SEP-2243）。** `MCP-Protocol-Version` 随每个请求传递
  （值为 `2026-07-28`），Streamable HTTP 请求必须携带 `Mcp-Method` 和 `Mcp-Name`，
  让基础设施无需解析 JSON 请求体即可路由。
- **授权强化。** 授权服务器必须按 RFC 9207 返回 `iss` 参数（SEP-2468），客户端在
  动态注册时必须设置 `application_type`（SEP-837），客户端凭据与发行方绑定——绝不
  能跨授权服务器复用（SEP-2352）。
- **响应缓存（SEP-2549）。** `tools/list`、`prompts/list`、`resources/list` 和
  `resources/read` 的响应携带 `ttlMs` 与 `cacheScope`。
- **Tasks 重构（SEP-2663）。** Tasks 移入 `io.modelcontextprotocol/tasks` 扩展，
  采用轮询式 `tasks/get` 与新增的 `tasks/update`，变更通知迁移到
  `subscriptions/listen` 流。
- **至少十二个月窗口的废弃项。** Roots、sampling 和 logging 被废弃
  （SEP-2577）；传统 HTTP+SSE 传输有一年过渡期；动态客户端注册（DCR）由客户端
  ID 元数据文档（CIMD）取代。

## 迁移清单

1. **删除握手。** 移除 `initialize` 与 `notifications/initialized` 的处理，以及所有
   `Mcp-Session-Id` 查找。仍然发送 `initialize` 的请求应按未知方法失败，而不是被
   协商。
2. **让每个请求自洽。** 服务端以前从 initialize 记住的一切——客户端能力、协议版
   本、身份——现在必须按请求从 `_meta` 读取，或在客户端主动选择时通过
   `server/discover` 获取。
3. **用 input_required 交互取代 elicitation。** 过去调用 `elicitation/create` 的工
   具现在返回带提问的 `resultType: "input_required"`，并在客户端携带
   `inputResponses` 重试时完成。
4. **不要在废弃原语上新建代码。** Roots、sampling 和 logging 在废弃窗口内仍然可
   用，但新代码不应再依赖它们。
5. **升级官方 Python SDK。** TypeScript、Python、Go 和 C# SDK 已随规范发布；从 RC
   到正式版大约有十周窗口，更早的 SDK 版本早于这些破坏性变更。
6. **更新传输层。** 在一年过渡期内下线传统 HTTP+SSE 传输，并在 Streamable HTTP 上
   输出必需的 `Mcp-Method` 与 `Mcp-Name` 头。
7. **检查授权链路。** 按 RFC 9207 校验 `iss`，注册时设置 `application_type`，每个
   发行方使用独立凭据。
8. **采用缓存元数据。** 为列表响应标注 `ttlMs` 与 `cacheScope`，让无状态基础设施
   可以安全缓存。

## input_required 流程代码

可运行的完整参考在 [examples/mcp-server](../../examples/mcp-server/README_cn.md)。
核心形状如下：

```python
class InputRequired(Exception):
    def __init__(self, requests):
        super().__init__("tool execution needs additional client input")
        self.requests = requests


def delete_resource(args, input_responses=None):
    answer = str((input_responses or {}).get("confirm", "")).strip().lower()
    if answer != "yes":
        raise InputRequired([{"id": "confirm", "prompt": "Type 'yes' to confirm deletion."}])
    return "deleted"
```

服务端在通用异常处理之前捕获 `InputRequired`，返回：

```json
{
  "result": {
    "resultType": "input_required",
    "requests": [{"id": "confirm", "prompt": "Type 'yes' to confirm deletion."}],
    "content": [{"type": "text", "text": "Additional client input is required before this tool can finish."}]
  }
}
```

客户端携带 `"inputResponses": {"confirm": "yes"}` 重试完全相同的 `tools/call`。因为
整个流程基于重试，未确认的调用不会产生任何副作用——这与幂等自动化的安全性质完全
一致。

验证完整行为，包括 JSON-RPC 错误码与被移除的握手：

```bash
python examples/mcp-server/verify.py starter --expect-failure
python examples/mcp-server/verify.py solution
```

## 本指南不覆盖的内容

本指南基于已发布的发布公告与随规范交付的 SDK。`_meta`、`requests` 条目和
`cacheScope` 取值的字段级线缆协议请以规范与 SDK 类型定义为准，上线前务必核对；生
产环境优先使用官方 Python SDK 而不是手写分发逻辑。授权的部署细节——发行方发现、
凭据存储与 CIMD 的推进节奏——同样不在本指南范围内。

## 来源

- [2026-07-28 MCP 规范发布公告](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [2026-07-28 RC 与破坏性变更概览](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)
- [Anthropic：将 MCP 捐给 Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- [Agentic AI Foundation 下的 MCP](https://aaif.io/projects/model-context-protocol)
