---
id: course-da-eda-l04
type: course
title: "挑战 04：核对真值"
summary: "套件断言精确数字——142 进 137 净、营收 33347.89、品类第一 Books；看着合理但不同即失败。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
hints:
  - title: "这个检查点考什么"
    body: "双套件对真值：142 行进、137 行净、2 条重复、2 条坏金额、1 条坏日期、营收 33347.89、品类第一 Books。"
  - title: "合理不等于正确"
    body: "产出『看着合理但不同』的数字就是失败——这份数据只有一个正确答案。对不上就找哪一步清洗跑偏了。"
  - title: "完成标准"
    body: "你的 `results.json` 与真值逐数字一致，且每个数字都能指回产生它的清洗步骤。"
---

# 挑战 04：核对真值

**判卷：** 客观——双套件 · **积分：** 10

测试套件断言的是精确数字：输入 142 行、清洗后 137 行、2 个重复、
2 个坏金额、1 个坏日期、总收入 33347.89、最高品类 Books。如果你的
实现"通过"的方式是产出不同但看似合理的数字，那就是没通过——这份
数据集只有一个正确答案。

跑 `python verify.py starter --expect-failure`：现在必须退出非零
（starter 已不处于未完成状态）。再跑 `python verify.py solution`——
全绿。

**检查点：** 两道门禁都过。用 `python verify.py progress` 取客观
认领码。
