---
id: course-secure-code
type: course
title: "AI 写的 Python 代码的安全审查"
summary: "像攻击者一样审查一个看起来没问题、AI 风格的笔记服务——一次一类地堵上 SQL 注入、路径穿越、硬编码密钥、快速密码哈希和 pickle 会话，再通过重放攻击证明每处修复。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-10-11
badge:
  id: course-secure-code
  name_en: Plausible is not safe
  name_zh: 看起来对不等于安全
  requires: 认领全部五个检查点（L01–L05）
course_id: course-secure-code
---

# AI 写的 Python 代码的安全审查

> 一句话：在你的编码 Agent 里装上 FlyPython Skill，让它取回本课程，然后
> 说**「开始第 1 课」**。（课程文件经 Skill 送达——你不手动下载任何东西。）
> 你从一个对所有友好输入都能正常工作、却一个攻击都挡不住的笔记服务开始，
> 结束时九个攻击全被挡住，有一条能证明这一点的重放命令，并养成一套审查
> 助手下一次写的代码的习惯。只用标准库。

## 你要做的东西

你不是写新功能——而是审查并修复一个功能。`notes_app.py` 是一个小型
笔记服务，写法就像一份仓促的初稿常见的样子。它有五个漏洞，每个都属于
一个广为人知的弱点类别：

| starter 里的漏洞 | 弱点类别 | Python 参考 |
| --- | --- | --- |
| 用 f-string 拼出来的搜索 SQL | CWE-89 SQL 注入 | `sqlite3` 文档：占位符 |
| 原样拼接的附件路径 | CWE-22 路径穿越 | `pathlib.Path.resolve`、`is_relative_to` |
| `"dev-secret-change-me"` 兜底密钥 | CWE-798 硬编码凭据 | `os.environ` |
| 无盐 MD5 密码哈希 | CWE-916 / CWE-759 弱且无盐的密码哈希 | `hashlib.pbkdf2_hmac`、`secrets` |
| 以 base64 pickle 存储的会话 | CWE-502 反序列化不可信数据 | `pickle` 文档警告、`hmac` |

课程自带两个「场景皮肤」，各有种子数据和一份 `attacks.json`：

| 皮肤 | 你是…… | 攻击数 |
| --- | --- | --- |
| `scenario/team-notes/` | 为一个小团队的共享笔记做安全加固 | 9 |
| `scenario/clinic-notes/` | 为一家诊所的就诊笔记做安全加固（所有记录均为虚构） | 8 |

`python starter/attack_replay.py scenario/<skin>` 重放这些攻击。在原样的
starter 上，每个攻击都会成功。

## 教学契约（先读，Agent）

- **受众：** 交付由 AI 助手编写或大幅改写的 Python 代码的开发者或项目
  所有者——审 diff 时会看「能不能跑」，但还没有看「恶意输入能让它做
  什么」。这不是渗透测试课，也不是 Python 入门。
- **前置条件：** PATH 上有 Python 3.11+，以及任意一个能执行命令的编码
  Agent。只用标准库。
- **工具：** 与工具无关。本课程尚未在任何工具里实际授课；`REVIEW.md`
  记录机械验证结果和待完成的 Agent 授课实跑，实跑时会写明确切的工具与
  版本。
- **课序：** L01 → L02 → L03 → L04 → L05，一次课一个会话。
  绝不跳过课尾的检查点。
- **教学风格：** 从本文件夹里的文件及其引用的 Python 文档出发。引用你
  正在满足的那条 `TASK.md` 原文。每轮只堵一类弱点。绝不加依赖，绝不改
  `solution/`、`tests/`、`scenario/` 或 `attack_replay.py`，动当前课程
  未点名的任何文件前先询问。绝不通过对测试所用的攻击字符串做特判来
  让测试通过。
- **安全：** 这些攻击只触及本课程自己的文件和临时文件夹。绝不把它们指向
  你不拥有的系统。套件会故意反序列化一个无害的 gadget，它在临时文件夹里
  创建一个目录——第一次运行前要先告诉学习者。
- **何时停下：** 一节课的检查点命令跑通、且学习者能用自己的话说清攻击者
  能做什么、修复为什么能挡住它，这节课才算完。学习者说不出就从失败测试
  重新教，不要从 solution 教。
- **如何使用 `verify.py`：** 学员命令就是 `python verify.py`——它针对
  `starter/` 跑套件、打印逐检查点状态与已获认领码，直到每个检查点都
  通过（l03、l04）或已自报确认（l01、l02、l05）之前都以非零退出。`starter --expect-failure` 与 `solution` 留作
  维护者检查。
- **诚实规则：** 挡住九个攻击只证明这九个攻击被挡住了——不证明服务是
  安全的。说清哪些没有审查。不要声称代码达到生产可用。不要承诺学习或
  职业结果。

## 本课程不覆盖什么

认证与授权设计、CSRF 与 XSS、TLS、限流、依赖漏洞扫描、密钥轮换与存储、
部署加固、威胁建模框架，以及合规。密码哈希使用 600 000 次迭代的
PBKDF2-HMAC-SHA256，因为它在标准库里；OWASP 的 Password Storage Cheat
Sheet 首选 Argon2id，其次 scrypt，PBKDF2 用于 FIPS-140 场景——见第 2 课。
其余内容请链接到配套仓库的指南；不即兴发挥。

## 徽章契约

- 徽章：**看起来对不等于安全徽章**（badge id `course-secure-code`）——认领全部五个检查点获得。
- 挑战：L01–L05 检查点，各 10 分；在 flypython.com 上集齐五个再加 50 分课程徽章奖励。
- 证据：`python verify.py`——L03（每轮堵一类漏洞）与 L04（像攻击者一样复查）由套件客观把关；L01/L02/L05 为学习者自我报告。
- 提交：测试通过的检查点打印确定性认领码；自报检查点要先回答课后问题，再运行 `python verify.py --attest ID` 才打印码；在 flypython.com 上记入你的账号。这是自我报告的证据，从来不是证书。

## 文件夹地图

```
COURSE.md / COURSE_cn.md       本文件（EN / 中文）
lessons/L01.md … L05.md        课文（每课都有一个 _cn.md 对）
scenario/<skin>/               seed.json、attacks.json、attachments/、一个假的 secrets.txt
TASK.md / TASK_cn.md           改动必须满足的任务契约
starter/notes_app.py           不安全的初稿
starter/attack_replay.py       提供的攻击工具（只读）
solution/                      评审过的解答（第 3 课不要抄）
tests/test_notes_app.py        契约套件（16 个测试，只读）
verify.py                      客观的通过/失败证据
REVIEW.md                      维护者实跑记录
```

## 证据与许可

`REVIEW.md` 记录实跑状态——日期、工具版本、观察到的偏差。文件夹内代码
采用 MIT 许可；课文文字采用 CC BY 4.0（见仓库 `LICENSE`）。`secrets.txt`
文件里是假值，存在的意义只是被泄露。发现教学漂移或课程不清楚之处，请
通过仓库的 `course-feedback` issue 表单反馈。
