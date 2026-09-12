# FlyPython 仓库 0.0.3 更新计划

版本：0.0.3（规划稿）
更新：2026-09-11

历史边界说明：本文记录 0.0.3 的内容模型和实施计划。当前挑战叙事、认领码、
徽章与公开学习路线已经由 0.0.4 计划接续；网站当前固定到后续状态提交
`920f790`。本文中的
“Agent 授课”和未勾选 TODO 不代表当前状态。本文件按所有者决策以中文保留。
关联：flypython.com `docs/product-and-growth-plan-0.0.3.md`

状态：规划文档，不代表已实现。本计划遵守 `AGENTS.md` 的仓库边界：本仓库
负责已审核内容、可运行证据与稳定 JSON 契约；网站负责展示与转化。
所有新内容中英文同步产出。

## 1. 网站 0.0.3 方向对本仓库的要求

网站规划把"agent 自授课课程"定为主产品线、新增 Project Radar 周报，
并把本仓库（4.1k star）作为顶层流量渠道。这需要仓库侧五项能力：

1. `courses/` 内容类型：可被 agent 授课、带客观验证的文件夹。
2. 结构化的 Project Radar 数据源（每项目一 YAML，不再用 README 表）。
3. 只产出候选、不生成描述的发现工具。
4. 契约更新：content-manifest、catalog 导出、schema、llms 文件。
5. 按 `docs/REPO_TO_WEBSITE.md` 对 README/README_cn 做导流改造。

## 2. `courses/` 规范（新增顶层目录）

每门课一个文件夹，尽可能由现有 guides/playbooks/examples 装配：

```
courses/<slug>/
  COURSE.md            # 元信息 + 授课契约（agent 首先读取）：
                       # 受众、前提、工具与版本、课程顺序、授课风格规则、
                       # 何时停止、如何使用 verify.py、本课不覆盖什么
  lessons/
    L01.md  L01_cn.md  # 目标、练习、检查点、预期证据
    ...
  scenario/            # 场景皮数据文件（同一技能、贴近领域）
  TASK.md              # 任务契约（复用 templates/TASK_CONTRACT.md）
  starter/  solution/  # 可运行的一对
  verify.py            # 客观通过/失败；尽量只用标准库
  REVIEW.md            # 维护者跟课记录：日期、工具、版本、授课漂移观察
```

规则（将写入 `AGENTS.md` 编辑标准）：

- agent 依据这些文件授课；不依赖网站、账户或视频。`verify.py` 是结业证据。
- 双语：每个英文 lesson 必须有同提交的 `*_cn.md`；双语齐备才算完成。
- `COURSE.md` 必须注明跟课所用的具体工具与版本（如 "Claude Code 2.x"）
  及 `reviewed_on`；工具大版本发布触发复查。
- REVIEW.md 人工跟课在可行时录屏：录像同时作为网站演示视频素材
  （见网站规划 §4.5）。
- 不虚构成果、薪资或"保证学会"式承诺。

首批（装配而非新写）：C1 Claude Code × Python 实战（旗舰，3 个场景皮：
Excel/报表自动化、数据监控、API 小工具）；C2 Codex CLI；C3 AGENTS.md
一份事实源；C4 AI 生成代码的验证与交付；C5 用 MCP 给 agent 接工具。
见网站规划 §2.2。

## 3. Project Radar 数据模型

把 `catalog/projects/README.md` 的表格改为每项目一 YAML（与
`catalog/resources/` 同一套创作模型）：

```yaml
id: marimo
repo: marimo-team/marimo
url: https://github.com/marimo-team/marimo
category: notebooks          # 受控列表，有意扩展
status: rising               # new|rising|stable|major-update|experimental|archived
first_seen: 2026-09-02
reviewed_on: 2026-09-02
license: Apache-2.0
evidence:
  last_release: "…"
  release_cadence: "…"
  maintenance: "…"
ai_familiarity: low          # low|medium|high：主流模型训练数据是否覆盖
                             # （AI 时代的差异化字段）
alternatives: [jupyter, quarto]
when_not_to_use: "…"
rationale: "…"               # 人工撰写，遵守策展政策
risk: "…"
```

- `tools/render_readmes.py` 从 YAML 重新生成 Radar 表（沿用 catalog 索引的
  生成块约定）。
- 新增确定性导出 `radar.json` + `schema/radar-v1.schema.json`，不扩
  `catalog-v1`（它已被消费方固定）。同样按版本管理；网站消费方固定完整
  commit。
- 迁移现有 7 条作为种子集。

## 4. `tools/radar_scan.py`（只做候选发现）

- 输入：GitHub Search API（近 30 天 `language:Python` star 增速）、
  catalog 内项目的 PyPI 发布、HN/r/Python 高票帖。
- 输出：`catalog/projects/candidates.json`——repo 地址、star、最近发布、
  license、首次发现日期。**不写描述、不定状态。** 理由/风险/状态由人工
  撰写与选择，遵守 `AGENTS.md` 与 `CURATION_POLICY.md`。
