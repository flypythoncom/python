---
id: course-secure-code-l02
type: course
title: "第 2 课：把威胁模型写成契约"
summary: "对每个函数，说清谁控制输入、他想要什么、代码必须拒绝什么——再把 TASK.md 里的每一条拒绝追查到一个测试，以及它背后的 Python 文档。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
hints:
  - title: "本检查点考察什么"
    body: "你能把 `TASK.md` 当成一张拒绝清单来读，把每一条追查到一个测试，并说出是哪个 Python 特性让这条拒绝可靠。"
  - title: "先划信任边界"
    body: "在 `read_attachment(base_dir, name)` 里，`base_dir` 来自你的配置，`name` 来自请求。契约故意区别对待它们。"
  - title: "用机制，不用过滤"
    body: "绑定参数、解析后的路径、带密钥的签名：每一种都消除一整类攻击。坏字符串黑名单只消除你想到的那些字符串。"
---

# 第 2 课：把威胁模型写成契约

## 目标

你能对每个函数说出每个输入由谁控制、他想要什么；把 `TASK.md` 里的每一条
拒绝追查到一个测试；并说出让这条拒绝可靠（而不是碰巧有效）的标准库机制。

## 为什么有这节课

「把它弄安全」是你能给 Agent 的最含糊的请求。它产出的是去掉引号、检查
`..`、或者查找 `admin` 字样的输入过滤——攻击者每一个都能绕过去。写成契约
的威胁模型说清必须拒绝什么，让测试去检查；你选的机制则决定了这条拒绝对
没人写过测试的输入是否依然成立。

## 本课内容

把测试并排打开，读 `TASK.md`。对每个函数，契约回答三个问题：

| 函数 | 谁控制输入 | 他想要什么 | 拒绝它的机制 |
| --- | --- | --- | --- |
| `find_notes` | 搜索的人 | 别的 owner 的笔记 | `?` 占位符——`sqlite3` 文档推荐的绑定值方式；再加 `instr`，让 `%` 和 `_` 保持字面意义 |
| `read_attachment` | 给文件起名的人 | 进程能读的任何文件 | 先 `Path.resolve()` 再 `is_relative_to(base)`——检查路径真正指向哪里，符号链接也算 |
| `load_secret_key` | 读得到你源码的人 | 签名密钥 | 没有缺省值；不足 32 个字符就拒绝启动 |
| `hash_password` / `verify_password` | 偷到数据库的人 | 密码 | 通过 `hashlib.pbkdf2_hmac` 做加盐慢哈希；比较用 `hmac.compare_digest` |
| `dump_session` / `load_session` | 持有 cookie 的人 | 另一个身份——或代码执行 | JSON 加 HMAC-SHA256 签名，在解码*之前*校验；绝不用 `pickle` |

每个选择的一手来源都是 Python 文档：

- **`pickle`：** 模块文档开头就警告 pickle 不安全，只应反序列化你信任的
  数据。会话 token 来自客户端——它永远不是你信任的数据。
- **`sqlite3`：** 文档里关于占位符的操作指南展示了用 `?` 绑定值，并警告
  不要用字符串格式化拼 SQL。
- **`hmac.compare_digest`：** 以抵御计时攻击为设计目标进行比较；对秘密值
  用 `==` 做不到这一点。
- **`secrets`：** 用于安全 token 和盐的模块——不是 `random`。

在密码哈希上，契约选了 600 000 次迭代的 PBKDF2-HMAC-SHA256，因为它在
标准库里，而且这正是 OWASP Password Storage Cheat Sheet 给 PBKDF2 的设置。
同一份 cheat sheet 首选 Argon2id，其次 scrypt，在需要 FIPS-140 合规时
推荐 PBKDF2。在真实项目里，判断哪种情况适用于你。

## 练习

在你熟悉的项目里挑一个接收请求、文件或消息队列输入的函数，为它填同样的
三列。然后检查：你的机制真的是机制，还是一个只去掉了你恰好想到的攻击
字符串的过滤器？

## 检查点

能回答下面三题时，用 `python verify.py --attest l02` 认领本检查点：

1. `Path(base) / "/etc/passwd"` 的结果是什么？为什么契约拒绝所有绝对路径
   的 `name`——哪怕它恰好指向 `base_dir` 之内？
2. 为什么 `load_session` 必须在解码 payload *之前*校验签名？
3. 为什么「从查询里去掉引号」不是 `find_notes` 可以接受的修复？

## 预期证据

为你拥有的一个函数写的三列威胁模型，并标明其机制是机制还是过滤器。
