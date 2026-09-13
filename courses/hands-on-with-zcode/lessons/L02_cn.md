---
id: course-zcode-l02
type: course
title: "第 2 课：写任务契约，让 Goal 模式承载计划"
summary: "把「改好一点」变成有边界、可测试的契约——再让 Goal 模式把它拆成你能看着逐一落地的任务。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-13
hints:
  - title: "本检查点考察什么"
    body: "你能把 `TASK.md` 当成可测试的陈述来读，而不是散文。每个以函数名开头的句子都是套件能断言的契约行。"
  - title: "Goal 模式是目标管理器"
    body: "ZCode 的 Goal 模式把目标拆成 Agent 逐项执行的任务列表，并在某步卡住时管理恢复。它拆的是你写的契约——含糊进去，含糊出来。"
  - title: "可测试性检查"
    body: "判断一句话能不能测：测试套件不看你的心思能不能断言它？数字、退出码、磁盘上的文件——不看感觉。"
---

# 第 2 课：写任务契约，让 Goal 模式承载计划

## 目标

你能把 `TASK.md` 当成一组可测试陈述来读，把每条陈述追查到
`tests/test_report_tool.py` 里的一个测试，并在任何文件被碰之前，
看着一个目标被拆成任务列表。

## 为什么有这节课

含糊的需求产出含糊的代码。「把坏行处理好一点」是许可 Agent 去猜；
「无效行收进 `errors`、带下标和原因，有效行照常产出报告」是给它
目标、也给你检查的方法。在 ZCode 里，拆解是一等公民：Goal 模式
把你的目标变成任务列表，并在某步卡住时管理恢复。它拆的是你写的
契约——精确的契约变成精确的任务列表。

## 本课内容

打开 `TASK.md`。注意每行的共同点：它描述的是可观察的行为，不是
实现。契约里的四句陈述，以及钉住它们的测试：

| 契约行 | 测试 |
| --- | --- |
| 「JSON 文件要加载成与 CSV 相同的记录列表」 | `test_load_json_records_returns_list_of_dicts` |
| 「无效行带下标和原因进 `errors`；有效行照常聚合」 | `test_invalid_records_are_isolated_with_reasons` |
| 「分组总计保留两位小数」 | `test_group_totals_are_rounded_to_two_decimals` |
| 「报告写出是原子的，且会创建缺失的父目录」 | `test_write_report_creates_missing_parent_directories` |

现在定目标。给 Agent 一个已经按契约拆好的目标：

**“目标：让 starter/report_tool.py 满足 TASK.md。一次只修一组
失败测试——先 JSON 加载，再无效行隔离，再舍入，再原子写，最后
是端到端测试——每个任务后跑 `python verify.py starter`。只许改
starter/report_tool.py；tests/、solution/、scenario/ 只读；只用
标准库。”**

放行执行之前，先读 Goal 模式产出的任务列表。每个任务都应点名
一条契约行和一个验证步骤——哪个任务写的是「改进错误处理」，就
收紧目标；那不是契约行。任务列表就是本课的交付物：它是你的契约
的可执行形态。

## 练习

为你真正拥有的一个脚本写一条契约行，用同样的形状：输入、输出、
错误情况、以及「完成 = `<命令>` 退出码为 0」。再写你会给 ZCode
的目标陈述——带上本课用过的同样边界。

## 检查点

运行 `python verify.py progress`——能回答下面三题时，本检查点的
认领码就会显示：

1. 用你自己的话说，`test_invalid_records_are_isolated_with_reasons`
   钉住的是 `TASK.md` 哪一行？
2. Goal 模式拿你的目标做什么——某步卡住时它又做什么？
3. 为什么边界要写进目标陈述，而不只写进任务？

## 预期证据

你起草的契约行、你的目标陈述、它产出的任务列表（或你收紧过的
版本及理由）。
