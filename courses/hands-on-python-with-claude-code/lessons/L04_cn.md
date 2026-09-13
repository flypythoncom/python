---
id: course-claude-code-l04
type: course
title: "第 4 课：像工程师一样验证，像怀疑者一样审查"
summary: 跑完整验证闭环，审查 Agent 的 diff 是否越界、有无副作用，并如实记录证明了什么、没证明什么。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "双套件门控：你的 starter 全绿，同时你要证明自己会审查证据而不只是产出绿灯。"
  - title: "三个皮肤都要端到端跑"
    body: "对每个 scenario 文件夹运行 `run_scenario`——csv、json 输入和错误路径都过一遍。然后拿契约审你的 diff：任何函数做得比它的契约行多，就是范围蔓延。"
  - title: "怀疑者的部分"
    body: "套件绿了但你解释不了某个 diff，那才是真正的失败。认领前先重读改动——认领码声明的是你验证过，不只是测试跑过。"
---

# 第 4 课：像工程师一样验证，像怀疑者一样审查

## 目标

完成完整的证据闭环——双向验证、三个皮肤各跑一次端到端、审查最终
diff 是否越界与有副作用——并写出三行验证记录，说明证明了什么、没
证明什么。

## 为什么要有这一课

"测试通过"是验证的起点而不是终点。测试套件锚定了九个行为，但它不会
告诉你：Agent 是否改了不该改的文件、工具在真实数据上会不会留下
垃圾、报表数字在**你的**领域里对不对。这部分判断永远属于人。

## 课程内容

按顺序跑完整个闭环：

```bash
python verify.py starter          # 你完成的实现：9/9
python verify.py solution         # 已审核参考实现：9/9
git diff --stat                   # （或等价命令）到底改了什么？
```

然后像真实用户一样，每个皮肤各跑一次（每次会在对应 scenario 文件夹
里写 `report.json`——确认 `.gitignore` 已处理，然后检查输出）：

```bash
python starter/report_tool.py scenario/excel-report
python starter/report_tool.py scenario/data-monitor
python starter/report_tool.py scenario/api-tool
```

对每个 `report.json` 核对三件事：`total = valid + invalid`；每条
`errors[i].reason` 都能对应到数据文件里真实存在的行；抽一个分组总计
手动重算。

接下来是怀疑者的 diff 审查。对 Agent 超出契约线的每一处改动问：是哪条
测试逼出来的？答案是"没有"，就是范围蔓延——回滚它并重跑套件。再检查
测试看不见的副作用：`scenario/` 之外有没有新建文件、有没有网络调用
（应当为零）、空数据文件会发生什么（试试看）。

## 练习

写下验证记录。三行，诚实：

```
已验证：<运行的命令、日期、结果>
未验证：<套件覆盖不到的部分——例如真实导出文件的编码、超大文件>
已知局限：<什么会让它失效——例如源系统改了表结构>
```

对照课程根目录的 `REVIEW.md`——同样的纪律，维护者版本。

## 检查点

以下全部达成即通过：三个皮肤干净运行；手动核算的分组总计一致；diff
审查发现（并回滚）了至少一处无强制理由的改动——或者你能论证每处改动
都有测试逼着；三行记录已经写下。

## 预期证据

验证记录、`git diff --stat` 输出、一个手动核算的分组总计。这就是真实
变更中你会附上的交付物。
