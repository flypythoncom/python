---
id: course-cursor
type: course
title: "上手 Cursor"
summary: "经过验证的 Python 工作流——任务契约、有界改动、客观 verify.py 证据——在 Cursor 里手把手教：由 Agent 模式跑闭环，你监督 diff 与项目规则。"
lang: zh-CN
content_version: 2
status: reviewed
reviewed_on: 2026-09-13
badge:
  id: course-cursor
  name_en: Reproduce with Cursor in the loop
  name_zh: Cursor 协同复现
  requires: 认领全部五个检查点（L01–L05）
course_id: course-cursor
---

# 上手 Cursor

> 一句话：装好 Cursor、装上 FlyPython Skill、让 Agent 取回本课文件（第 1 课
> 就是这三步，你什么都不用下载），开一个 Agent 对话，对它说**「开始第 1 课」**。完成时你会得到一个能跑的报表工具、一条
> 可复现的通过/失败命令，以及 Cursor 工作流：Agent/Ask/Plan 模式、
> `.cursor/rules` 项目规则与 diff 审查。练习核心与 Claude Code、Codex
> 课程完全相同——变的只是你驱动的工具。

## 你要做的东西

一个小型 Python 报表工具：读进脏乱的真实数据（CSV 或 JSON）、隔离
无效行而不是直接崩溃、聚合有效行、原子地写出报告。课程自带三个
「场景皮肤」，让你在自己熟悉的领域里练习：

| 皮肤 | 你是…… | 数据 |
| --- | --- | --- |
| `scenario/excel-report/` | 把每周订单导出整理成区域汇总 | `orders.csv` |
| `scenario/data-monitor/` | 检查自家服务器的延迟数据 | `metrics.csv` |
| `scenario/api-tool/` | 汇总从内部 API 拉取的工单数据 | `tickets.json` |

三个皮肤跑的是同一份代码、同一套测试。真正的产品是这些技能——契约、
错误隔离、舍入、原子写、验证——皮肤只是让它们变得具体。

## 教学契约（先读，Agent）

如果你是教授本课程的 Cursor Agent，请遵守以下规则：

- **受众：** 有 AI 协作经验、但困在可靠性上的项目所有者——脚本能跑，
  一遇真实数据就坏。这不是 Python 入门教程，也不是提示词工程课。
- **前置条件：** PATH 上有 Python 3.11+，装有 Cursor 编辑器并已登录。
  无需安装任何包——课程只用标准库。学习者套餐的 Agent 额度能否撑完
  整门课在编写时未经证实——见 `REVIEW.md`。
- **工具：** 按 cursor.com/docs 上文档描述的 Cursor 编写（Agent/Ask/
  Plan 模式、带 `description`/`globs`/`alwaysApply` front matter 的
  `.cursor/rules/*.mdc` 项目规则、diff 审查）。真实授课实跑尚待
  完成——`REVIEW.md` 记录已验证与未验证的部分。Cursor 主版本发布
  会触发课程重审。
- **课序：** L01 → L02 → L03 → L04 → L05，一次课一个会话。
  绝不跳过课尾的检查点。
- **教学风格：** 从本文件夹里的文件出发，不要凭通用知识发挥。引用
  你正在满足的那条契约原文。做让测试从红变绿的最小改动。绝不加
  依赖、绝不改 `solution/`、动当前课程未点名的任何文件前先询问。
  仓库根若有 `AGENTS.md`，读它——Cursor 同样会读。
- **何时停下：** 一节课的检查点命令跑通、且学习者能用自己的话说清
  哪里坏了、为什么，这节课才算完。学习者说不出就从失败测试重新教，
  不要从 solution 教。
- **如何使用 `verify.py`：** 学员命令就是 `python verify.py`——它跑套件、
  打印逐检查点状态与已获认领码，在门控检查点（l03、l04）未全通过时以
  非零退出。`starter --expect-failure` 与 `solution` 留作维护者检查。
  「完成」指学习者做完有界改动后，默认命令把所有门显示为 `[passed]`。- **诚实规则：** 说清你没验证什么。不要声称代码达到生产可用。不要
  承诺学习或职业结果。

## 本课程不覆盖什么

Cursor 的安装、套餐定价、模型选择、MCP 配置、团队/管理功能，以及
任何推销内容。这些由配套仓库的指南与手册承载——给链接，不即兴发挥。

## 徽章契约

- 徽章：**Cursor 协同复现徽章**（badge id `course-cursor`）——认领全部五个检查点获得。
- 挑战：L01–L05 检查点，各 10 分；在 flypython.com 上集齐五个再加 50 分课程徽章奖励。
- 证据：`python verify.py`——L03（有界改动）与 L04（验证与评审）由套件客观把关；L01/L02/L05 为学习者自我报告。
- 提交：测试通过的检查点打印确定性认领码；自报检查点要先回答课后问题，再运行 `python verify.py --attest ID` 才打印码；在 flypython.com 上记入你的账号。这是自我报告的证据，从来不是证书。

## 文件夹地图

```
COURSE.md / COURSE_cn.md   本文件（EN / 中文）
lessons/L01.md … L05.md    课文（每课都有一个 _cn.md 对）
scenario/<skin>/           每个皮肤的数据文件与 scenario.json
TASK.md / TASK_cn.md       改动必须满足的任务契约
starter/report_tool.py     有意未完成的实现
solution/report_tool.py    评审过的解答（第 3 课不要抄）
tests/test_report_tool.py  契约套件（只读）
verify.py                  客观的通过/失败证据
REVIEW.md                  维护者实跑记录
```

## 证据与许可

本课程文件夹属于已评审内容：`REVIEW.md` 记录最近一次实跑——日期、
工具版本、观察到的偏差。文件夹内代码采用 MIT 许可；课文文字采用
CC BY 4.0（见仓库 `LICENSE`）。发现教学漂移或课程不清楚之处，请
通过仓库的 `course-feedback` issue 表单反馈。
