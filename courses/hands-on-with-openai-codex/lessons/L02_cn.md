---
id: course-codex-cli-l02
type: course
title: "第 2 课：写任务契约，让 AGENTS.md 承载规则"
summary: "把「改好一点」变成有边界、可测试的契约——再让它持久化，让每个 Codex 线程都从同一套规则开始。"
lang: zh-CN
content_version: 2
status: reviewed
reviewed_on: 2026-09-13
hints:
  - title: "本检查点考察什么"
    body: "你能把 `TASK.md` 当成可测试的陈述来读，而不是散文。每个以函数名开头的句子都是套件能断言的契约行。"
  - title: "AGENTS.md 是指令链"
    body: "Codex 干活前先读 AGENTS.md：~/.codex 里的全局文件，加上从仓库根到当前目录的项目文件。想让每个线程都遵守的规则放那里——不要在每个提示里重打。"
  - title: "可测试性检查"
    body: "判断一句话能不能测：测试套件不看你的心思能不能断言它？数字、退出码、磁盘上的文件——不看感觉。"
---

# 第 2 课：写任务契约，让 AGENTS.md 承载规则

## 目标

你能把 `TASK.md` 当成一组可测试陈述来读，把每条陈述追查到
`tests/test_report_tool.py` 里的一个测试，并写出 Codex 线程会自动
读取的持久规则。

## 为什么有这节课

含糊的需求产出含糊的代码。「把坏行处理好一点」是许可 Agent 去猜；
「无效行收进 `errors`、带下标和原因，有效行照常产出报告」是给它
目标、也给你检查的方法。在 Codex 应用里还有第二种失败：你在某个
线程里敲的规则，下一个线程里根本不存在。契约固定任务本身；
`AGENTS.md` 固定工作规则。

## 本课内容

打开 `TASK.md`。注意每行的共同点：它描述的是可观察的行为，不是
实现。契约里的四句陈述，以及钉住它们的测试：

| 契约行 | 测试 |
| --- | --- |
| 「JSON 文件要加载成与 CSV 相同的记录列表」 | `test_load_json_records_returns_list_of_dicts` |
| 「无效行带下标和原因进 `errors`；有效行照常聚合」 | `test_invalid_records_are_isolated_with_reasons` |
| 「分组总计保留两位小数」 | `test_group_totals_are_rounded_to_two_decimals` |
| 「报告写出是原子的，且会创建缺失的父目录」 | `test_write_report_creates_missing_parent_directories` |

再看持久的另一半。Codex 做任何工作之前都会先读 `AGENTS.md`——
`~/.codex` 里的全局文件，然后从仓库根一路向下读项目文件；越靠近
当前目录的文件优先级越高。本课程的工作规则正是该放那里的东西。
开一个草稿文件，为本项目起草三条规则，例如：

```
- 只改 starter/report_tool.py。tests/、solution/、scenario/ 只读。
- 每轮只修一个失败测试组；修完跑 `python verify.py starter`。
- 只用标准库——不加新依赖。
```

告诉线程：**“这些是我给项目定的规则——把它们写到文件夹根的
AGENTS.md 里，让每个新线程开工就带上。”** 然后开一个*新*线程，让它
总结自己的工作规则。它把你的三行原样引回来，说明指令链通了；没有
就检查文件落在哪一层。

## 练习

为你真正拥有的一个脚本写一条契约行，用同样的形状：输入、输出、
错误情况、以及「完成 = `<命令>` 退出码为 0」。再写你会放进那个
项目 AGENTS.md 的两条规则。

## 检查点

运行 `python verify.py`——能回答下面三题时，本检查点的
认领码就会显示：

1. 用你自己的话说，`test_invalid_records_are_isolated_with_reasons`
   钉住的是 `TASK.md` 哪一行？
2. 跨线程携带规则的是提示词还是 AGENTS.md？
3. 全局 `~/.codex/AGENTS.md` 相对项目文件的优先级顺序是什么？

## 预期证据

你起草的契约行、两条规则，以及新线程对自己工作规则的总结。
