---
id: course-llm-features
type: course
title: "用 Python 构建 LLM 功能：结构化输出、工具调用与评测"
summary: "把演示日的一次模型调用变成能上线的功能——校验结构化输出、给工具调用设白名单、带着错误信息重试、拿不准就转人工而不是瞎猜，并用分母覆盖全部用例的离线评测来度量。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
badge:
  id: course-llm-features
  name_en: Model output is untrusted input
  name_zh: 模型输出是不可信输入
  requires: 认领全部五个检查点（L01–L05）
course_id: course-llm-features
---

# 用 Python 构建 LLM 功能：结构化输出、工具调用与评测

> 一句话：在你的编码 Agent 里装上 FlyPython Skill，让它取回本课程，然后
> 说**「开始第 1 课」**。（课程文件经 Skill 送达——你不手动下载任何东西。）
> 完成时你会得到 `ticket_triage.py`：一个把每条模型回复都当作不可信输入的
> 工单分诊功能，外加一个带通过/失败阈值的离线评测。不需要 API key、不需要
> 联网、不需要第三方包——由一个回放 client 代替模型。

## 你要做的东西

一个工单分诊功能：模型读一张工单，回复分类、优先级、一句话摘要，以及
是否必须由人来看。它可以先调用一个查询工具。课程自带三个「场景皮肤」，
每个都有带标注的用例和录好的模型回复：

| 皮肤 | 你是…… | 模型可调用的工具 |
| --- | --- | --- |
| `scenario/shop-support/` | 给网店客服收件箱分流 | `lookup_order(order_id)` |
| `scenario/it-helpdesk/` | 整理公司内部 IT 请求 | `lookup_device(asset_tag)` |
| `scenario/saas-feedback/` | 给应用内产品反馈分类 | 无 |

录好的回复是手写的练习数据，模仿模型真实会出现的失败形状——包在
Markdown 围栏里的 JSON、不在列表里的分类、`"priority": "high"`、多出来的
字段、不存在的工具、类型不对的工具参数、用闲聊散文代替 JSON。它们**不是**
从任何模型采集的，课程也不对任何真实模型出现这些问题的频率做任何声明。

## 教学契约（先读，Agent）

- **受众：** 在脚本或 notebook 里调过模型 API、现在要把这个调用放进产品
  的 Python 开发者——在产品里，一条格式错误的回复、一次幻觉出来的工具
  调用、一个看起来比实际好的评测，都会变成某个人的事故。这不是提示词
  工程课，也不是 Python 入门。
- **前置条件：** PATH 上有 Python 3.11+，以及任意一个能执行命令的编码
  Agent。只用标准库；练习不需要 API key，也不需要联网。
- **工具：** 与工具无关。本课程尚未在任何工具里实际授课；`REVIEW.md`
  记录机械验证结果和待完成的 Agent 授课实跑，实跑时会写明确切的工具与
  版本。
- **课序：** L01 → L02 → L03 → L04 → L05，一次课一个会话。
  绝不跳过课尾的检查点。
- **教学风格：** 从本文件夹里的文件出发，不要凭任何厂商 API 的通用知识
  发挥。引用你正在满足的那条 `TASK.md` 原文。做让测试从红变绿的最小
  改动。绝不加依赖，绝不改 `solution/`、`tests/` 或 `scenario/`，动当前
  课程未点名的任何文件前先询问。绝不为了让某条录好的回复通过而放松校验。
- **何时停下：** 一节课的检查点命令跑通、且学习者能用自己的话说清
  哪里坏了、为什么，这节课才算完。学习者说不出就从失败测试重新教，
  不要从 solution 教。
- **如何使用 `verify.py`：** 学员命令就是 `python verify.py`——它针对
  `starter/` 跑套件、打印逐检查点状态与已获认领码，直到每个检查点都
  通过（l03、l04）或已自报确认（l01、l02、l05）之前都以非零退出。`starter --expect-failure` 与 `solution` 留作
  维护者检查。
- **诚实规则：** 在少量录好的回复上跑的离线评测，说明不了真实模型在真实
  流量上的表现——要讲明白。不要声称功能达到生产可用。不要承诺学习或
  职业结果。

## 本课程不覆盖什么

任何具体厂商的 SDK 或其结构化输出模式、API key 与密钥管理、提示词措辞、
检索增强（RAG）与 embedding、微调、Agent 框架、流式输出、成本与延迟
预算，以及在生产流量上的在线评测。第 5 课展示真实 client 从哪里接入；
其余内容由配套仓库的指南承载——给链接，不即兴发挥。

## 徽章契约

- 徽章：**模型输出是不可信输入徽章**（badge id `course-llm-features`）——认领全部五个检查点获得。
- 挑战：L01–L05 检查点，各 10 分；在 flypython.com 上集齐五个再加 50 分课程徽章奖励。
- 证据：`python verify.py`——L03（校验、工具调用、重试）与 L04（诚实评测）由套件客观把关；L01/L02/L05 为学习者自我报告。
- 提交：测试通过的检查点打印确定性认领码；自报检查点要先回答课后问题，再运行 `python verify.py --attest ID` 才打印码；在 flypython.com 上记入你的账号。这是自我报告的证据，从来不是证书。

## 文件夹地图

```
COURSE.md / COURSE_cn.md      本文件（EN / 中文）
lessons/L01.md … L05.md       课文（每课都有一个 _cn.md 对）
scenario/<skin>/              scenario.json、cases.json、recordings.json、查询数据
TASK.md / TASK_cn.md          改动必须满足的任务契约
starter/ticket_triage.py      演示日版本的实现
solution/ticket_triage.py     评审过的解答（第 3 课不要抄）
tests/test_ticket_triage.py   契约套件（15 个测试，只读）
verify.py                     客观的通过/失败证据
REVIEW.md                     维护者实跑记录
```

## 证据与许可

`REVIEW.md` 记录实跑状态——日期、工具版本、观察到的偏差。文件夹内代码
采用 MIT 许可；课文文字采用 CC BY 4.0（见仓库 `LICENSE`）。发现教学漂移
或课程不清楚之处，请通过仓库的 `course-feedback` issue 表单反馈。
