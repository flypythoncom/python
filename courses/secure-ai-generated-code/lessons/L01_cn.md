---
id: course-secure-code-l01
type: course
title: "第 1 课：看起来对不等于安全"
summary: "通过 FlyPython Skill 取回课程，读一个看起来没问题的笔记服务，然后对它重放九个攻击，看着每一个都得手。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
hints:
  - title: "本检查点考察什么"
    body: "先复现攻击再动手修：`python verify.py` 把 l03 和 l04 显示为 `[open]`，`attack_replay.py` 对 `team-notes` 打印 `blocked=0/9`。"
  - title: "先读代码，再看攻击"
    body: "运行任何东西之前，先写下你觉得哪里不对。把你的猜测和重放结果对比，就是这一课。"
  - title: "完成的标志"
    body: "对五个函数中的每一个，你都能说出攻击者能得到什么。然后用 `python verify.py --attest l01` 认领本检查点。"
---

# 第 1 课：看起来对不等于安全

## 目标

课程文件已由你的 Agent 取回工作目录。你在不运行的情况下读过 starter、
写下了你认为哪里不对，然后重放了攻击——并能说出攻击者从五个函数中的每
一个能得到什么。本课不改任何代码。

## 第 1 步——让 Agent 取回本课（你不下载）

在一个空工作目录里打开你的编码 Agent，粘贴这一句话：

> Read https://flypython.com/skills/flypython/SKILL.md and start the FlyPython course `secure-ai-generated-code`.

Agent 会给你一个授权链接和一组短码。打开链接、登录、核对码与 Agent
显示的一致后点「允许」，然后对 Agent 说「好了」。它把本课文件写到
`courses/secure-ai-generated-code/`。

**前提**：这些课程需要一个能执行命令**并且**能联网的编码 Agent。只能
聊天的网页 AI 做不了。

**安全说明：** 本课程的攻击只触及课程自己的文件和临时文件夹。有一个测试
会故意反序列化一个无害的 payload，它在临时文件夹里创建一个目录——那是
证据，不是意外。

## 为什么有这一课

AI 写的代码通常可读、风格一致、有文档。评审者正是靠这些信号判断代码
没问题——而它们对「恶意输入能让它做什么」一个字也没说。starter 对每个
友好输入都能正常工作。这正是它危险的原因。

## 热身（5 分钟，不用 Agent）

打开 `starter/notes_app.py`，读 `init_db` 之后的五个函数。每个写一行：
它信任了什么输入，可能出什么问题？先别运行任何东西。

## 本课内容

让 Agent 先只读不动手：

**“读 COURSE.md——它是本文件夹的教学契约。再读 TASK.md 和
starter/notes_app.py。不要改任何文件。告诉我每个函数信任了哪个它不该
信任的输入。”**

然后运行学员命令和攻击重放：

```bash
python verify.py
python starter/attack_replay.py scenario/team-notes
```

重放打印 `blocked=0/9`。读那些 `[OPEN]` 行——每一行都是真实后果：

| 攻击 | 攻击者得到了什么 |
| --- | --- |
| `t01`、`t02`（sql） | 以 Alice 身份搜索，却拿到 Bob 和 Carol 的笔记，包括「Salary review」 |
| `t03`、`t04`（path） | `secrets.txt` 的内容——一个在 `attachments/` 之外的文件 |
| `t05`、`t06`（secret-key） | 一个用源码里人人可见的密钥启动的服务 |
| `t07`（fast-hash） | 一次 MD5 调用就能复现的存储哈希——以及一个泄露的 MD5 仍然能登录 |
| `t08`（forged-session） | 攻击者用自己的密钥签出来的 `admin` 会话 |
| `t09`（pickle-session） | 代码执行：payload 在加载时创建了一个目录 |

套件里有十一个失败测试钉住这些行为。维护者命令会打印它们：

```bash
python verify.py starter --expect-failure
```

有五个测试已经通过：正常搜索能用且限定 owner、正常附件能读、密码能与
自己的哈希验证通过、会话能往返、重放工具能打印用法。每条友好路径都能用。

## 练习

把热身笔记和重放结果对比。哪些漏洞你读代码就发现了，哪些漏掉了？挑一个
你漏掉的，让 Agent 用两句话解释这个攻击——不是让它修。

## 检查点

运行 `python verify.py`。不看材料能回答下面三题时，用
`python verify.py --attest l01` 认领本检查点：

1. 查询 `%' OR owner != '` 是怎样把 Alice 的搜索变成所有人的笔记的？
   写出 starter 实际执行的 SQL。
2. 为什么 `t09` 算代码执行，而不只是「坏数据」？
3. 热身时你漏掉了哪个漏洞？代码的什么地方让它看起来没问题？

## 预期证据

你的热身笔记、重放输出，以及三个答案。
