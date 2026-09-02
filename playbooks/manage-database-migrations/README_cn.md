---
id: manage-database-migrations
type: playbook
title: 管理数据库架构迁移
summary: 规划、执行并验证具备零停机兼容性与回滚安全性的可逆数据库迁移。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# 管理数据库架构迁移

1. 当引入非增量（破坏性）列或表变更时，必须将数据库架构迁移与应用代码部署解耦分步进行。
2. 遵循“扩展与收缩（Expand and Contract）”模式：先添加允许为空的新列或新表，实现双写，批量回填历史数据，最后废弃清理旧列。
3. 仔细审查 Alembic 自动生成的迁移脚本；逐行检查生成的 SQL 语句，排查破坏性操作（如直接 `DROP COLUMN`、长事务锁表或未索引外键约束）。
4. 在提交代码前，在本地干净的测试数据库上同时验证 `upgrade()` 升级与 `downgrade()` 回退逻辑。
5. 在迁移执行脚本中配置显式语句超时（Statement Timeout），防止在生产高并发环境下长时间阻塞表级读写。
6. 验证新旧两版应用代码在过渡期数据库结构下的共存表现，确保平滑滚动升级零停机。
