---
id: course-claude-code
type: course
title: 用 Claude Code 实战 Python
summary: 一门由 Agent 授课的课程：从下载课程文件夹到交付一个经过测试与验证的 Python 报表工具——包括任务契约、最小变更和客观的通过/失败证据。
lang: zh-CN
content_version: 3
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-claude-code
  name_en: Reproduce the failure
  name_zh: 复现故障
  requires: 全部五个检查点认领通过（L01–L05）
course_id: course-claude-code
---

# 用 Claude Code 实战 Python

> 摘要：装好 Claude Code、装上 FlyPython Skill、让 Agent 取回本课文件（第 1 课
> 就是这三步，你什么都不用下载），说一句 **"开始第 1 课"**，Agent
> 就会带你走完一套经过验证的 AI 写 Python 工作流：任务契约 → 最小变更 →
> 测试 → 客观验证。课程结束时你会得到一个可运行的报表工具、一条可复现的
> 通过/失败命令，以及能迁移到自己项目里的模式。课程以 Claude Code 为教学
> 工具，但工作流适用于任何有能力的编码 Agent。

## 你将做出什么

一个小型 Python 报表工具：读取混乱的真实数据（CSV 或 JSON），把无效行
隔离而不是崩溃，汇总有效行，并以原子方式写出报告。课程附带三个场景
"皮肤"，你可以在自己熟悉的领域里练习：

| 皮肤 | 你的角色 | 数据 |
| --- | --- | --- |
| `scenario/excel-report/` | 把每周订单导出变成区域销售摘要 | `orders.csv` |
| `scenario/data-monitor/` | 检查来自服务器的服务延迟数据 | `metrics.csv` |
| `scenario/api-tool/` | 汇总从内部 API 拉取的工单数据 | `tickets.json` |

三个皮肤走同一份代码和同一套测试。真正的教学目标是技能——契约、错误
隔离、舍入、原子写入、验证；皮肤只是让它们具体可感。

## 教学契约（Agent 请先阅读本节）

如果你是授课的编码 Agent，请遵守以下规则：

- **受众：** 有 AI 协作经验、但卡在可靠性上的项目所有者——脚本能跑，
  一遇真实数据就坏。这不是 Python 入门教程，也不是提示词工程课。
- **前置条件：** PATH 中有 Python 3.11+，本文件夹已在工具中打开，能运行
  shell 命令。无需安装任何第三方包——课程只用标准库。
- **工具：** 以 Claude Code 2.x 完成教学与审核（审核日期 2026-09-12）。
  Claude Code 主版本更新会触发课程复审。
- **课程顺序：** L01 → L02 → L03 → L04 → L05，每次一课。绝不跳过课末的
  检查点。
- **教学风格：** 从本文件夹的文件出发，而不是凭通用知识。引用你正在
  满足的契约原文。做能让一个测试从红变绿的最小变更。不新增依赖，不修改
  `solution/`，改动当前课程未授权的文件前先询问。
- **何时停止：** 当检查点命令运行通过、且学习者能用自己的话说清"什么
  失败了、为什么"时，一课才算完成。说不出来就基于失败的测试重新讲，
  而不是直接看答案。
- **如何使用 `verify.py`：** 学员命令就是 `python verify.py`——它跑套件、
  打印逐检查点状态与已获认领码，在门控检查点（l03、l04）未全通过时以
  非零退出。`starter --expect-failure` 与 `solution` 留作维护者检查。
  「完成」指学习者做完有界改动后，默认命令把所有门显示为 `[passed]`。- **诚实规则：** 说明哪些内容没有验证过。不要宣称代码已达到生产可用。
  不承诺任何学习或职业结果。

## 本课程不涉及的内容

Claude Code 安装、提示词技巧、多文件架构、pandas 或真正的 Excel
（`.xlsx`）文件、部署、任何销售内容。这些主题在配套仓库里有指南和
手册——链接过去，不要现场发挥。


## 徽章契约

- 徽章：**复现故障徽章**（徽章 id `course-claude-code`）——认领全部五个检查点后获得。
- 挑战：L01–L05 检查点各 10 分；五项全部在 flypython.com 认领后另加 50 分课程徽章奖励。
- 证据：`python verify.py` —— L03（边界修改）与 L04（验证与审查）由测试套件客观判定；L01/L02/L05 为学习者自报。
- 提交：每个通过的检查点会打印确定性认领码，在 flypython.com 上记入你的账号。这是自我报告的证据，绝不是证书。

## 文件夹结构


```
COURSE.md / COURSE_cn.md   本文件（英文 / 中文）
lessons/L01.md … L05.md    课程（每课都有 _cn.md 中文版）
scenario/<skin>/           每个皮肤的数据文件与 scenario.json
TASK.md / TASK_cn.md       变更必须满足的任务契约
starter/report_tool.py     故意未完成的实现
solution/report_tool.py    已审核的参考实现（第 3 课不可抄袭）
tests/test_report_tool.py  契约测试套件（只读）
verify.py                  客观通过/失败证据
REVIEW.md                  维护者试跑记录
```

## 证据与许可

课程文件夹是经过审核的内容：`REVIEW.md` 记录最近一次试跑的日期、工具
版本和观察到的偏差。本文件夹中的代码采用 MIT 许可；课程文字采用
CC BY 4.0（见仓库 `LICENSE`）。发现教学偏差或不清楚的课程，请通过仓库的
`course-feedback` issue 表单反馈。
