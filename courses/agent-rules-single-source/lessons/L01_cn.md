---
id: course-agent-rules-l01
type: course
title: "量化你已经存在的漂移"
summary: "对三个场景仓库运行检查器，把漂移读成测试失败，而不是一种感觉。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "考你能不能把漂移量化而不是凭感觉：对三个 scenario 仓库跑检查器，把每个结果当测试失败读，不当气氛。"
  - title: "认出三种仓库状态"
    body: "scenario 文件夹展示了契约要分类的三种形态——干净的单一真源仓库、带薄指针的仓库、副本已漂移的仓库。先说出谁是谁再往下走。"
  - title: "完成标准"
    body: "你能用文件而不是感觉解释 `ok=false`：哪个文件偏离了 `AGENTS.md`，检查器是怎么发现的。"
---

# 量化你已经存在的漂移

## 目标

对三个场景仓库运行检查器，把漂移读成测试失败，而不是一种感觉。

## 课程内容

运行 `python starter/rules_check.py scenario/drifted`——它说一切正常。这正是 bug：三个文件对同一行为各执一词，却没有任何东西察觉。然后运行验证器：

```bash
python verify.py starter --expect-failure
```

## 练习

- 把 `verify.py --expect-failure` 里的每个具名失败对应到一类真实漂移：无真源、无指针识别、无漂移报告
- 打开 `scenario/drifted/.cursorrules`，找出与 AGENTS.md 矛盾的规则

## 检查点

本课的命令运行通过，并且你能用自己的话回答下面的问题（由 Agent
提问、你作答——这就是关口）：

1. 本课跑了哪条命令，它判定了什么？
2. 一开始什么失败了、为什么——用你自己的话说？
3. 下次再信任类似的改动之前，你会先检查什么？

## 预期证据

命令输出记录与你的回答。
