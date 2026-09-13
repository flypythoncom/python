---
id: course-claude-code-l03
type: course
title: "第 3 课：按测试驱动一次有边界的变更"
summary: 让 Agent 在契约约束下修改 starter——最小变更、不新增依赖、一次一组测试从红到绿。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "门控是 `python verify.py starter`——九个测试在你的 starter 上全绿。一次只推一组失败：先 `load_records`（csv/json/ValueError），再 `build_report`，再 `write_report`，最后 `main`。"
  - title: "套件真正断言的坑"
    body: "布尔值不是数字——`isinstance(True, int)` 为 True，要显式排除。分组总计保留两位小数。`total = valid + invalid` 在全部行都非法时也必须成立。"
  - title: "原子写就是原子写"
    body: "`write_report` 必须用同级临时文件加 `os.replace`，成功时不能留下 `.tmp`——套件检查的是文件系统，不是你的意图。还红就直接跑 unittest 看失败名。"
---

# 第 3 课：按测试驱动一次有边界的变更

## 目标

starter 通过一系列有边界的变更通过全部九个测试，并且在不先看
solution 的前提下，你能解释 Agent 产出的每一个 diff。

## 为什么要有这一课

这是最容易被跳过、也最练真功夫的一课。看 Agent 用一次巨型重写让
七个失败测试全部通过，你什么都学不到；监督七个小 diff、每个都锚定
一条契约线，你学到的是如何让 AI 写的代码仍然属于你。

## 课程内容

对 Agent 说："**按 TASK.md 修改 starter/report_tool.py。一次只处理一组
失败测试：先 JSON 加载，再校验隔离，再舍入，再原子写入，最后端到端。
每完成一组就运行测试套件，给我看 diff，再继续。**"

守住契约的边界：

- 只有 `starter/report_tool.py` 可以变。diff 若触碰 `tests/`、
  `solution/` 或 `scenario/`，停下来问为什么。
- 不引入标准库之外的新依赖——也不引入当前变更用不到的 import。
- 每次变更只应指向一条契约线。拒绝顺手重构（"既然改到这里我把……
  也重命名了"）。
- Agent 想改测试？答案是不。测试就是契约；动的是代码。

每组之后运行套件：

```bash
PYTHONPATH=starter python -m unittest discover -s tests -v
```

失败数应逐组下降：7 → 5 → 4 → 3 → 2 → 0。

## 练习

最后一组自己做。当只剩端到端测试时，亲手写下 `run_scenario`/`main`
的修复（它们很小），然后跑完整套件。看懂 Agent 的 diff 是学习；亲手
写最后十行是内化。

## 检查点

```bash
python verify.py starter --expect-failure   # 此时应当报"预期失败但没有失败"：starter 已经通过
python verify.py starter                    # 必须通过全部九个测试
```

第一条命令失败是好消息——说明 starter 不再处于"正确的未完成"状态。
然后回答：哪个变更最小？哪个你自己会做过头？

## 预期证据

从 7 个失败降到 0 的测试输出记录，加上各步 diff。只有当你的 starter
通过之后才允许打开 `solution/`——对比两种实现，记下已审核方案做到了
而你没有做到的一件事。
