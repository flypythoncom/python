---
id: course-github-copilot-l03
type: course
title: "第 3 课：有界改动，一轮一审"
summary: "通过有界的轮次把 starter 推到全绿——每轮先审 diff 再发下一轮，用 Restore Checkpoint 和 Git 守住每一处改动。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
hints:
  - title: "本检查点考察什么"
    body: "starter 通过你监督的改动让九个测试全绿——`python verify.py` 只在 starter 套件变绿后显示本检查点的码。"
  - title: "先落盘，后审查"
    body: "在 Copilot 会话里，Agent 直接保存编辑，没有待定的 Keep/Undo 步骤。你的审查关口是每轮之后的改动文件 diff、用 Restore Checkpoint 回滚一轮，以及一组变绿后的 Git 提交。"
  - title: "完成的标志"
    body: "每个 diff 都能对上一条契约行，而且不看 solution/ 你也讲得清每一处改动。"
---

# 第 3 课：有界改动，一轮一审

## 目标

starter 通过一串有界改动让九个测试全绿，并且不看 solution，你也
讲得清 Agent 产出的每一个 diff。

## 为什么有这节课

这节课最容易被跳过——也恰恰是长本事的那节。放任 Agent 把文件一次
重写，什么也学不到，只留下一份你没底气审查的 diff。监督一连串小 diff、
各自钉在一条契约行上，才能让代码仍然是你的。

Copilot 有一点你必须知道：在 Copilot（Agent Host）会话里，Agent 直接
应用并保存编辑。Manual permissions 让命令和工具调用等你批准；它不会
扣住文件编辑等你批准。所以边界不是一个「接受」按钮——而是你在每轮
之后、发下一条提示词之前做的审查。

## 先铺好安全网（一次）

1. **Git 基线。** 如果工作目录还不是 Git 仓库，先跑 `git init`，再
   `git add -A` 和 `git commit -m "baseline"`。之后 Source Control 视图
   会准确显示每一轮改了什么。
2. **逐请求的改动摘要。** 在设置里打开 `chat.checkpoints.showFileChanges`。
   每次请求完成后都会列出它改的文件和行数，**View All File Changes**
   打开多文件 diff。
3. **（可选）动只读文件前先问。** `chat.tools.edits.autoApprove` 设置
   接受 glob；设成 `false` 的文件在编辑生效前会显示 diff 并等你批准。
   写进 `.vscode/settings.json`：

   ```json
   {
     "chat.tools.edits.autoApprove": {
       "**/*": true,
       "**/tests/**": false,
       "**/solution/**": false,
       "**/scenario/**": false
     }
   }
   ```

## 本课内容

开一个新的对话会话（已完结任务的对话带着过期上下文），保持 **Agent**
角色和 **Manual permissions**，说：

**“按 TASK.md 改 starter/report_tool.py。一次只修一组失败测试：
先 JSON 加载，再无效行隔离，再舍入，再原子写，最后是端到端测试。
每修完一组跑 `python verify.py starter`，然后停下来等我，再做下一组。”**

每一轮之后、回复之前：

- 打开这一轮改动的文件（或 Source Control），逐块读完。只应有
  `starter/report_tool.py` 变了。`tests/`、`solution/`、`scenario/` 里
  任何东西动了，就把鼠标悬停在那次请求上选 **Restore Checkpoint**，
  再问为什么。
- 标准库之外不加 import——连与本改动无关的 import 也不要。
- 每处改动朝一条契约行推进。顺手重构（「我顺便重命名了……」）就恢复
  检查点，用更窄的提示词重问。
- Agent 想改测试，答案是不行。测试是契约；动的是代码。
- 一组变绿、diff 讲得通，就在 Source Control 里提交。这个提交是你的
  永久记录；检查点是临时的。

命令批准请求也要读：`python verify.py starter` 安全；`pip install` 任何
东西都是停止信号。Restore Checkpoint 回滚文件和对话历史，但**不会**撤销
已经跑过的命令——这正是 Manual permissions 替你扣住命令的原因。

预期失败数逐组下降：7 → 5 → 4 → 3 → 2 → 0。

## 练习

挑 Agent 产出的一个 hunk——最好是「无效行隔离」那段——在对话里
讲回给它听：「第 N 行做了 X，满足契约行 Y」。讲不清就先让它走读
自己的 diff，再发下一组。

## 检查点

运行 `python verify.py`。本检查点的码只在 starter 套件
全绿时出现。不看材料能回答即算通过：

1. 这次有界改动走了几轮，是什么让每轮保持有界？
2. 你回滚或收窄过哪个 diff 或命令，用的是什么——检查点、拒绝批准，
   还是更窄的提示词？
3. 指出实现「无效行带原因隔离」的那个 hunk——它在哪？

## 预期证据

一次全绿的 `python verify.py starter` 运行、你按组做的提交，和你对这次
改动的逐块讲解。
