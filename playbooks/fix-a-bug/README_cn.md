---
id: fix-a-python-bug
type: playbook
title: 用回归测试修复 Python Bug
summary: 复现行为、缩小原因、完成最小修复，并证明回归问题不会再次出现。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# 用回归测试修复 Python Bug

1. 在[任务契约](../../templates/TASK_CONTRACT_cn.md)中记录实际行为、预期行为、最小失败输入
   和受影响的用户路径；
2. 先增加一个能因所报告问题而失败的测试；如果修改前没有失败，它还不能构成回归证据；
3. 让 coding agent 检查调用路径并提出范围最小的可能原因，不授权无关重构；
4. 只修改契约要求的行为，除非契约明确变更，否则保持公共错误形式稳定；
5. 依次运行新测试、最近的测试套件、完整确定性测试；
6. 审查 diff 是否扩大范围、隐藏异常、新增网络或文件副作用、遗漏边界情况；
7. 重跑原始用户路径，并在[验证记录](../../templates/VERIFICATION_cn.md)中写下命令与结果。

可以用 [product slug 示例](../../examples/product-slug/README_cn.md)完成一次完整练习。
