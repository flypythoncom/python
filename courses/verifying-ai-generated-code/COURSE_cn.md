---
id: course-verify-ship
type: course
title: "从「能跑」到「能上线」：验证 AI 写的代码"
summary: 为你的 AI 项目补上缺失的发布证据机器——一个 ship check：运行测试、解析实际跑了什么、拒绝零测试项目，并写出诚实的交付记录。
lang: zh-CN
content_version: 3
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-verify-ship
  name_en: It runs is not evidence
  name_zh: 能跑不是证据
  requires: 全部五个检查点认领通过（L01–L05）
course_id: course-verify-ship
---

# 从「能跑」到「能上线」：验证 AI 写的代码

> 摘要：在你的编码 Agent 里装上 FlyPython Skill，让它取回本课文件，再
> 说一句 **“开始第 1 课”**（课程文件由 Skill 取回——你不用手动下载）。
> 课程结束时你拥有 `ship_check.py`：一条命令把“演示能跑”变成一份书面
> 交付记录——命令、退出码、解析出的测试数、一个拒绝零测试项目的判定，
> 以及一份显式的未验证清单。工具无关；仅用 Python 标准库。

## 你将做出什么

面向小型 AI 项目的发布证据构建器。给定一个带 `ship.json` 的项目目录，
它运行配置的检查命令，解析实际跑了多少测试、是否通过，并原子地写出
`SHIP-RECORD.json` 与诚实的判定：

| 皮肤 | 状态 | 数据 |
| --- | --- | --- |
| `scenario/green-project/` | 两个通过的测试 + 声明的未验证项 | `ship.json`、`calc.py`、`tests/` |
| `scenario/red-project/` | 一个故意写错的断言 | 正在研究的回归 |
| `scenario/no-tests/` | 零个测试——绝不能放行的状态 | 空的 `tests/` |

## 教学契约（Agent 请先阅读本节）

- **受众：** 正在交付 AI 写的 Python、却还只能凭记忆回答“什么证明了
  这次发布”的项目所有者。
- **前置条件：** PATH 中有 Python 3.11+，任一编码 Agent（以 Claude
  Code 2.x 与 Codex CLI 0.x 完成教学与审核，审核日期 2026-09-12）。
  只用标准库。
- **课程顺序：** L01 → L05；绝不跳过检查点。
- **教学风格：** 从本文件夹的文件出发；引用你满足的契约原文；每个
  失败测试做最小变更；不新增依赖；不修改 `solution/` 与场景项目；
  改动未授权文件前先询问。
- **何时停止：** 检查点命令通过、且学习者能说清什么失败了、为什么。
- **`verify.py`：** `python verify.py starter --expect-failure` 复现七个
  具名失败；`python verify.py solution` 通过 10/10。
- **诚实规则：** 记录里的“未验证”清单正是重点——永远不要把一份通过
  的记录说成比它包含的更多。

## 本课程不涉及的内容

部署平台、CI 服务、性能测试、预发环境。flypython.com 的产品质量指南
覆盖更完整的发布清单；本课程构建的是证据核心。


## 徽章契约

- 徽章：**「能跑」不是证据徽章**（徽章 id `course-verify-ship`）——认领全部五个检查点后获得。
- 挑战：L01–L05 检查点各 10 分；五项全部在 flypython.com 认领后另加 50 分课程徽章奖励。
- 证据：`python verify.py` —— L03（边界修改）与 L04（验证与审查）由测试套件客观判定；L01/L02/L05 为学习者自报。
- 提交：每个通过的检查点会打印确定性认领码，在 flypython.com 上记入你的账号。这是自我报告的证据，绝不是证书。

## 文件夹结构


`COURSE.md`/`COURSE_cn.md`、双语 `lessons/`、`scenario/` 项目、
`TASK.md`/`TASK_cn.md`（代码契约）、`starter/`、`solution/`、`tests/`
（10 个测试）、`verify.py`、`REVIEW.md`。

## 证据与许可

`REVIEW.md` 记录试跑状态。代码 MIT；文字 CC BY 4.0（见仓库 `LICENSE`）。
教学偏差请走 `course-feedback` issue 表单。
