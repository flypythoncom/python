# Playbook

Playbook 把反复出现的 Python 工作变成可审查步骤，并明确什么才算完成。

| 任务 | 什么时候使用 | 完成证据 |
| --- | --- | --- |
| [用回归测试修复 Bug](fix-a-bug/README_cn.md) | 行为错误或发生回归 | 修改前稳定复现失败，修改后通过 |
| [增加或修改 API](add-an-api/README_cn.md) | HTTP 或 Python 公共契约发生变化 | 契约、错误、测试和兼容性得到验证 |
| [接入外部 API](integrate-an-external-api/README_cn.md) | Python 调用第三方服务或模型 | 超时、失败、凭据和测试替身均已覆盖 |
| [升级依赖](upgrade-dependencies/README_cn.md) | 需要更新运行时或包 | 锁文件、测试、安全公告和运行检查通过 |
| [发布版本](ship-a-release/README_cn.md) | 包或服务准备交付 | 产物、变更日志、部署和回退得到验证 |

[English index](README.md)
