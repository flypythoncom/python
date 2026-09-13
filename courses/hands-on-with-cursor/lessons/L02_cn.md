---
id: course-cursor-l02
type: course
title: "第 2 课：写任务契约，让 .cursor/rules 承载规则"
summary: "把「改好一点」变成有边界、可测试的契约——再让它持久化，让每个 Cursor 会话都从同一套规则开始。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-13
hints:
  - title: "本检查点考察什么"
    body: "你能把 `TASK.md` 当成可测试的陈述来读，而不是散文。每个以函数名开头的句子都是套件能断言的契约行。"
  - title: "项目规则是指令链"
    body: "Cursor 干活前先读 `.cursor/rules/*.mdc`。front matter 决定规则何时生效：`description` 让 Agent 按需取用，`globs` 匹配到文件时生效，`alwaysApply: true` 永远生效。AGENTS.md 也会被读取。"
  - title: "可测试性检查"
    body: "判断一句话能不能测：测试套件不看你的心思能不能断言它？数字、退出码、磁盘上的文件——不看感觉。"
---

# 第 2 课：写任务契约，让 .cursor/rules 承载规则

## 目标

你能把 `TASK.md` 当成一组可测试陈述来读，把每条陈述追查到
`tests/test_report_tool.py` 里的一个测试，并写出 Cursor 会话会
自动读取的持久规则。

## 为什么有这节课

含糊的需求产出含糊的代码。「把坏行处理好一点」是许可 Agent 去猜；
「无效行收进 `errors`、带下标和原因，有效行照常产出报告」是给它
目标、也给你检查的方法。在 Cursor 里还有第二种失败：你在某个
对话里敲的规则，下一个对话里根本不存在。契约固定任务本身；
项目规则固定工作规则。

## 本课内容

打开 `TASK.md`。注意每行的共同点：它描述的是可观察的行为，不是
实现。契约里的四句陈述，以及钉住它们的测试：

| 契约行 | 测试 |
| --- | --- |
| 「JSON 文件要加载成与 CSV 相同的记录列表」 | `test_load_json_records_returns_list_of_dicts` |
| 「无效行带下标和原因进 `errors`；有效行照常聚合」 | `test_invalid_records_are_isolated_with_reasons` |
| 「分组总计保留两位小数」 | `test_group_totals_are_rounded_to_two_decimals` |
| 「报告写出是原子的，且会创建缺失的父目录」 | `test_write_report_creates_missing_parent_directories` |

再看持久的另一半。Cursor 从 `.cursor/rules/` 读项目规则——每条
规则是一个 `.mdc` 文件，front matter 控制它何时生效：
`alwaysApply: true` 附加到每次请求，`globs` 在匹配文件出现时
生效，`description` 让 Agent 在相关时自行取用。本课程的工作规则
应该放一条常驻规则。告诉 Agent：

**“创建 `.cursor/rules/flypython-course.mdc`，`alwaysApply: true`，
写入这些工作规则：只许改 starter/report_tool.py；tests/、solution/、
scenario/ 只读；每轮只修一组失败测试；修完跑
`python verify.py starter`；只用标准库。”**

然后开一个*新*对话，让它总结自己的工作规则。它把你的规则原样引
回来，说明规则生效了；没有就检查 front matter——`alwaysApply`
写错或漏写是最常见的原因。

## 练习

为你真正拥有的一个脚本写一条契约行，用同样的形状：输入、输出、
错误情况、以及「完成 = `<命令>` 退出码为 0」。再写你会放进那个
项目 `.cursor/rules/` 的两条规则，并决定各自用哪个 front matter
字段控制生效时机。

## 检查点

运行 `python verify.py progress`——能回答下面三题时，本检查点的
认领码就会显示：

1. 用你自己的话说，`test_invalid_records_are_isolated_with_reasons`
   钉住的是 `TASK.md` 哪一行？
2. 跨会话携带规则的是对话提示词还是 `.cursor/rules`？
3. 带 `globs` 的规则和带 `alwaysApply: true` 的规则有什么区别？

## 预期证据

你起草的契约行、两条带 front matter 选择的规则，以及新对话对
自己工作规则的总结。
