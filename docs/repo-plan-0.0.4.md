# FlyPython 仓库 0.0.4 更新计划

版本：0.0.4（规划草稿，第 3 版）
更新日期：2026-09-12（第 3 版——挑战模型定稿 + A/B 阶段拆分）
关联：flypython.com `docs/product-and-growth-plan-0.0.4.md`

状态：除 FP-414 与真实 Agent 可解性试跑外，本计划已实现；网站当前固定
到 `920f790`（阶段 A + 数据分析模块 live 状态）。`AGENTS.md` 的仓库边界不变：
本仓库拥有经审核的内容、可运行的证据与稳定的 JSON 契约；网站拥有呈现、
账号体系与转化。所有新内容中英同一次变更交付。

修订说明：0.0.4 首稿提出纯本地的进度产物；第 2 版转向账号体系与服务端
进度。第 3 版按所有者决策定稿产品形态：**PentesterLab 式挑战产品——
学员亲手解题，AI Agent 是解题工具而非授课者**；`COURSE.md` 授课契约
保留为可选「引导模式」。网站侧实施拆为 0.0.4a 内容引擎 / 0.0.4b 平台
机制（账号与排行榜门控于目录深度 ≥15–20 挑战）；**本仓库全部工作项
属于阶段 A**——认领码即 flag 契约，先服务本地挑战循环，后为网站服务端
记录所用。

## 1. 主题：面向服务端进度记录的检查点认领码

学习者在检查点套件通过后，把 `verify.py` 打印的认领码输入网站，网站
即记录进度。本仓库拥有让这些码可信且稳定的一切：

- 认领码由 `(course_id, checkpoint_id, evidence)` 确定性推导，其中
  evidence 是客观套件的结果——相同输入在任何机器、离线状态下都产生
  相同的码。
- 认领码短小、可人工输入（如 base32 的 8 个字符）。
- 认领码可抽查、并非防篡改；所有表述统一为"自我报告的证据"，绝不
  使用认证式措辞。
- 课程工具中无网络访问、无账号、无遥测——登录后的一切都归网站侧。
- 挑战可解性是上线门槛：每个挑战必须用目标 Agent（Claude Code /
  Codex）实测一遍——既不能被秒解到无趣，也不能被卡住无解；实测
  记录进 `REVIEW.md`。

## 2. 工作项

### FP-411 检查点认领码（`verify.py`）

- 新子命令：`python verify.py progress` 按检查点打印其 id、名称、通过
  状态（来自客观套件），以及——通过时——认领码。
- 认领码跨运行、跨平台稳定；推导方式（含每课程盐值常量）在课程契约
  中文档化，并像代码一样接受审核。
- 仅用标准库；输出确定；可安全重复运行。

### FP-412 挑战叙事（COURSE.md + 课程）

- 叙事重心从"Agent 授课"改为"学员解题"：课程标注为挑战（"挑战 01：
  复现故障"），`TASK.md` + 检查点 + `verify.py` 即 exercise+flag
  骨架；`COURSE.md` 授课契约保留为可选「引导模式」入口。
- COURSE.md 增加徽章契约章节：课程徽章名（如"Verified Report Tool"）、
  五个检查点挑战、"自我报告证据"的诚实表述——并指向网站的记录流程。
- 检查点小节写明其满足的徽章要求与认领步骤。
- 中英同一次提交；按 manifest 规则更新 `reviewed_on` 与
  `content_version`。

### FP-413 徽章契约对齐

- 每门课程的 `COURSE.md` 以结构化 front matter/字段声明徽章元数据
  （徽章 id、展示名中英、要求文本），让网站从课程数据渲染徽章地图与
  服务端记录——网站侧不手抄任何徽章定义。

### FP-414 Agent skill 打包（评估）

- 评估把课程摄取发布为 SKILL.md 兼容的 skill（OpenMAIC / Codex 工作
  台），遵循仓库模板约定。人工撰写；先留下真实试点记录再给建议。

### FP-415 `verify_courses.py` 扩展

- 扩展课程契约验证器：每个检查点都暴露认领码；认领码确定性成立
  （相同输入在两次运行、两个平台上产生相同码）；格式经过校验；
  进度子命令纳入 CI 演练。

## 3. 首批学习路线的仓库侧：「用 Agent 做数据分析」

网站 0.0.4 计划 §5 定义了首条学习路线（课程序列 + 项目挑战 + 徽章 +
积分）。本仓库承担其中的内容与证据层：

### FP-416 DA 路线三门新课

