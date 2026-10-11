---
id: course-github-copilot-l02
type: course
title: "第 2 课：写任务契约，让 .github 指令文件承载规则"
summary: "把「改好一点」变成有边界、可测试的契约——再用 `.github/copilot-instructions.md` 和带 `applyTo` 的指令文件把它持久化，让每个 Copilot 会话都从同一套规则开始。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
hints:
  - title: "本检查点考察什么"
    body: "你能把 `TASK.md` 当成可测试的陈述来读，而不是散文。每个以函数名开头的句子都是套件能断言的契约行。"
  - title: "两类指令文件"
    body: "`.github/copilot-instructions.md`（或 `AGENTS.md`）对整个工作区常驻生效。`.github/instructions/*.instructions.md` 在 Agent 创建或修改的文件匹配其 `applyTo` glob 时附加，或在 `description` 与任务相符时按需加载。"
  - title: "可测试性检查"
    body: "判断一句话能不能测：测试套件不看你的心思能不能断言它？数字、退出码、磁盘上的文件——不看感觉。"
---

# 第 2 课：写任务契约，让 .github 指令文件承载规则

## 目标

你能把 `TASK.md` 当成一组可测试陈述来读，把每条陈述追查到
`tests/test_report_tool.py` 里的一个测试，写出 Copilot 会话会自动读取的
持久指令——并能从回复的 References 里证明它们确实被用上了。

## 为什么有这节课

含糊的需求产出含糊的代码。「把坏行处理好一点」是许可 Agent 去猜；
「无效行收进 `errors`、带下标和原因，有效行照常产出报告」是给它
目标、也给你检查的方法。在 Copilot 里还有第二种失败：你在某个
对话里敲的规则，下一个对话里根本不存在。契约固定任务本身；
指令文件固定工作规则。

## 本课内容

打开 `TASK.md`。注意每行的共同点：它描述的是可观察的行为，不是
实现。契约里的四句陈述，以及钉住它们的测试：

| 契约行 | 测试 |
| --- | --- |
| 「JSON 文件要加载成与 CSV 相同的记录列表」 | `test_load_json_records_returns_list_of_dicts` |
| 「无效行带下标和原因进 `errors`；有效行照常聚合」 | `test_invalid_records_are_isolated_with_reasons` |
| 「分组总计保留两位小数」 | `test_group_totals_are_rounded_to_two_decimals` |
| 「报告写出是原子的，且会创建缺失的父目录」 | `test_write_report_creates_missing_parent_directories` |

再看持久的另一半。Copilot 会话读取两类指令文件：

- **常驻：** 工作区根下的 `.github/copilot-instructions.md`（或
  `AGENTS.md`，Copilot 同样会读）。工作区里的每次请求都带上它。
- **定向：** 带 YAML front matter 的
  `.github/instructions/<name>.instructions.md`。`applyTo` 是相对工作区
  根的 glob；Agent 创建或修改匹配的文件时，VS Code 附加这个文件。
  `description` 让 Agent 在任务相符时按需加载。

本课程的工作规则只在改动课程文件夹时才有意义，所以应该放定向文件。
告诉 Agent：

**“创建 `.github/instructions/flypython-course.instructions.md`，front
matter 写 `name: FlyPython course rules`、一行 `description`、
`applyTo: 'courses/hands-on-with-github-copilot/**'`，写入这些工作规则：
只许改 starter/report_tool.py；tests/、solution/、scenario/ 只读；每轮
只修一组失败测试；修完跑 `python verify.py starter`；只用标准库。”**

在批准任何其他操作之前先读它创建的文件——`applyTo` glob 是最常写错
的地方。

然后开一个*新*对话会话，让它改 `starter/report_tool.py` 里的一个
docstring，并总结它正在遵守的规则。展开回复里的 **References**：指令
文件应该在列表里。不在的话，先打开 Agent Customizations 编辑器确认文件
被发现，再检查 `applyTo` 是否匹配 Agent 编辑的路径。继续之前撤销那个
docstring 改动（第 3 课讲怎么撤）。

## 练习

为你真正拥有的一个脚本写一条契约行，用同样的形状：输入、输出、
错误情况、以及「完成 = `<命令>` 退出码为 0」。再为那个项目写两条
规则，并决定哪条放 `.github/copilot-instructions.md`、哪条放带
`applyTo` 的文件。

## 检查点

能回答下面三题时，用 `python verify.py --attest l02` 认领本检查点：

1. 用你自己的话说，`test_invalid_records_are_isolated_with_reasons`
   钉住的是 `TASK.md` 哪一行？
2. 跨会话携带规则的是对话提示词还是指令文件？
3. 带 `applyTo` 的指令文件什么时候被附加？你是怎么确认自己那个被
   附加了的？

## 预期证据

你起草的契约行、两条规则及其文件选择，以及新会话里显示该指令文件的
References 列表。
