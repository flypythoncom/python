---
id: ai-coding-context-budget
type: guide
title: Coding Agent 上下文预算与精准任务设计
summary: 通过控制上下文体积、编写明确任务契约与建立自动化验证闭环，最大化 Agent 编码准确率。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Coding Agent 上下文预算与精准任务设计

直接向 Coding Agent 丢入整个仓库代码会带来大量噪声，稀释注意力并增加模型幻觉。
高效的 AI Coding 依赖于严格的上下文预算与边界明确的任务契约。

## 1. 上下文窗口是注意力预算

避免一次性将数十个无关文件塞入 Agent 提示词。仅提供：
1. 待修改的目标代码文件；
2. 直接调用方/被调用方的公共接口签名；
3. 定义预期行为的自动化测试用例。

## 2. 将需求表达为机器可验证的契约

诸如“优化这段 API”之类的模糊自然语言会导致 Agent 进行不可控的重构。应当明确指定：
- 输入类型与输出结构；
- 允许的依赖范围与标准库约束；
- 必须覆盖的边界异常与错误码；
- 最终判断完成的验证命令。

## 3. 利用本地工具建立亚秒级反馈闭环

确保 Agent 能借助现代工具链（如 [uv documentation](https://docs.astral.sh/uv/) 与
[pytest documentation](https://docs.pytest.org/en/stable/)）在本地快速执行测试。
极速的反馈闭环能够让 Agent 在人工审查前自主修复语法与逻辑缺陷。

## 4. 严格审查 Git Diff 的副作用

在合并前始终审查代码差异，确保 Agent 没有意外删除重要注释、引入未经审查的依赖或改动全局共享状态。
