---
id: course-deepseek-harness-l02
type: course
title: "第 2 课：写任务契约，让 cordis.yml 承载配置"
summary: "把「改好一点」变成有边界、可测试的契约——再把工作规则放进组装出来的 Agent 里，而不是会被遗忘的提示词。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-13
hints:
  - title: "本检查点考察什么"
    body: "你能把 `TASK.md` 当成可测试的陈述来读，而不是散文。每个以函数名开头的句子都是套件能断言的契约行。"
  - title: "组装就是指令链"
    body: "Harness 的 Agent 在 `cordis.yml` 里组装：用哪个模型插件、哪些工具插件、什么系统指令、会话存到哪。想让每次运行都遵守的规则要写进组装里——不要每个会话重打一遍。"
  - title: "可测试性检查"
    body: "判断一句话能不能测：测试套件不看你的心思能不能断言它？数字、退出码、磁盘上的文件——不看感觉。"
---

# 第 2 课：写任务契约，让 cordis.yml 承载配置

## 目标

你能把 `TASK.md` 当成一组可测试陈述来读，把每条陈述追查到
`tests/test_report_tool.py` 里的一个测试，并把工作规则做成组装
Agent 的一部分，而不是每次都要重打的提示词。

## 为什么有这节课

含糊的需求产出含糊的代码。「把坏行处理好一点」是许可 Agent 去猜；
「无效行收进 `errors`、带下标和原因，有效行照常产出报告」是给它
目标、也给你检查的方法。用组装式 Agent 还有第二种失败：你在某个
会话里敲的规则下一个会话没有——除非它们活在组装配置里。

## 本课内容

打开 `TASK.md`。注意每行的共同点：它描述的是可观察的行为，不是
实现。契约里的四句陈述，以及钉住它们的测试：

| 契约行 | 测试 |
| --- | --- |
| 「JSON 文件要加载成与 CSV 相同的记录列表」 | `test_load_json_records_returns_list_of_dicts` |
| 「无效行带下标和原因进 `errors`；有效行照常聚合」 | `test_invalid_records_are_isolated_with_reasons` |
| 「分组总计保留两位小数」 | `test_group_totals_are_rounded_to_two_decimals` |
| 「报告写出是原子的，且会创建缺失的父目录」 | `test_write_report_creates_missing_parent_directories` |

再看持久的另一半。在 DeepSeek Harness 里，Agent 声明在
`cordis.yml` 中：模型插件、可用工具插件、轨迹落盘的会话存储、
以及它启动时带上的指令。把本课程的工作规则放到重启后仍在的地方
——例如 Agent 的配置指令里：

```
- 只改 starter/report_tool.py。tests/、solution/、scenario/ 只读。
- 每步只修一组失败测试；修完跑 `python verify.py starter`。
- 只用标准库——不加新依赖。
```

开一个*新*会话，让 Agent 陈述它的工作规则。它把你的规则原样引
回来，说明组装配置带上了；没有就检查指令是否真的写进了会话加载
的那份配置。

## 练习

为你真正拥有的一个脚本写一条契约行，用同样的形状：输入、输出、
错误情况、以及「完成 = `<命令>` 退出码为 0」。再写你会放进那个
项目 Agent 组装配置里的两条规则。

## 检查点

运行 `python verify.py progress`——能回答下面三题时，本检查点的
认领码就会显示：

1. 用你自己的话说，`test_invalid_records_are_isolated_with_reasons`
   钉住的是 `TASK.md` 哪一行？
2. 跨会话携带规则的是提示词还是 `cordis.yml` 组装配置？
3. 为什么只增轨迹让组装式 Agent 比聊天转录更好审计？

## 预期证据

你起草的契约行、两条规则，以及新会话对自己工作规则的陈述。