- `courses/da-eda/`：探索性数据分析（pandas）——读真实数据集、描述
  统计、缺失值与分布；挑战产出 `results.json`，`verify.py` 校验数字
  （容差比较）。
- `courses/da-visualization/`：数据可视化（matplotlib）——按规格产出
  图表；挑战校验"图表存在 + 底层数据正确"，不评审美。
- `courses/da-report/`：从分析到报告——结构化 Markdown/JSON 报告生成
  器；挑战校验"报告结构 + 数字与 results.json 一致"，不评文笔。
- 每门课遵循课程契约：COURSE.md 教学契约、中英课程对、TASK 契约、
  starter/solution、`verify.py` 双向验证、REVIEW 记录。
- 首批非标准库依赖（pandas、matplotlib）经 uv 管理，装环境是第 1 课
  内容；依赖锁定进课程文件夹。

### FP-417 路线契约与综合项目

- 新增 `paths/data-analysis/`：`PATH.md` 路线清单（模块序列、前置、
  各课程徽章、路线徽章「数据分析 Agent」、积分表）+ 综合项目挑战
  （捆绑公开数据集 + 带容差的数字答案 + `verify.py`）。
- 路线清单是结构化数据（面向网站 FP-409 渲染），网站侧不手抄定义。
- 网站侧对应项：FP-409（路线结构/页面）与 FP-410（首条路线挂载）。

### FP-418 基础路线组装（「Agent 工具基础」）

- 新建入门模块 M0：认识 AI 编程 Agent——工具生态总览（Claude Code /
  Codex / Cursor）、安装与第一次对话；中英双语。
- 新建路线挑战：同一任务在 Claude Code 与 Codex 下各完成一次并双重
  验证。
- `paths/foundation/` 路线契约（PATH.md：模块序列、徽章「Agent
  使用者」、积分表），复用已上线的 C1–C4 作为模块 1–4。
- 网站侧对应项：FP-409（路线结构/页面）与 FP-410（路线挂载）。
- 完整路线体系见 flypython.com `docs/LEARNING-PATHS.md`。

## 4. Non-goals

本仓库无账号、无服务端判题、课程工具无网络访问、无认证式措辞、无
网站内容第二副本。反作弊设计刻意保持轻量（可抽查的码）；重反作弊是
网站侧的关切，不在本仓库范围。

## 5. TODO 与当前状态

- [x] FP-411 全部五门课程的认领码子命令，推导方式已文档化。（本地
  2026-09-12：`verify.py progress` 上线——l03/l04 由测试套件客观判定、
  l01/l02/l05 自报；认领码 8 位 base32，确定性两次运行一致）
- [x] FP-412 徽章契约 + 挑战叙事，中英一次变更交付。（本地
  2026-09-12：五门课程 COURSE.md/COURSE_cn.md 增加徽章契约章节并升
  content_version 2，manifest 已重生成）
- [x] FP-413 供网站渲染的结构化徽章元数据。（本地 2026-09-12：全部
  8 门课 `COURSE.md`/`COURSE_cn.md` frontmatter 增加 `badge`（id、
  name_en、name_zh、requires）与 `course_id`）
- [ ] FP-414 SKILL.md 打包评估，附书面记录。
- [x] FP-415 `verify_courses.py` 认领码覆盖进 CI。（本地 2026-09-12：
  进度契约检查——双运行确定性、JSON 结构、5 检查点、码格式——已入
  验证器并随 `make check`/validate.yml 执行）
- [x] FP-416 DA 路线三门新课（`da-eda`、`da-visualization`、
      `da-report`），中英 + verify.py 双向验证。（本地 2026-09-12：
      首批非标准库课程，依赖经 `requirements.txt` 锁定——pandas
      2.3.3 / matplotlib 3.10.9；da-eda 12 测试、da-visualization
      5 测试、da-report 6 测试；Agent 可解性实测仍待录 REVIEW.md）
- [x] FP-417 `paths/data-analysis/` 路线契约 + 综合项目挑战。（本地
  2026-09-12：`path.json` + `capstone/`——303 行脏数据集、
  `verify.py` 真值校验（容差 0.01）、综合项目认领码）
- [x] FP-418 基础路线 M0 入门模块 + 路线挑战 + `paths/foundation/`
      路线契约。（本地 2026-09-12：`path.json` + `modules/` 双语
      模块文档，复用 C1–C4 为模块 1–4）
- [x] 配套契约：manifest `type:"path"` + schema 枚举、`paths/**/*.md`
      入 CONTENT_GLOBS、`tools/verify_paths.py` 入 `make check` 与
      validate.yml、CURATION_POLICY scope 加学习路线、README 双语
      叙事改为挑战平台、requirements-dev 锁定 DA 依赖。

