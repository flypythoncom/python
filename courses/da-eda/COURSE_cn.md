---
id: course-da-eda
type: course
title: 用 Agent 做探索性数据分析
summary: 挑战式课程——让你的 Agent 处理一份脏的商店导出数据，产出一份经过真值校验的 EDA 摘要（results.json）。目录中第一门非标准库课程；pandas 由 uv 管理。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-da-eda
  name_en: EDA Challenger
  name_zh: 探索分析挑战者
  requires: 全部五个检查点认领通过（L01–L05）
course_id: course-da-eda
---

# 用 Agent 做探索性数据分析

> 速览：这是一门**挑战课程**——解题的是你，Agent 是手里的工具。让它
> 处理 `scenario/shop-export/transactions.csv`（142 行脏数据），实现
> `starter/eda.py` 里的契约，最终产出一份 `results.json`，其中每个
> 数字都会被客观真值校验。可选引导模式：`COURSE.md` + `lessons/` 仍
> 可作为 Agent 授课路径，想要引导而不是挑战时用它。

## 你要做出的东西

一个 pandas 脚本：读入一份真实风格的脏交易导出，清洗（重复行、不可
解析金额、坏日期），写出经过验证的摘要：清洗行数、总收入、分地区
收入、最高收入品类、日期范围。

## 环境——第 0 课就是装环境

这是目录里第一门离开标准库的课程：

```bash
cd courses/da-eda
uv sync            # 或：pip install -r requirements.txt
```

`verify.py` 会检查 pandas，缺失时打印这条提示。

## 挑战（检查点）

| # | 挑战 | 判卷方式 |
| --- | --- | --- |
| L01 | 脏数据长什么样——写代码前先给 CSV 做画像 | 自我声明 |
| L02 | 先定答案——写下期望的 results.json 结构 | 自我声明 |
| L03 | 清洗与统计——实现 `clean_transactions` + `summarize` | 客观（starter 套件） |
| L04 | 核对真值——两套件全绿 | 客观（双套件） |
| L05 | 换成你自己的数据——拿一份真实导出来跑 | 自我声明 |

## 徽章契约

- 徽章：**探索分析挑战者**（badge id `da-eda`）——五个检查点全部
  认领后获得。
- 挑战：L01–L05 各 10 分；五个全部在 flypython.com 认领后 +50 课程
  徽章奖励分。
- 证据：`python verify.py progress`——L03/L04 由套件客观判卷，
  L01/L02/L05 为学习者自报。
- 提交：每个通过的检查点打印一个确定性认领码，在 flypython.com 上
  记入你的账号。自我报告的证据，绝非证书。

## 本课程不覆盖的内容

可视化（见 `da-visualization`）、报告（见 `da-report`）、统计理论、
SQL、notebook。数据集是合成的，但数据质量问题和你会在真实导出中
遇到的一样。

## 文件夹地图

```
COURSE.md / COURSE_cn.md   本文件（EN / 中文）
lessons/L01.md … L05.md    挑战说明（每课有 _cn.md 配对）
scenario/shop-export/      transactions.csv（脏输入数据）
TASK.md / TASK_cn.md       代码必须满足的契约
starter/eda.py             故意未完成的实现
solution/eda.py            审核过的解答
tests/test_eda.py          契约测试套件（只读）
verify.py                  客观通过/失败 + 认领码
requirements.txt           锁定的 pandas 依赖
REVIEW.md                  维护者走查记录
```

## 证据与许可

审核过的内容：`REVIEW.md` 记录走查。代码 MIT 许可；课程文字
CC BY 4.0（见仓库 `LICENSE`）。
