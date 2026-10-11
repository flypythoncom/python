---
id: course-llm-features-l04
type: course
title: "第 4 课：诚实地读评测"
summary: "套件全绿证明的是契约；评测度量的是功能。跑完三个皮肤，接受那个没过阈值的结果，并写下少量录好的回复能说明什么、不能说明什么。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
hints:
  - title: "本检查点考察什么"
    body: "starter 和 solution 双双通过——维护者那一对命令 `verify.py starter` / `verify.py solution` 都必须是绿的，你的 starter 套件通过后 `python verify.py` 打印本检查点的码。"
  - title: "评测不通过也可以是正确结果"
    body: "`shop-support` 报出 0.750，阈值 0.800，以 1 退出。你的代码是对的；这个功能在这份数据上还不够好。调低阈值不是修复。"
  - title: "完成的标志"
    body: "你有一份三行证据记录——已验证 / 未验证 / 已知局限——同事拿到就能据此行动。"
---

# 第 4 课：诚实地读评测

## 目标

两个套件都通过，你在每个皮肤上跑过评测，并手握一份书面记录：这些数字
证明了什么、没证明什么。

## 为什么有这节课

第 1 课里，starter 的评测在一个六个用例崩了一个的皮肤上报出 100%。模型
功能过早上线，最常见的原因就是这个：不是模型差，而是评测把失败藏起来了。
现在评测的分母是全部用例，数字可能会*下降*——这正是目的所在。

## 本课内容

亲自在终端里跑维护者那一对命令：

```bash
python verify.py starter
python verify.py solution
```

再在每个皮肤上跑你的评测：

```bash
python starter/ticket_triage.py scenario/shop-support
python starter/ticket_triage.py scenario/it-helpdesk
python starter/ticket_triage.py scenario/saas-feedback
```

你应该看到：

| 皮肤 | 结果 | 退出码 |
| --- | --- | --- |
| `shop-support` | `accuracy=0.750 correct=6/8 fallbacks=1` | 1 |
| `it-helpdesk` | `accuracy=0.833 correct=5/6 fallbacks=1` | 0 |
| `saas-feedback` | `accuracy=0.800 correct=4/5 fallbacks=0` | 0 |

拿 `it-helpdesk` 和第 1 课对比：starter 说 1.000，你的评测说 0.833。同样的
录好回复，诚实的分母。

现在像评审者一样读每一行失败：

1. **`shop-support` 没过阈值——这是对的。** 用例 `s08` 得到一个合法但错误
   的分类；`s07` 两次散文回复后兜底给了人。你的代码没有任何错。这个功能
   在这份数据上低于你定的标准。试试 `--min-accuracy 0.7`，看它「通过」——
   然后写下为什么这不是修复。
2. **兜底安全，但不是免费的。** `h06` 兜底是因为两次回复都超过了 120 字符
   的摘要上限。把兜底单独计数：一个对一半工单都兜底的功能，安全但没用。
3. **看评测没打分的部分。** 这里的正确性是 `category` + `needs_human`。
   `priority` 和 `summary` 只校验形状，从不与标注比较。判断这对你的功能
   是否可以接受。
4. **检查套件没钉的边界。** `cases.json` 为空会怎样？`recordings.json` 里的
   回复比循环要的少会怎样？（`ReplayClient` 会抛异常——你的循环应该让它
   抛出来。）挑一个跑一下，记下发生了什么。

## 练习

为这个功能写三行证据记录：

- **已验证：** 你跑过的命令和它们证明了什么。
- **未验证：** 至少包括——真实模型的行为、你没录到的流量、没打分的字段，
  以及录音没有模仿到的一切。
- **已知局限：** 每个皮肤没达到或勉强达到的阈值，以及兜底率。

## 检查点

运行 `python verify.py`。starter 套件通过后本检查点的码就会打印；上面那
一对维护者命令都必须是绿的，这道门才名副其实。不看材料能回答即算通过：

1. 为什么 `shop-support` 以 1 退出是你的代码的正确行为？
2. 在六个手写用例上的 `accuracy=0.833`，能告诉你真实模型处理真实工单时
   的什么？
3. 你会最先把哪个字段加进评测打分，为什么？

## 预期证据

两次全绿运行、三行评测输出，以及你的三行证据记录。