## 6. 执行顺序（本仓库全部为阶段 A 内容引擎）

1. FP-411 + FP-412 + FP-415 一次变更完成（码、挑战叙事、检查器）；
   `COURSE.md` 降级为可选引导模式随 FP-412 落地。
2. FP-413 徽章元数据（frontmatter 声明，供网站渲染消费）。
3. FP-418 基础路线组装（大部分课程已上线，工作量最小、最先可见）。
4. FP-416 三门新课 + FP-417 路线契约（内容层，可与第 1 步并行起步，
   上线依赖网站 FP-409/410——路线页公开可收录，不依赖账号）。
5. 记录一次真实外部工具运行后再做 FP-414。
6. 网站阶段 B（账号/进度/排行榜）门控于目录深度 ≥15–20 个挑战，
   本仓库不启动任何配合项直至达标。

## 7. 自 0.0.3 结转（未完成）

- FP-326 备注：五次 Agent 实机授课记录仍待写入各课程 `REVIEW.md`
  （属于发布证据，不是内容阻塞项）。
- FP-327 发布步骤：网站 pin 在一次刻意变更中固定到本仓库发布 SHA。
- FP-334 仓库描述/话题 + 首个 GitHub Release；该 Release 时将
  CHANGELOG `[Unreleased]` 切为正式版本小节。

## 8. 实施规范（挑战模型改造细节）

### 8.1 课程文件夹改造（FP-411/412/413）

现有文件夹骨架不变，叙事重心改到挑战：

```
courses/<slug>/
  TASK.md / TASK_cn.md   ← 挑战入口：题目陈述、约束、通过条件
  COURSE.md              ← 可选「引导模式」契约 + 徽章契约章节
  lessons/L01*.md        ← 小节重标为 "Challenge 01: ..."；检查点
                           写明满足的徽章要求与认领步骤
  verify.py              ← 新增 `progress` 子命令
  REVIEW.md              ← 追加 Agent 可解性实测记录
```

**认领码推导**（`python verify.py progress`）：

- 每检查点输出：`id / 名称 / 通过状态 / 认领码`（通过时）
- `code = base32(sha256(salt + course_id + checkpoint_id + evidence_hash))`
  取前 8 字符——纯标准库、离线、跨平台确定
- `salt` 为每课程常量，与 `course_id` 一起声明在 `COURSE.md`
  frontmatter；推导方式在课程契约中文档化并接受代码级审核
- 防手误不防作弊；所有表述为"自我报告的证据"

**徽章元数据**（`COURSE.md` frontmatter，供网站 FP-407/409 渲染）：

```yaml
badge:
  id: verified-report-tool
  name_en: Verified Report Tool
  name_zh: 验证过的报表工具
  requires: 全部五个检查点认领通过
salt: <per-course constant>
course_id: hands-on-python-with-claude-code
```

### 8.2 路线层 `paths/`（FP-417/418）

```
paths/
  foundation/PATH.md       入门路线：M0 + 复用 C1–C4；徽章「Agent 使用者」
  data-analysis/PATH.md    DA 路线：C1 模块 0–1 + da-* 三门 + 综合项目；
                           徽章「数据分析 Agent」；积分表
  data-analysis/capstone/  综合项目挑战：捆绑公开数据集 + 容差数字校验
                           + verify.py
```

`PATH.md` 为结构化路线契约（模块序列、前置、各课程徽章、路线徽章、
积分表：检查点 10 分 / 课程 BOSS 50 分 / 综合项目 200 分），网站
FP-409 渲染消费，网站侧不手抄定义。

### 8.3 契约与文档跟进

- `content-manifest.json`：`type` 增加 `"path"`，`paths/**` 入 manifest；
  schema 与 `verify_courses.py` 同一次变更跟上
- `CURATION_POLICY.md`：scope 补学习路线
- `README.md` / `README_cn.md`：首屏叙事从资源目录调整为挑战平台
- `REVIEW.md`：每门课追加 Agent 可解性实测（不被秒解、不被卡死）

### 8.4 落地顺序（与 §6 对应）

1. **C1 试点**（`hands-on-python-with-claude-code`）：progress 子命令 +
   挑战叙事 + 徽章 frontmatter + `verify_courses.py` 扩展，一次变更
2. 试点验收后**横推 C2–C5**
3. `paths/foundation/`（复用现有课，最快可见）
4. `da-eda` / `da-visualization` / `da-report` 新课 + `paths/data-analysis/`
   + M0 入门模块
