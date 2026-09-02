---
id: write-llm-evals
type: playbook
title: 为大模型与 Agent 编写确定性评测
summary: 结合黄金测试集与 Schema 断言，为 Prompt 调整与工具调用 Agent 构建防劣化回归测试套件。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# 为大模型与 Agent 编写确定性评测

1. 沉淀带版本管理的真实用户输入黄金测试集（Golden Dataset），覆盖标准流程、对抗性输入、歧义用例及已知历史 Bug。
2. 在引入大模型语义评分前，优先建立确定性边界断言：校验 JSON Schema 契约合法性、必填字段完整性及禁用敏感词。
3. 针对工具调用入参进行严格类型断言；验证模型选择的工具与参数完全符合预定义的工具契约，杜绝幻觉参数。
4. 将轻量本地单元测试与在线模型评测解耦。在快速 CI 中使用录制的 Mock 响应，在线评测采用定时批处理运行。
5. 在变更 Prompt 或迁移模型前后，记录评测通过率、Token 消耗及延迟基线。严禁在没有指标对比证据的情况下直接发布 Prompt 变更。
6. 固定测试时的 temperature 与随机种子，设置可量化的容差阈值，防止偶发波动干扰回归结论。
