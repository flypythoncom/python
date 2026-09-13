---
id: course-mcp-tools-l02
type: course
title: "JSON-RPC 分发契约"
summary: "合法请求回显 id；非法请求得 -32600；未知或已移除的方法得 -32601。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "分发契约：合法请求回显 `id`，畸形请求得 -32600，未知或已删除的方法得 -32601。"
  - title: "版本门"
    body: "携带非 `2026-07-28` 的 `_meta.protocolVersion` 的请求得 -32600——请求自我声明版本而不是协商版本。"
  - title: "完成标准"
    body: "凭记忆能填真值表：正常请求、坏 jsonrpc、未知方法、已删方法、错版本。"
---

# JSON-RPC 分发契约

## 目标

合法请求回显 id；非法请求得 -32600；未知或已移除的方法得 -32601。

## 课程内容

分发规则小而可测：检查 jsonrpc 与 method、保留 id、用正确的错误码作答。先跑失败的分发测试，用最小的步骤让它们通过。Agent 工作时，把 01-tools-list.json 与 04-removed-initialize.json 当作夹具。

## 练习

- 问 Agent：initialize 为什么必须返回 -32601，并在消息里点明 2026-07-28 的移除
- 拒绝任何触碰 tests/ 或 solution/ 的 diff

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。
