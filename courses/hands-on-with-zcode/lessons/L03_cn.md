---
id: course-zcode-l03
type: course
title: "第 3 课：有界改动，逐任务盯守"
summary: "沿着目标的任务列表把 starter 推到全绿——用工作区 Git 状态审每一处落地的改动。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-13
hints:
  - title: "本检查点考察什么"
    body: "starter 通过你监督的改动让九个测试全绿——`python verify.py progress` 只在 starter 套件变绿后显示本检查点的码。"
  - title: "Git 状态就是边界"
    body: "工作区把 Git 状态放在执行旁边——每个任务完成后，工作区立刻显示改了什么。动错文件的任务一眼可见；用目标恢复倒回去，而不是叠补丁。"
  - title: "完成的标志"
    body: "每处改动都能对上一条契约行，Git 状态显示 starter/report_tool.py 之外没动过任何东西，而且不看 solution/ 你也讲得清每处编辑。"
---

# 第 3 课：有界改动，逐任务盯守

## 目标

starter 通过一串有界改动让九个测试全绿，工作区 Git 状态证明没有
动过别的东西，并且不看 solution，你也讲得清每一处编辑。

## 为什么有这节课

这节课最容易被跳过——也恰恰是长本事的那节。放任 Agent 一次重写
整个文件，什么也学不到，只留下一份你没底气审查的改动。监督一连串
小改动、各自钉在一条契约行上，才能让 AI 写的代码仍然是你的。
ZCode 把 Git 状态放在执行旁边——每个任务之后你都能直接看到动了
什么，「有没有越界」变成看一眼，而不是猜。

## 本课内容

第 2 课的目标与任务列表批准后，开始执行——一次一个任务，任务
之间按计划跑 `python verify.py starter`。

守住契约边界：

- 只动 `starter/report_tool.py`。每个任务后看 Git 状态：`tests/`、
  `solution/`、`scenario/` 动过就停掉目标，用它的恢复倒回去，
  而不是往上叠修正。
- 标准库之外不加 import。
- 每个任务朝一条契约行推进。顺手重构（「我顺便重命名了……」）
  一律拒绝。
- Agent 想改测试，答案是不行。测试是契约；动的是代码。

任务之间认真审。Git 状态给出 diff；读 hunk，不只读任务的自我
汇报。讲不清的改动就用恢复倒回去——Goal 模式管的正是这件事：
用更紧的指令重启这一步，而不是在坏状态上叠修复。

预期失败数逐任务下降：7 → 5 → 4 → 3 → 2 → 0。

## 练习

挑 Agent 的一处改动——最好是「无效行隔离」那步——在 Git diff
里找到它，讲回来：「这个 hunk 做了 X，满足契约行 Y」。讲不清就
让它走读那个 hunk，再跑下一个任务。

## 检查点

运行 `python verify.py progress`。本检查点的码只在 starter 套件
全绿时出现。不看材料能回答即算通过：

1. 这次有界改动走了几个任务，是什么让每个任务保持有界？
2. 你拒绝或恢复掉过哪处改动，为什么？
3. 指出实现「无效行带原因隔离」的那个 hunk——它在 diff 的哪里？

## 预期证据

一次全绿的 `python verify.py starter` 运行、一份只含
`starter/report_tool.py` 的 Git diff，和你的逐块讲解。
