---
id: course-claude-code-l02
type: course
title: "第 2 课：动手之前先写任务契约"
summary: 把"优化一下"变成有边界、可测试的契约——这是与编码 Agent 协作杠杆最大的一项技能。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "考你能不能把 `TASK.md` 读成可测试的语句而不是散文。每个以函数名开头的句子都是套件能断言的契约行。"
  - title: "把一行契约对到一个测试"
    body: "挑一行契约——比如 `total = valid + invalid must hold`——在 `tests/test_report_tool.py` 里找到断言它的测试。然后为你自己的一个脚本写一行契约：输入、输出、错误路径，以及『完成 = 某命令退出 0』。"
  - title: "可测试性检查"
    body: "判断一句话是否可测试：套件能否不读你的心思就断言它？看数字、退出码、磁盘上的文件——不看感觉。"
---

# 第 2 课：动手之前先写任务契约

## 目标

你能把 `TASK.md` 读成一组可测试的陈述，把每条陈述对应到
`tests/test_report_tool.py` 中的测试，并用仓库的任务契约模板为自己的
项目写出一条契约。

## 为什么要有这一课

模糊的需求产出模糊的代码。"把坏数据处理得稳一点"是在允许 Agent 猜；
"无效行收集进 `errors`，带 index 和 reason，有效行照常出报告"既给了
它目标，也给了你验收方式。契约是你决定"完成"含义的地方——要在 Agent
用一次看似合理的重写消耗掉你的信任之前决定。

## 课程内容

打开 `TASK.md`。注意每一行的共同点：它描述可观察的行为，而不是实现
方式。契约中的四条陈述及其锚定测试：

| 契约陈述 | 锚定测试 |
| --- | --- |
| JSON 数据文件按对象列表加载 | `test_load_json_records_returns_list_of_dicts` |
| 不支持的扩展名抛出 `ValueError` | `test_unsupported_suffix_raises_value_error` |
| 无效行以 `{"index", "reason"}` 隔离；有效行照常汇总 | `test_invalid_records_are_isolated_with_reasons` |
| 分组总计保留两位小数 | `test_group_totals_are_rounded_to_two_decimals` |

再注意边界条款——说明变更"不可以"做什么的行：不新增依赖、只改
`starter/report_tool.py`、只用标准库。边界条款的作用，是防止 Agent
出于"帮忙"的重写吞掉你的整个文件。

完整模板在配套仓库（`templates/TASK_CONTRACT.md`）。字段包括：用户
结果、当前行为、期望行为、输入输出、允许触碰的文件、明确不做的事、
失败与恢复、验收命令、权限（网络/提交/推送）。你留空的每个字段，都是
你交给机器替你做的决定。

## 练习

下一个契约由你自己来写，小而真实：

1. 选一个你真正拥有的脚本（报表、爬虫、同步任务）。
2. 按上面的表格形式为它写三条契约陈述——写行为，不写实现。
3. 为每条陈述写出锚定它的测试名。
4. 加一条边界条款（Agent 不可触碰的文件，或不可新增的依赖）。

让 Agent 参照 `TASK.md` 点评你的契约——它应该找出歧义，而不是加功能。

## 检查点

把你的四行内容给 Agent 看，问："这几条里哪一条你能靠作弊满足——测试
过了但行为没做到？"如果你们都找不到作弊路径，契约就足够具体。修掉
任何没通过这一关的行。

## 预期证据

你的契约（4 行）和作弊评审结果。第 3 课中 Agent 只按课程的 `TASK.md`
编码——你自己的契约在第 5 课投入使用。
