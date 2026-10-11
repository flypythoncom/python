---
id: course-secure-code-l03
type: course
title: "第 3 课：每轮只堵一类漏洞"
summary: "五个有界轮次——搜索、附件、密钥、密码、会话——每轮用机制（绝不用过滤）堵上一类弱点，并用测试和重放证明。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
hints:
  - title: "本检查点考察什么"
    body: "starter 通过你监督的改动让十六个测试全绿——`python verify.py` 只在 starter 套件变绿后显示本检查点的码。"
  - title: "警惕过滤器"
    body: "如果 diff 加了 `replace(\"'\", \"\")`、检查 `'..' in name`，或者拿 `attacks.json` 里的攻击字符串做比较，拒绝它。契约要的是机制。"
  - title: "重放最后才变绿"
    body: "`test_replay_blocks_every_team_notes_attack` 需要五类漏洞全部堵上。直到最后一轮它都是红的。"
---

# 第 3 课：每轮只堵一类漏洞

## 目标

starter 通过五个有界轮次让十六个测试全绿，每轮堵上一类弱点，并且你能
解释每处修复为什么对测试从没试过的输入同样有效。

## 为什么有这节课

让 Agent「修掉安全问题」，你会得到一个大 diff：真正的修复与过滤器、
重命名、新辅助函数混在一起。你分不清哪一行挡住了哪个攻击。每轮一类，才能
让每处修复小到可以对照第 2 课的机制逐一核对。

## 本课内容

开一个新的 Agent 会话，说：

**“按 TASK.md 改 starter/notes_app.py，每轮只处理一类弱点：先
find_notes，再 read_attachment，再 load_secret_key，再把 hash_password 和
verify_password 一起，最后把 dump_session 和 load_session 一起。每轮之后
跑 `python verify.py starter` 和
`python starter/attack_replay.py scenario/team-notes`，给我看 diff，然后
等我。不要改 tests/、solution/、scenario/ 或 attack_replay.py。”**

预期失败数和重放结果这样变化：

| 哪一轮之后 | 失败测试数 | 重放（`team-notes`） |
| --- | --- | --- |
| 开始 | 11 | 0/9 |
| `find_notes` | 9 | 2/9 |
| `read_attachment` | 6 | 4/9 |
| `load_secret_key` | 5 | 6/9 |
| 密码 | 3 | 7/9 |
| 会话 | 0 | 9/9 |

（在无法创建符号链接的平台上，符号链接测试会被跳过，前两行分别是 10 和
8。）

让每一轮守住它的机制：

- **搜索：** SQL 字符串是常量；值放进参数元组。拒绝任何转义引号或删除
  字符的 diff。用 `LIKE` 加通配符转义也可以，但前提是转义完整；`instr`
  干脆避开了这个问题。
- **附件：** 先 resolve，再用 `is_relative_to` 检查是否包含在内。拒绝
  `if ".." in name`——它漏掉符号链接和绝对路径，还会误拒 `notes..txt`
  这样的正常名字。
- **密钥：** 永远没有兜底值。如果 Agent 加了一个「开发环境缺省值」，它就
  把漏洞又带回来了。
- **密码：** 盐用 `secrets.token_bytes(16)`，摘要用 `hashlib.pbkdf2_hmac`，
  校验用 `hmac.compare_digest`。`verify_password` 对任何不是它自己写出的
  格式都返回 False。
- **会话：** 把 `pickle` 从文件里彻底删掉。先校验签名再解码；只捕获你
  预期的解码错误，并把它们转成 `SecurityError`。

会话那一轮之后，运行 `grep -n pickle starter/notes_app.py`。它应该什么都
不打印。

## 练习

针对附件修复，对 `scenario/team-notes/attachments` 试两个测试没用过的
名字：`./agenda.txt`（正常名字——应该能读）和
`agenda.txt/../../secrets.txt`（应该被拒绝）。运行前先预测每个结果，
记下机制是否无需新增一行代码就处理了这两个。

## 检查点

运行 `python verify.py`。本检查点的码只在 starter 套件全绿时出现。不看
材料能回答即算通过：

1. 你因为它是过滤器而不是机制，拒绝或收窄过哪个 diff？
2. 为什么 `test_replay_blocks_every_team_notes_attack` 只在最后一轮才通过？
3. 如果 `load_session` 先解码 payload、后校验签名，会发生什么？

## 预期证据

一次全绿的 `python verify.py starter`、打印 `blocked=9/9` 的重放、五个
diff，以及你的练习结果。
