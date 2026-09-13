---
id: course-mcp-tools-l03
type: course
title: "校验与错误隔离"
summary: "参数是不可信输入：先校验再执行，绝不让处理函数打断传输。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "`python verify.py starter`——实现 `MCPServer` 的 `register_tool` 与 `handle_request`：校验、分发、错误隔离全绿。"
  - title: "工具是不可信输入"
    body: "缺必填参数 → `isError` 内容 'Missing required argument: <arg>'；未知工具 → 'Tool not found'；处理函数抛异常 → `isError` 'Error: <e>'。工具失败绝不能打断传输层。"
  - title: "返回形态"
    body: "`tools/list` 产出带 name/description/inputSchema 的 `result.tools`；`tools/call` 产出 text 型 `result.content`——信封结构要精确，套件比对的是结构。"
---

# 校验与错误隔离

## 目标

参数是不可信输入：先校验再执行，绝不让处理函数打断传输。

## 课程内容

两条边界让工具服务变得安全：按声明的 inputSchema 校验必填参数（缺参变成结构化结果而不是异常），并包裹每个处理函数，让它的失败返回 isError 而不是断开连接。03-missing-argument.json 在线路上演示了第一条边界。

## 练习

- 把每个校验测试对应到它锚定的契约行
- 问：如果处理函数抛出 InputRequired 会怎样？（下一课。）

## 检查点

本课的命令运行通过，并且你能用自己的话回答下面的问题（由 Agent
提问、你作答——这就是关口）：

1. 本课跑了哪条命令，它判定了什么？
2. 一开始什么失败了、为什么——用你自己的话说？
3. 下次再信任类似的改动之前，你会先检查什么？

## 预期证据

命令输出记录与你的回答。
