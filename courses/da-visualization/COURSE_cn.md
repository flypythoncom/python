---
id: course-da-visualization
type: course
title: 用 Agent 做数据可视化
summary: 挑战课程——把干净的销售数据变成三张有规格的图和一份 summary.json，其中数字会与数据集校验。图必须由数据生成，不许硬编码。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-da-visualization
  name_en: Visualization Challenger
  name_zh: 可视化挑战者
  requires: 全部五个检查点认领通过（L01–L05）
course_id: course-da-visualization
---

# 用 Agent 做数据可视化

> 速览：挑战课程——你解题，Agent 是工具。把
> `scenario/sales-clean/sales_daily.csv` 变成三张符合规格的 PNG 图和
> 一份 `summary.json`。验证检查文件存在、是合法 PNG、数字与数据集
> 一致——它**不**评价美观，展示产出时请如实说明这一点。

## 你要做出的东西

一个 matplotlib 脚本，产出 `out/revenue_by_region.png`、
`out/daily_revenue.png`、`out/revenue_histogram.png` 和
`out/summary.json`——“这是我的图”这句话中可机器核查的那一半。

## 环境

```bash
cd courses/da-visualization
uv sync            # pandas + matplotlib（或 pip install -r requirements.txt）
```

## 挑战（检查点）

| # | 挑战 | 判卷方式 |
| --- | --- | --- |
| L01 | 图是证据的包装——每张图在声称什么？ | 自我声明 |
| L02 | 先写规格——写下每张图必须呈现的数字 | 自我声明 |
| L03 | 三张图与摘要——实现契约 | 客观（starter 套件） |
| L04 | 数字与图一致——两套件全绿 | 客观（双套件） |
| L05 | 诚实边界——验证看不到什么 | 自我声明 |

## 徽章契约

- 徽章：**可视化挑战者**（badge id `da-visualization`）——五个检查点
  全部认领。
- 挑战：L01–L05 各 10 分；flypython.com 上 +50 课程徽章奖励分。
- 证据：`python verify.py`——L03/L04 客观判卷，L01/L02/L05
  自报。自我报告的证据，绝非证书。

## 本课程不覆盖的内容

图表设计、仪表盘、seaborn/plotly、交互图。只用 Agg 后端是刻意的：
图是证据产物，不是 UI。

## 文件夹地图

```
COURSE.md / COURSE_cn.md   本文件（EN / 中文）
lessons/L01.md … L05.md    挑战说明（每课有 _cn.md 配对）
scenario/sales-clean/      sales_daily.csv（干净输入）
TASK.md / TASK_cn.md       契约
starter/charts.py          未完成实现
solution/charts.py         审核过的解答
tests/test_charts.py       契约套件（只读）
verify.py                  客观通过/失败 + 认领码
requirements.txt           锁定的 pandas + matplotlib
REVIEW.md                  维护者走查记录
```

代码 MIT 许可；文字 CC BY 4.0（见仓库 `LICENSE`）。
