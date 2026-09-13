---
id: course-mcp-tools-l01
type: course
title: "MCP 到底是什么（2026-07-28）"
summary: "一个面向工具的无状态 JSON-RPC 2.0 接口——无握手、无会话、版本放在 _meta 里。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "先理解形态再写码：MCP 2026-07-28 是无状态 JSON-RPC 2.0 接口——没有 initialize 握手、没有会话、版本走 `_meta.protocolVersion`。"
  - title: "说出缺了什么"
    body: "列出旧流程里被本规范删掉的东西：initialize、sessions、roots、sampling。收到 `initialize` 时正确回答是 -32601 错误，不是握手。"
  - title: "完成标准"
    body: "一句话说清整个生命周期：进来一个请求 dict，出去一个响应 dict。"
---

# MCP 到底是什么（2026-07-28）

## 目标

一个面向工具的无状态 JSON-RPC 2.0 接口——无握手、无会话、版本放在 _meta 里。

## 课程内容

读 TASK.md，然后双向运行验证器。2026-07-28 规范移除了 initialize 握手与会话：服务端直接响应 tools/list 与 tools/call，每个请求通过 _meta 自报协议版本。边读边手动试 scenario/requests/ 里的线路样本。

## 练习

- 先预测 04-removed-initialize.json 的响应，再对照 TASK.md
- 把 starter 的每个预期失败对应到一条规范

## 检查点

本课的命令运行通过，并且你能用自己的话回答下面的问题（由 Agent
提问、你作答——这就是关口）：

1. 本课跑了哪条命令，它判定了什么？
2. 一开始什么失败了、为什么——用你自己的话说？
3. 下次再信任类似的改动之前，你会先检查什么？

## 预期证据

命令输出记录与你的回答。
