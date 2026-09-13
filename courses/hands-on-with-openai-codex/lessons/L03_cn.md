---
id: course-codex-cli-l03
type: course
title: "第 3 课：有界改动，逐块审 diff"
summary: "通过有界的轮次把 starter 推到全绿——并用应用内的 diff 审查与审批机制守住每一处改动。"
lang: zh-CN
content_version: 2
status: reviewed
reviewed_on: 2026-09-13
hints:
  - title: "本检查点考察什么"
    body: "starter 通过你监督的改动让九个测试全绿——`python verify.py` 只在 starter 套件变绿后显示本检查点的码。"
  - title: "审批就是边界"
    body: "应用会在跑命令前询问、在每个文件 diff 落地前展示。读命令、读 diff——闭眼批准正是「有界工作」变成「整文件重写」的方式。"
  - title: "完成的标志"
    body: "每个 diff 都能对上一条契约行，而且不看 solution/ 你也讲得清每一处改动。"
---

# 第 3 课：有界改动，逐块审 diff

## 目标

starter 通过一串有界改动让九个测试全绿，并且不看 solution，你也讲得清
Agent 产出的每一个 diff。

## 为什么有这节课

这节课最容易被跳过——也恰恰是长本事的那节。放任一个线程把文件一次
重写，什么也学不到，只留下一份你没底气审查的 diff。监督一连串小
diff、各自钉在一条契约行上，才能让 AI 写的代码仍然是你的。Codex
应用的审批模型就是为这个存在的：命令要先问再跑，编辑以可审查的
diff 落地。

## 本课内容

开一个新线程（已完结任务的线程带着过期上下文），说：

**“按 TASK.md 改 starter/report_tool.py。一次只修一组失败测试：先
JSON 加载，再无效行隔离，再舍入，再原子写，最后是端到端测试。每修完
一组跑 `python verify.py starter`，先给我 diff 再继续。”**

守住契约边界：

- 只动 `starter/report_tool.py`。diff 碰到 `tests/`、`solution/`、
  `scenario/` 就停下问为什么。
- 标准库之外不加 import——连与本改动无关的 import 也不要。
- 每处改动朝一条契约行推进。顺手重构（「我顺便重命名了……」）一律
  拒绝。
- Agent 想改测试，答案是不行。测试是契约；动的是代码。

认真用审批提示。Agent 提议命令时读它——`python verify.py starter`
安全；`pip install` 任何东西都是停止信号。它改文件时打开 diff 视图，
逐块读完再接受。讲不清的 diff 就拒绝。

预期失败数逐组下降：7 → 5 → 4 → 3 → 2 → 0。

## 练习

挑 Agent 产出的一个 hunk——最好是「无效行隔离」那段——在线程里讲回
给它听：「第 N 行做了 X，满足契约行 Y」。讲不清就先让它走读自己的
diff，再接受下一处改动。

## 检查点

运行 `python verify.py`。本检查点的码只在 starter 套件全绿
时出现。不看材料能回答即算通过：

1. 这次有界改动走了几轮，是什么让每轮保持有界？
2. 你拒绝或收窄过哪个审批提示，为什么？
3. 指出实现「无效行带原因隔离」的那个 hunk——它在哪？

## 预期证据

一次全绿的 `python verify.py starter` 运行，和你对这次改动的逐块
讲解。
