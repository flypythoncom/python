---
id: ship-a-python-release
type: playbook
title: 发布 Python 版本
summary: 交付可追踪的包或服务版本，并验证真实线上行为与回退路径。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# 发布 Python 版本

1. 选择准确 commit，并从该版本确认测试、版本号、变更日志、迁移、配置和兼容性；
2. 在干净环境一次性构建产物，并检查产物内容；
3. 用最小权限凭据发布或部署，记录产物摘要、部署标识和配置版本；
4. 验证安装过程或线上真实用户路径，而不是只相信命令成功；
5. 检查健康状态、日志、数据变化和关键集成；
6. 验收失败就停止发布并按文档回退，只有可访问的目标产物验证通过后才宣布可用。
