---
id: path-foundation-challenge
type: path
title: "路线挑战：双 Agent、双重验证"
summary: 基础路线收官挑战——同一任务分别用 Claude Code 与 Codex CLI 完成并亲手双重验证。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# 路线挑战：双 Agent、双重验证

**积分：** 200 · **类型：** 项目 · **证据：** 客观验证（`verify.py`）

基础路线的收官挑战：证明你能驱动**两个**不同的 Agent 完成同一项任务——
并且两个结果都由你亲手验证。

## 任务

选一个你真正在乎的小任务（建议：“一个统计文件行数、词数、字节数的
CLI”，或复用路线四门课程 `hands-on-python-with-claude-code`、
`hands-on-with-openai-codex-cli`、`agent-rules-single-source`、
`verifying-ai-generated-code` 的任意场景皮）。然后：

1. **第一轮 —— Claude Code。** 新建文件夹，写一个 `TASK.md` 描述契约
   （输入、输出、边界情况、完成 = 测试通过），让 Claude Code 实现它，
   并写一个 `verify.py` 式的检查，在结果上跑通。
2. **第二轮 —— Codex CLI。** 同一任务、新文件夹、同一份 `TASK.md`。
   用 Codex CLI 独立实现——不要抄第一轮的代码。
3. **双重验证。** 用你的客观检查对**两份**实现各跑一遍。记录差异：
   结构、边界处理、测试覆盖、任何让你意外的地方。

## 需要留下的记录

- 两个文件夹都保留原样（它们就是你的证据）。
- 一段简短笔记：哪个 Agent 的产出需要的修正更少，以及**你为什么这么
  判断**——这是把 `verifying-ai-generated-code` 一课的怀疑式审查用到跨工具对比上。

## 检查点

完成条件：

- 两份实现都在，且你的客观检查对每份都通过。
- 你的对比笔记至少写出一个有证据的具体差异（文件、测试或命令输出）。

本挑战的认领计入基础路线徽章——**「Agent 使用者」**的 200 分。
自我报告的证据，绝非证书。