- 只读、限速、不触达私有端点（与 `check_links.py` 同一约束）。

## 5. 契约与工具更新

- `schema/content-manifest-v1.schema.json`：`type` 增加 `"course"`
  （schema 变更须与 manifest 重新生成、网站 pin 更新在同一次刻意操作中完成）。
- `tools/build_content_manifest.py`：像 guides/playbooks 一样遍历
  `courses/`；每个语言文件各算 sha256。
- 新增 `tools/verify_courses.py`（对照 `verify_examples.py`）：检查文件夹
  契约——COURSE.md 存在、EN/CN lesson 成对、verify.py 对 starter 预期失败、
  对 solution 预期通过。
- `llms.txt` / `llms-full.txt`：增加 courses 与 radar 区块，深链到课程
  文件夹与 `radar.json`。
- `docs/CURATION_POLICY.md`：scope 扩展至课程与 radar 条目；写清
  `ai_familiarity` 分级规则。
- `.github/ISSUE_TEMPLATE/`：新增 `course-feedback.yml`（报告授课漂移/
  课节不清/verify 不符），与 project-proposal 并列。
- GitHub 维护项：仓库描述与 topics 加关键词；发布第一个带版本号的
  Release（让 watcher 收到通知，配合网站内容节奏）。

## 6. 导流改造（按 `docs/REPO_TO_WEBSITE.md`）

- README/README_cn 顶部横幅 → `https://flypython.com/from-github`
  （只有该路由上线并验证后才切换；之前链根域，遵守该文档自己的规则）。
- 每个 guide/playbook/example 文末一条情境化链接到对应站内页——延续当前
  任务，不做通用横幅。
- 仓库描述按新定位改写（"AI writes Python; we make it verifiable and
  deliverable"，最终措辞实施时定）。

## 7. 执行顺序

1. `courses/` 规范 + `verify_courses.py` + C1 文件夹（EN+CN）→ manifest/
   schema 更新同一次完成。
2. Radar YAML 迁移 + `radar.json` 导出 + schema + README 渲染。
3. `radar_scan.py` + 第一批候选。
4. llms 文件、策展政策、issue 模板、仓库描述/topics。
5. `/from-github` 线上验证后做 README 导流改造。
6. 首个课程落地时开始 Releases/tagging 节奏。

## 8. TODO（编号续接网站规划；全部未验收）

- [ ] FP-325 `courses/` 规范写入 `AGENTS.md`；COURSE.md 授课契约经评审。
- [ ] FP-326 C1 课程文件夹完成（3 个场景皮、verify.py 双向、EN+CN、
  真实跟课的 REVIEW.md）。
- [ ] FP-327 manifest `type: "course"` + schema + `build_content_manifest.py`
  遍历；网站 pin 更新同一次刻意完成（FP-224 规则）。
- [ ] FP-328 `verify_courses.py` 进入验证工作流与 Makefile。
- [ ] FP-329 `catalog/projects/` 迁为 per-project YAML（迁移 7 条种子）+
  `render_readmes.py` 重生成验证。
- [ ] FP-330 `radar.json` 导出 + `schema/radar-v1.schema.json` +
  `export_catalog.py` 扩展；`--check` 全绿。
- [ ] FP-331 `tools/radar_scan.py` 合入：限速与"不生成描述"有测试保证。
- [ ] FP-332 llms.txt / llms-full.txt 增加 courses+radar 区块；深链有效
  （pin 更新后网站侧 llms-links 测试保持绿）。
- [ ] FP-333 `CURATION_POLICY.md` scope + `ai_familiarity` 分级规则；
  `course-feedback.yml` issue 模板。
- [ ] FP-334 仓库描述/topics/关键词；第一个 GitHub Release。
- [ ] FP-335 README/README_cn 横幅 + 各文档情境化文末链接，以线上
  `/from-github` 验证为前置。
- [ ] FP-344 双许可 LICENSE 就位（MIT 代码 / CC BY 4.0 内容，两仓库同）——
  课程文件夹分发与 FP-326 的前置。
- [ ] FP-350 校验器与 schema 追上政策：`validate_catalog.py` 与
  `catalog-v1`/`radar-v1` 支持 Radar 生命周期状态与 `ai_familiarity`；
  manifest schema 增加 `type: "course"`；首个 Release（FP-334）时把
  CHANGELOG `[Unreleased]` 切入 `0.1.0` 段。

## 9. 非目标与风险

- 本仓库仍是内容/证据源：不做网站功能、不放付费内容、不接分析、
  密钥不入库。
- 课程质量风险：agent 会偏离 COURSE.md——用 verify.py + 有记录的人工
  跟课（REVIEW.md）兜底，不用承诺兜底。
- Radar 产能风险：候选很便宜，审核条目很贵——人工审核是有意保留的
  瓶颈，不能省。
- Pin 纪律：每次 schema/manifest 变更都搭配一次刻意的网站 pin 更新；
  永不依赖移动分支。
