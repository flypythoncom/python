---
id: course-kimi-code-l02
type: course
title: "第 2 课：写任务契约，在规划道里拆步"
summary: "把「改好一点」变成有边界、可测试的契约——再让 plan 子代理（无写无 shell）先把它拆成步骤，然后才许动文件。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-13
hints:
  - title: "本检查点考察什么"
    body: "你能把 `TASK.md` 当成可测试的陈述来读，而不是散文。每个以函数名开头的句子都是套件能断言的契约行。"
  - title: "plan 碰不了任何东西"
    body: "内置 `plan` 子代理只产出计划，没有 shell 和写工具——规划是一条独立的、无副作用的道。子代理也不能再生子代理，所以分道不会递归到你视野之外。"
  - title: "可测试性检查"
    body: "判断一句话能不能测：测试套件不看你的心思能不能断言它？数字、退出码、磁盘上的文件——不看感觉。"
---

# 第 2 课：写任务契约，在规划道里拆步

## 目标

你能把 `TASK.md` 当成一组可测试陈述来读，把每条陈述追查到
`tests/test_report_tool.py` 里的一个测试，并在任何文件被碰之前，
用规划道把契约拆成步骤。

## 为什么有这节课

含糊的需求产出含糊的代码。「把坏行处理好一点」是许可 Agent 去猜；
「无效行收进 `errors`、带下标和原因，有效行照常产出报告」是给它
目标、也给你检查的方法。Kimi Code 的内置分道把纪律变成字面事实：
`plan` 能思考工作但手里没有写和 shell 工具，规划不可能失手变成
改代码。子代理不能再生子代理，工作也不会递归出你的视野。

## 本课内容

打开 `TASK.md`。注意每行的共同点：它描述的是可观察的行为，不是
实现。契约里的四句陈述，以及钉住它们的测试：

| 契约行 | 测试 |
| --- | --- |
| 「JSON 文件要加载成与 CSV 相同的记录列表」 | `test_load_json_records_returns_list_of_dicts` |
| 「无效行带下标和原因进 `errors`；有效行照常聚合」 | `test_invalid_records_are_isolated_with_reasons` |
| 「分组总计保留两位小数」 | `test_group_totals_are_rounded_to_two_decimals` |
| 「报告写出是原子的，且会创建缺失的父目录」 | `test_write_report_creates_missing_parent_directories` |

现在让规划道干活。告诉 `kimi`：

**“用 plan 子代理把 TASK.md 拆成 starter/report_tool.py 的有序
实现计划：每组失败测试一步，每步以 `python verify.py starter`
收尾。现在不要改任何东西。”**

读它返回的计划。它应该点名你刚追查到测试的四个行为组，且顺序
上每一步都可独立验证。如果某步是「改进错误处理」，打回去——
那不是契约行。一份能逐行对着 `TASK.md` 核对的计划，就是本课的
交付物。

再注意什么在跨会话携带规则：仓库根若有 `AGENTS.md`，Kimi Code
会读它——持久的工作规则活在文件里，不活在你会关掉的对话里。

## 练习

为你真正拥有的一个脚本写一条契约行，用同样的形状：输入、输出、
错误情况、以及「完成 = `<命令>` 退出码为 0」。再草拟 `plan` 道
应该为它返回的两步计划。

## 检查点

运行 `python verify.py progress`——能回答下面三题时，本检查点的
认领码就会显示：

1. 用你自己的话说，`test_invalid_records_are_isolated_with_reasons`
   钉住的是 `TASK.md` 哪一行？
2. `plan` 没有写和 shell 工具为什么重要？
3. 为什么「子代理不能再生子代理」让审查更容易？

## 预期证据

你起草的契约行，和你接受的（或打回去并说明理由的）那份有序计划。
