---
id: course-llm-features-l02
type: course
title: "第 2 课：把模型输出写成契约"
summary: "提示词负责请求，契约负责检查。把 TASK.md 当成你的代码与模型之间的边界来读——回复必须长什么样、能运行哪些工具、不照做时怎么办。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
hints:
  - title: "本检查点考察什么"
    body: "你能把 `TASK.md` 当成可测试陈述来读、把每条追查到一个测试——并说清为什么 `build_messages` 里的格式要求单靠它自己不够。"
  - title: "提示词是请求，不是保证"
    body: "`build_messages` 把确切格式告诉了模型。模型通常会照做。「通常」正是 `parse_triage` 存在的原因。"
  - title: "工具调用就是模型在决定你的代码运行什么"
    body: "工具注册表是白名单，参数是不可信输入——和你对待网页表单的规则一样。"
---

# 第 2 课：把模型输出写成契约

## 目标

你能把 `TASK.md` 当成一组关于模型回复的可测试陈述来读，把每条陈述追查到
`tests/test_ticket_triage.py` 里的一个测试，并解释契约替你做的三个决定：
什么是合法回复、哪些工具调用可以运行、模型不照做时怎么办。

## 为什么有这节课

打开 starter 里的 `build_messages`。它已经把确切的 JSON 字段、允许的分类、
优先级范围、怎样调用工具都告诉了模型。很多团队到此为止——提示词说了我们
要什么，回复就会是我们要的。提示词是请求。契约是请求被忽略时你的代码
强制执行的东西，而测试是你确认它真的强制执行了的方法。

厂商 API 往往提供 JSON 或受 schema 约束的输出模式。用上它能减少格式错误
的回复；但它不会告诉你分类对不对、工具参数能不能放心执行、评测是否诚实。
本课程的契约照样适用。

## 本课内容

把测试并排打开，读 `TASK.md`。契约做了三个决定：

**1. 什么是合法回复。** 恰好四个字段，每个都有类型和范围。其他一律拒绝，
错误信息点名字段。

| 契约行 | 测试 |
| --- | --- |
| 「去掉……外面包着的一层 Markdown 代码围栏」 | `test_parse_strips_a_markdown_fence` |
| 「`category` 属于 *categories*」 | `test_parse_rejects_an_unknown_category_naming_the_field` |
| 「`priority` 是 1 到 4 的 `int`（`bool` 和 `float` 都拒绝）」 | `test_parse_rejects_bad_priorities` |
| 「缺字段或多字段都抛出点名该字段的 `TriageError`」 | `test_parse_rejects_missing_extra_and_mistyped_fields` |

为什么要点名字段？因为第 3 课会把错误信息回传给模型。「回复无效」没给它
任何可改的依据；「category must be one of billing, shipping, …; got 'login'」
准确告诉它该改哪里。

**2. 哪些工具调用可以运行。** `tools` 字典就是白名单。未登记的名字在任何
东西运行之前就被拒绝；参数在调用函数之前就按声明的名字和类型检查。
`shop-support` 里那条录好的 `{"tool": "issue_refund", …}` 回复是要记住的
例子：一个能点名任意函数的模型，能让你的代码做那个函数能做的任何事。

**3. 失败时怎么办。** 带着错误信息重试一次，然后兜底：把工单交给人、不给
分类。兜底绝不猜——一个自信但错误的分类，比一句诚实的「需要人来看」更糟。

## 练习

从你熟悉的项目里拿一个模型调用——或者编一个——用同样的形状写出它的输出
契约：确切的字段及其类型和范围、它可以调用的工具及参数类型、失败策略
（重试几次、兜底返回什么）。然后给每句话打标：测试套件不看你的心思能
断言它吗？

## 检查点

能回答下面三题时，用 `python verify.py --attest l02` 认领本检查点：

1. `build_messages` 已经说明了格式。为什么 `parse_triage` 还要再检查？
2. 为什么被拒绝的工具调用绝不能到达工具函数——`issue_refund` 本来可能
   做什么？
3. 为什么兜底返回 `category: None`，而不是最可能的那个分类？

## 预期证据

你起草的输出契约，每句都标明可测或不可测。
