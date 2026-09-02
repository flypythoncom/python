# 任务 Playbook

Playbook 把反复出现的 Python 工程任务变成带明确完成标准的、可审查的步骤。

| 任务 | 适用场景 | 完成证据 |
| --- | --- | --- |
| [用回归测试修复 Bug](fix-a-bug/README_cn.md) | 线上行为错误或出现功能倒退 | 复现脚本在修复前失败，修复后通过 |
| [增加或修改 API](add-an-api/README_cn.md) | 公开 HTTP 接口或库契约发生变化 | 契约、错误码、测试用例和向后兼容性完成验证 |
| [集成外部 API](integrate-an-external-api/README_cn.md) | Python 调用第三方服务或模型接口 | 超时、网络故障、鉴权和测试桩全部覆盖 |
| [升级依赖](upgrade-dependencies/README_cn.md) | 运行环境或第三方依赖包需要更新 | 锁文件、单元测试、安全通告和冒烟测试全部通过 |
| [发布上线](ship-a-release/README_cn.md) | 构建产物或服务准备发布 | 产物构建、更新日志、部署和回退方案完成验证 |
| [编写确定性评测](write-llm-evals/README_cn.md) | 变更 LLM 提示词、替换模型或更新 Agent 工具 | 黄金测试集与结构化断言验证无性能/准确率倒退 |
| [搭建结构化日志](setup-structured-logging/README_cn.md) | 从本地脚本走向生产级服务 | JSON 格式、Trace ID 上下文贯穿与脱敏通过验证 |
| [管理数据库架构迁移](manage-database-migrations/README_cn.md) | 修改 SQL 数据库表结构或 ORM 模型 | 升级、回滚、数据回填与零停机平滑发布完成验证 |

[English index](README.md)
