---
id: path-foundation-challenge
type: path
title: "路线挑战：双 Agent、双重验证"
summary: 基础路线收官——把同一个任务分别交给六个路线 Agent 中任选的两个，并亲手验证两份产出。
lang: zh-CN
content_version: 2
status: reviewed
reviewed_on: 2026-09-13
---

# 路线挑战：双 Agent、双重验证

**积分：** 200 · **类型：** 项目 · **证据：** 客观（`verify.py`）

基础路线的最后一关：证明你能驱动**两个不同**的 Agent 完成同一个任务——
并且亲手验证两份结果。

## 任务

挑一个你真正在乎的小任务（建议：「一个统计文件行数、词数、字节数的
CLI」，或复用路线课程里的任一场景皮肤：
`hands-on-python-with-claude-code`、`hands-on-with-openai-codex`、
`hands-on-with-cursor`、`hands-on-with-deepseek-harness`、
`hands-on-with-kimi-code`、`hands-on-with-zcode`、
`agent-rules-single-source`、`verifying-ai-generated-code`）。

从本路线教授的六个 Agent 工具中任选**两个**（Claude Code、Codex 应用、
Cursor、DeepSeek Harness、Kimi Code、ZCode），然后：

1. **第一轮——Agent A。** 在全新文件夹里写一份描述契约的 `TASK.md`
   （输入、输出、边界情况、完成 = 测试通过），驱动第一个 Agent 实现，
   并加一个 `verify.py` 式的检查能在结果上通过。
2. **第二轮——Agent B。** 同一个任务、新文件夹、同一份 `TASK.md`。
   驱动一个*不同*的 Agent 独立实现——不要抄第一轮的代码。
3. **双重验证。** 对**两份**实现都跑你的客观检查。记录差异：结构、
   边界情况处理、测试覆盖、任何让你意外的地方。

## 要记录什么

- 两个文件夹都原样保留（它们就是你的证据）。
- 一段短笔记：哪个 Agent 的产出需要的修正更少，以及*你为什么这么
  认为*——这是 `verifying-ai-generated-code` 课程里怀疑式评审习惯
  的跨工具应用。

## 检查点

满足以下条件即完成：

- 两份实现都存在，且你的客观检查在各自上通过。
- 你的对比笔记点名了至少一处有证据的具体差异（一个文件、一个测试、
  一段命令输出）。
- 两个 Agent 确实是不同的工具——不是同一个工具的两个会话。

本挑战的认领记入基础路线徽章——为 **Agent 使用者** 贡献 200 分。
自我报告的证据，从来不是证书。
