---
id: upgrade-python-dependencies
type: playbook
title: 升级 Python 依赖
summary: 在边界明确的修改中，用锁文件、兼容性、安全和运行证据完成依赖升级。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# 升级 Python 依赖

1. 定义包范围、升级原因、支持的 Python 版本和回退方式；
2. 先阅读上游发布说明与安全公告，识别破坏性或弃用行为，再修改锁文件；
3. 只更新目标直接依赖，并审查所有传递依赖变化；
4. 运行格式、类型、测试、构建和真实运行 smoke check；
5. 审查依赖来源、安装脚本、许可证、产物大小和新增权限；
6. 记录最终版本与用户影响，不把无关升级混入同一个修改。
