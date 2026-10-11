---
id: course-secure-code-l04
type: course
title: "第 4 课：像攻击者一样复查"
summary: "测试全绿和 9/9 的重放只是地板。重放第二个皮肤、跑一遍静态扫描并记下它漏了什么、攻击一处套件从没试过的地方，并写下还有什么没审查。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
hints:
  - title: "本检查点考察什么"
    body: "starter 和 solution 双双通过——维护者那一对命令 `verify.py starter` / `verify.py solution` 都必须是绿的，你的 starter 套件通过后 `python verify.py` 打印本检查点的码。"
  - title: "扫描器找的是模式，不是意图"
    body: "在这个 starter 上，ruff 的 `S` 规则标出了 f-string SQL、MD5 和 `pickle.loads`——对路径拼接和兜底密钥一言不发。把干净的扫描结果当作证据中的一行。"
  - title: "完成的标志"
    body: "你有一份安全证据记录——已验证 / 未验证 / 已知局限——点名了没人审查过的部分。"
---

# 第 4 课：像攻击者一样复查

## 目标

两个套件都通过、两个皮肤的重放全部被挡住，你手握一份书面记录：审查了
什么、扫描器抓到和没抓到什么、还有什么没人审查过。

## 为什么有这节课

`blocked=9/9` 很容易被过度解读。它的意思是九个特定攻击被挡住了。真正的
攻击者会试第十个。安全审查就是追问「测试没试过什么」的习惯——并把答案
写下来，而不是想当然。

## 本课内容

亲自跑维护者那一对命令和两次重放：

```bash
python verify.py starter
python verify.py solution
python starter/attack_replay.py scenario/team-notes
python starter/attack_replay.py scenario/clinic-notes
```

套件只重放 `team-notes`。`clinic-notes` 用的是不同的 payload——
`x' OR 1=1 --`、注入到 *owner* 而不是查询里、`scans/../../secrets.txt`、
空密钥。如果你的修复都是机制，它不做任何改动就会打印 `blocked=8/8`。如果
没有，说明你有一处修复是过滤器。

然后做套件做不了的审查：

1. **跑静态扫描，再读它漏了什么。** 如果你有 Ruff（仓库的开发依赖里有
   它），对你的修复跑它的 flake8-bandit 规则：

   ```bash
   ruff check --isolated --select S starter/notes_app.py
   ```

   你的修复应该什么都不报。作为对照，在原始 starter 上 Ruff 0.16.10 报告
   S608（由字符串拼出的 SQL）、S324（MD5，两处）和 S301（`pickle.loads`）
   ——对路径拼接和 `"dev-secret-change-me"` 兜底值什么都不报。如果你提交过
   基线，对它跑同一条命令就能亲眼看到。扫描器是能抓住已知模式的快速初筛；
   它不是审查。
2. **攻击一处套件从没试过的地方。** 挑一个：带 Unicode 大小写的搜索
   （`É` 与 `é`）、一个是目录的附件名、一个签名有效但内容是 JSON 列表的
   会话 token、一个 10 000 字符长的密码。先预测，再运行，记下结果。
3. **读 diff 里删掉了什么。** 用 `git diff` 对比 starter 与你的基线。确认
   `pickle` 和 `md5` 都没了，也没有 `except Exception` 吞掉
   `SecurityError`。

## 练习

为这次改动写安全证据记录：

- **已验证：** 你跑过的命令、两次重放、扫描输出。
- **未验证：** 至少包括——整体的认证与授权、会话 token 如何传输（cookie
  标志、TLS）、登录限流、密钥的存储与轮换、依赖漏洞，以及所有不在
  `attacks.json` 里的攻击。
- **已知局限：** 第 2 步里你发现的、契约从未承诺过的东西，以及密码哈希的
  选择（PBKDF2 而不是 Argon2id）。

## 检查点

运行 `python verify.py`。starter 套件通过后本检查点的码就会打印；上面那
一对维护者命令都必须是绿的，这道门才名副其实。不看材料能回答即算通过：

1. `clinic-notes` 不做改动就通过了吗？如果没有，哪处修复是过滤器？
2. 在原始 starter 上扫描器漏掉了哪两类漏洞？为什么基于模式的工具会漏掉
   它们？
3. 你额外的那次攻击结果如何？它在你的「未验证」清单上吗？

## 预期证据

两次全绿运行、两次重放输出、扫描输出，以及你的三行证据记录。
