---
id: course-llm-features-l05
type: course
title: "第 5 课：接到你自己的模型功能上"
summary: "把真实模型放到同一个接缝后面：一个 client 可调用对象、一份输出契约、一张白名单、一个兜底，以及录一次、每次改动都回放的评测。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
hints:
  - title: "本检查点考察什么"
    body: "自我报告：你确认把这套模式用到了自己的一个模型调用上。证据是你的契约、你录下的用例和你的评测输出——不是我们查得了的码。"
  - title: "client 就是接缝"
    body: "本课程的一切只依赖 `client(messages) -> str`。真实的厂商调用能放进这个可调用对象后面；上次它说过的话的回放也能。"
  - title: "录音是数据"
    body: "从真实流量录下的回复可能含有客户数据。进 git 之前像对待任何数据集一样审查它们。"
---

# 第 5 课：接到你自己的模型功能上

## 目标

你把这套模式——输出契约、带校验的解析、工具白名单、重试与兜底、诚实的
离线评测——用到你自己项目里的一个模型调用上，并记录评测给出的结果。

## 为什么有这节课

课程用手写回复，是为了在任何地方都能离线运行。你的功能连的是真实模型。
模式之所以能迁移，是因为代码自始至终只依赖一个东西：一个接收消息、返回
文本的可调用对象。

## 本课内容

1. **把你的厂商调用包到接缝后面。** 写一个函数 `live(messages) -> str`，
   调用你所用厂商的 API 并返回回复文本。API key 从环境变量读取；绝不写进
   代码，也绝不进录音。
2. **先写契约。** 确切的字段、类型、范围；工具及其参数类型；重试次数和
   兜底。第 2 课练习里的草稿就是起点。
3. **录一次，每次改动都回放。** 包一层 live client，把每条回复都存下来；
   用它把带标注的用例跑一遍，之后每次改动都从录音评测——不要 key、不花钱、
   每次答案相同：

   ```python
   import json
   from pathlib import Path


   class RecordingClient:
       """Wrap a live client and keep every reply so an eval can replay it."""

       def __init__(self, live):
           self.live = live
           self.replies = []

       def __call__(self, messages):
           text = self.live(messages)
           self.replies.append(text)
           return text


   def save_recordings(recorded: dict[str, list[str]], path: Path) -> None:
       path.write_text(
           json.dumps({"replies": recorded}, ensure_ascii=False, indent=2) + "\n",
           encoding="utf-8",
       )
   ```

   有意识地重新录制——改了提示词、换了模型或厂商时——并把新的评测输出和
   旧的对比。
4. **用评测做门禁。** 在看结果之前定好阈值，让评测命令低于阈值时以非零
   退出——和 `ticket_triage.py` 一样的形状。
5. **记下它没证明什么。** 写三行：已验证 / 未验证 / 已知局限。「未验证」
   永远包括你没录到的真实流量。

如果你的功能不合身——输出是没有字段可校验的自由文本，或者用例太少没法
标注——写下模式在哪里失效了。这个判断本身就是本事的一部分。

## 练习

在录任何东西之前，先为你的功能标注至少十个真实或贴近真实的输入。标出
你预计会兜底的那些。

## 检查点

本检查点自我报告。能回答下面三题时，用
`python verify.py --attest l05` 认领：

1. 你的 `live` client 返回什么？它的 key 从哪里来？
2. 你的第一行评测输出是什么？它过了你事先定的阈值吗？
3. 你的「未验证」清单上有什么是利益相关方会以为已覆盖的？

## 预期证据

你的输出契约、带标注的用例、第一行评测输出，以及三行记录。含客户数据的
录音不要放进公开仓库。
