---
id: course-agent-rules
type: course
title: Agent 规则的单一真源
summary: 不再同时维护彼此打架的 AGENTS.md、CLAUDE.md 与 .cursorrules——亲手构建一个能证明仓库只有一处规则真源的检查器，由你的编码 Agent 授课。
lang: zh-CN
content_version: 3
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-agent-rules
  name_en: Measure the drift
  name_zh: 规则漂移检测
  requires: 全部五个检查点认领通过（L01–L05）
course_id: course-agent-rules
---

# Agent 规则的单一真源

> 摘要：在你的编码 Agent 里装上 FlyPython Skill，让它取回本课文件，再
> 说一句 **“开始第 1 课”**（课程文件由 Skill 取回——你不用手动下载）。
> 课程结束时你拥有一个可运行的规则一致性检查器（`rules_check.py`）——
> 任何规则文件偏离 AGENTS.md 的那一刻，CI 就会失败——外加应用到你自己
> 仓库的单一真源配置。天然工具无关：Claude Code、Codex CLI、Cursor
> 都读这些文件。

## 你将做出什么

一个仅用标准库的检查器，强制执行本仓库自己使用的契约：`AGENTS.md`
必须存在且非空，其他被识别的规则文件（`CLAUDE.md`、`.cursorrules`）
要么是指向它的瘦指针，要么是它的精确副本。其余情况都算漂移——带
原因报告并以非零退出码失败。课程附带三个场景仓库：

| 皮肤 | 状态 | 数据 |
| --- | --- | --- |
| `scenario/thin-pointer/` | 健康：AGENTS.md + 两个指针文件 | 指针式 CLAUDE.md、.cursorrules |
| `scenario/single-copy/` | 健康：AGENTS.md + 精确副本 | 完全重复的规则文本 |
| `scenario/drifted/` | 故障：.cursorrules 复述过期规则 | 一个待捕获的真实漂移 |

## 教学契约（Agent 请先阅读本节）

- **受众：** 为多个 Agent 工具维护规则文件的任何人——你体会过三个
  文件对同一行为各执一词的痛苦。
- **前置条件：** PATH 中有 Python 3.11+，任一编码 Agent（以 Claude
  Code 2.x 与 Codex CLI 0.x 完成教学与审核，审核日期 2026-09-12——
  设计上工具无关）。只用标准库。
- **课程顺序：** L01 → L05；绝不跳过检查点。
- **教学风格：** 从本文件夹的文件出发；引用你满足的契约原文；每个
  失败测试做最小变更；不新增依赖；不修改 `solution/`；改动未授权文件
  前先询问。
- **何时停止：** 检查点命令通过、且学习者能说清什么失败了、为什么。
- **`verify.py`：** `python verify.py starter --expect-failure` 复现六个
  具名失败；`python verify.py solution` 通过 11/11。
- **诚实规则：** 说明哪些没验证过；不保证 Agent 服从——检查器报告的是
  文件状态，不是 Agent 行为。

## 本课程不涉及的内容

该写什么规则（见仓库 `templates/AGENT_RULES.example.md` 与
flypython.com 上的 AGENTS.md 指南）、多仓库配置、机器策略强制。检查器
刻意收窄：一个目录、三个文件名、一个真源。


## 徽章契约

- 徽章：**量化漂移徽章**（徽章 id `course-agent-rules`）——认领全部五个检查点后获得。
- 挑战：L01–L05 检查点各 10 分；五项全部在 flypython.com 认领后另加 50 分课程徽章奖励。
- 证据：`python verify.py` —— L03（边界修改）与 L04（验证与审查）由测试套件客观判定；L01/L02/L05 为学习者自报。
- 提交：测试通过的检查点打印确定性认领码；自报检查点要先回答课后问题，再运行 `python verify.py --attest ID` 才打印码，在 flypython.com 上记入你的账号。这是自我报告的证据，绝不是证书。

## 文件夹结构


`COURSE.md`/`COURSE_cn.md`、双语 `lessons/`、`scenario/` 仓库、
`TASK.md`/`TASK_cn.md`（代码契约）、`starter/`、`solution/`、`tests/`
（11 个测试）、`verify.py`、`REVIEW.md`。

## 证据与许可

`REVIEW.md` 记录试跑状态。代码 MIT；文字 CC BY 4.0（见仓库 `LICENSE`）。
教学偏差请走 `course-feedback` issue 表单。
