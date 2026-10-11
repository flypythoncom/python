---
id: course-llm-features-l01
type: course
title: "第 1 课：演示能跑不等于功能可靠"
summary: "通过 FlyPython Skill 取回课程，跑一遍 starter 的评测，抓住那个不可能为真的数字——再把每个失败测试对应到让它坏掉的真实回复。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
hints:
  - title: "本检查点考察什么"
    body: "先复现失败再动手：`python verify.py` 必须把 l03 和 l04 显示为 `[open]`，并且你能解释 starter 的评测输出错在哪。"
  - title: "评测那一行读两遍"
    body: "在 `it-helpdesk` 上 starter 打印 `accuracy=1.000 correct=5/6`。两个数不可能都对。找出哪个在撒谎、为什么。"
  - title: "完成的标志"
    body: "对某一个皮肤，你能说出每个失败测试代表哪条录好的回复。然后用 `python verify.py --attest l01` 认领本检查点。"
---

# 第 1 课：演示能跑不等于功能可靠

## 目标

课程文件已由你的 Agent 取回工作目录。你跑过 starter 的评测，找到了输出里
那个不可能为真的数字，并能说出每个失败测试代表哪一种真实的模型回复。
本课不改任何代码。

## 第 1 步——让 Agent 取回本课（你不下载）

在一个空工作目录里打开你的编码 Agent，粘贴这一句话：

> Read https://flypython.com/skills/flypython/SKILL.md and start the FlyPython course `llm-features-in-python`.

Agent 会给你一个授权链接和一组短码。打开链接、登录、核对码与 Agent
显示的一致后点「允许」，然后对 Agent 说「好了」。它把本课文件写到
`courses/llm-features-in-python/`。

**前提**：这些课程需要一个能执行命令**并且**能联网的编码 Agent。只能
聊天的网页 AI 做不了。练习本身不需要 API key，也不发任何网络请求。

## 为什么有这一课

几乎每个模型驱动功能的第一版都长得像这个 starter：发提示词、对回复
`json.loads`、直接用字段。演示时能跑，因为演示那条回复格式恰好规整。
进了产品，模型迟早会把 JSON 包进 Markdown 围栏、编一个分类、写
`"priority": "high"`、要调用一个你根本没写的工具，或者干脆用散文回答。
这些都是正常回复——处理它们的代码才是功能本身。

## 本课内容

让 Agent 先只读不动手：

**“读 COURSE.md——它是本文件夹的教学契约。再读 TASK.md 和
starter/ticket_triage.py。不要改任何文件。告诉我测试期望哪些行为、
starter 缺了哪些。”**

然后运行学员命令——整个课程你只需要这一条检查命令：

```bash
python verify.py
```

再在两个皮肤上跑 starter 的评测：

```bash
python starter/ticket_triage.py scenario/it-helpdesk
python starter/ticket_triage.py scenario/shop-support
```

读 `it-helpdesk` 输出的第一行：`accuracy=1.000 correct=5/6`。六个对五个
不是 100%。starter 的 `evaluate` 跳过每个崩掉的用例，再用剩下的做分母——
模型失败得越厉害，评测反而越好看。

套件里有十二个失败测试。按让它们坏掉的回复分组：

| 失败的测试 | 让 starter 坏掉的回复 |
| --- | --- |
| `test_parse_strips_a_markdown_fence` | ```` ```json { … } ``` ```` 而不是裸 JSON |
| `test_parse_rejects_an_unknown_category_naming_the_field`、`test_parse_rejects_bad_priorities`、`test_parse_rejects_missing_extra_and_mistyped_fields` | `"category": "login"`、`"priority": "high"`、多出来的 `"confidence"`、散文、JSON 列表——要么照单全收，要么崩溃 |
| `test_unregistered_tool_is_refused`、`test_tool_arguments_are_validated_before_the_call` | `{"tool": "issue_refund", …}` 或 `{"asset_tag": 301}`——由模型决定你的代码运行什么 |
| `test_invalid_reply_is_retried_with_the_error_fed_back`、`test_repeated_invalid_replies_fall_back_to_a_human`、`test_tool_call_budget_ends_in_the_fallback` | 一条坏回复直接终止请求，既不给第二次机会，也没有安全兜底；模型不停调用工具也没人拦 |
| `test_accuracy_divides_by_every_case_and_counts_fallbacks` | 评测悄悄丢掉崩溃的用例 |
| `test_shop_support_eval_is_reported_below_threshold`、`test_it_helpdesk_eval_passes_its_threshold` | 端到端：就是你刚读的那行评测输出 |

有三个测试已经通过——合法回复能解析、工具结果会回传给模型、缺参数时
打印用法。starter 不是全错；它恰好错在回复不再「客气」的地方。

维护者命令会精确打印失败测试名：

```bash
python verify.py starter --expect-failure
```

## 练习

挑一个你最有代入感的皮肤，把它的 `recordings.json` 和 `cases.json` 并排
打开，每个用例写一行：starter 对这条回复做了什么（接受、崩溃、还是判错），
以及它*应该*做什么。写完让 Agent 确认——不是让它修。

## 检查点

运行 `python verify.py`。不看材料能回答下面三题时，用
`python verify.py --attest l01` 认领本检查点：

1. starter 在 `it-helpdesk` 上为什么打印 `accuracy=1.000` 却又是
   `correct=5/6`？两个数里哪个是诚实的？
2. 说出两条会让 starter 崩溃的录好回复，以及一条它接受了但其实是错的。
3. 为什么包在 Markdown 围栏里的回复是正常回复，而不是可以忽略的模型
   bug？

## 预期证据

默认命令的输出、那两行评测输出，以及你对一个皮肤的逐用例笔记。第 4 课
会拿它们和修好后的评测对比。
