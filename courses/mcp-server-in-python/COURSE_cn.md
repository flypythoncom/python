---
id: course-mcp-tools
type: course
title: 用 MCP 给你的 Agent 装上工具（Python）
summary: 用纯 Python 构建一个无状态的 Model Context Protocol 工具服务——JSON-RPC 2.0 分发、schema 校验、错误隔离与 2026-07-28 的 input_required 多轮交互——并理解真正的工具该放在哪里。
lang: zh-CN
content_version: 3
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-mcp-tools
  name_en: MCP Tool Server
  name_zh: MCP 工具服务器
  requires: 全部五个检查点认领通过（L01–L05）
course_id: course-mcp-tools
---

# 用 MCP 给你的 Agent 装上工具（Python）

> 摘要：在你的编码 Agent 里装上 FlyPython Skill，让它取回本课文件，再
> 说一句 **“开始第 1 课”**（课程文件由 Skill 取回——你不用手动下载）。
> 课程结束时你拥有一个实现无状态 2026-07-28 规范的 MCP 工具服务——
> 无 initialize 握手、参数校验、处理异常隔离、input_required 多轮交互
> ——由一个失败的 starter 和一个通过的 solution 共同证明。仅用标准库；
> 无需 API Key。

## 你将做出什么

仓库作为可运行示例发布的同一个经过审核的 MCP 工具服务契约，组装成
课程：一个 `MCPServer` 类，直接响应 `tools/list` 与 `tools/call`，用
正确的 JSON-RPC 错误码拒绝坏请求，按声明的 schema 校验参数，把处理
函数的异常隔离为结构化 `isError` 结果，并完成 `input_required` 多轮
交互。`scenario/requests/` 下的请求样本让你在学习时直接试线路格式：

| 文件 | 演练什么 |
| --- | --- |
| `01-tools-list.json` | 无握手直接列出工具 |
| `02-echo-call.json` | 一次成功的 tools/call |
| `03-missing-argument.json` | 参数校验失败 |
| `04-removed-initialize.json` | 已移除的 initialize 方法 |

## 教学契约（Agent 请先阅读本节）

- **受众：** 想让 Agent 安全调用自己代码的开发者——想理解协议本身，
  而不是粘贴一个服务脚手架。
- **前置条件：** PATH 中有 Python 3.11+，能读 JSON，任一编码 Agent
  （以 Claude Code 2.x 完成教学与审核，审核日期 2026-09-12）。只用
  标准库。
- **课程顺序：** L01 → L05；绝不跳过检查点。
- **教学风格：** 从本文件夹的文件出发；引用你满足的规范原文；每个
  失败测试组做最小变更；不新增依赖；不修改 `solution/`；改动未授权
  文件前先询问。
- **何时停止：** 检查点命令通过、且学习者能说清什么失败了、为什么。
- **`verify.py`：** `python verify.py starter --expect-failure` 复现列出的
  失败；`python verify.py solution` 通过全部测试。
- **诚实规则：** 本课程构建的是协议的服务端；不认证任何特定客户端的
  合规性。说明哪些没验证过。

## 本课程不涉及的内容

纯 JSON-RPC 字典之外的传输层（stdio/HTTP 接线）、部署、客户端配置。
仓库的 MCP 迁移指南覆盖把既有服务迁移到 2026-07-28 规范。


## 徽章契约

- 徽章：**MCP 工具服务徽章**（徽章 id `course-mcp-tools`）——认领全部五个检查点后获得。
- 挑战：L01–L05 检查点各 10 分；五项全部在 flypython.com 认领后另加 50 分课程徽章奖励。
- 证据：`python verify.py` —— L03（校验与错误隔离）与 L04（多轮交互）由测试套件客观判定；L01/L02/L05 为学习者自报。
- 提交：每个通过的检查点会打印确定性认领码，在 flypython.com 上记入你的账号。这是自我报告的证据，绝不是证书。

## 文件夹结构


`COURSE.md`/`COURSE_cn.md`、双语 `lessons/`、`scenario/requests/`
线路样本、`TASK.md`/`TASK_cn.md`（完整服务契约）、`starter/`、
`solution/`、`tests/`、`verify.py`、`REVIEW.md`。

## 证据与许可

`REVIEW.md` 记录试跑状态。代码 MIT；文字 CC BY 4.0（见仓库 `LICENSE`）。
教学偏差请走 `course-feedback` issue 表单。
