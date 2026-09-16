---
id: course-da-report
type: course
title: 用 Agent 从分析到报告
summary: 挑战课程——把经过验证的 EDA 摘要变成结构化报告（report.json + report.md），其中每个数字都可回溯到输入。验证检查结构与数字一致性，不评价文笔。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-da-report
  name_en: Report Challenger
  name_zh: 分析报告挑战者
  requires: 全部五个检查点认领通过（L01–L05）
course_id: course-da-report
---

# 用 Agent 从分析到报告

> 速览：挑战课程——把 `scenario/analysis-pack/results.json` 变成
> `out/report.json` + `out/report.md`。契约：报告里每个数字都必须
> 原样回溯到输入。验证检查结构与数字一致性，不评价文笔。

## 你要做出的东西

一个报告生成器：载入已验证的输入 → 构建结构化报告 dict → 渲染
Markdown → 写出两份产物。结构化 JSON 是可审计层，Markdown 给人看。

## 环境

```bash
cd courses/da-report
# 仅使用标准库——无需安装任何依赖。
```

## 挑战（检查点）

| # | 挑战 | 判卷方式 |
| --- | --- | --- |
| L01 | 报告是与读者的契约 | 自我声明 |
| L02 | 先结构，后文字 | 自我声明 |
| L03 | 构建并渲染报告 | 客观（starter 套件） |
| L04 | 数字可回溯到输入 | 客观（双套件） |
| L05 | 报告验证看不到的东西 | 自我声明 |

## 徽章契约

- 徽章：**分析报告挑战者**（badge id `da-report`）——五个检查点
  全部认领。
- 挑战：L01–L05 各 10 分；flypython.com 上 +50 课程徽章奖励分。
- 证据：`python verify.py`——L03/L04 客观判卷，
  L01/L02/L05 自报。自我报告的证据，绝非证书。

## 本课程不覆盖的内容

模板引擎（Jinja）、PDF 导出、排版样式、文字质量。套件验证的是结构
与数字——写得好不好仍是你的事。

## 文件夹地图

```
COURSE.md / COURSE_cn.md   本文件（EN / 中文）
lessons/L01.md … L05.md    挑战说明（每课有 _cn.md 配对）
scenario/analysis-pack/    results.json（已验证输入）
TASK.md / TASK_cn.md       契约
starter/report.py          未完成实现
solution/report.py         审核过的解答
tests/test_report.py       契约套件（只读）
verify.py                  客观通过/失败 + 认领码
REVIEW.md                  维护者走查记录
```

代码 MIT 许可；文字 CC BY 4.0（见仓库 `LICENSE`）。
