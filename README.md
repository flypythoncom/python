# FlyPython: Learn to ship Python with AI coding agents

[![GitHub stars](https://img.shields.io/github/stars/flypythoncom/python?style=flat-square&label=stars)](https://github.com/flypythoncom/python/stargazers)
[![Validate](https://github.com/flypythoncom/python/actions/workflows/validate.yml/badge.svg)](https://github.com/flypythoncom/python/actions/workflows/validate.yml)
[![Website](https://img.shields.io/badge/Website-flypython.com-blue?style=flat-square)](https://flypython.com)

[English](README.md) · [中文](README_cn.md) · [🌐 Online Portal](https://flypython.com)

Real projects; your agent does the typing, `verify.py` decides when you're
done.

> **Challenge courses with objective verification.** Pick a folder from
> [`courses/`](courses/), solve the contract in `TASK.md` with your coding
> agent as the tool, and prove it with `verify.py` — which prints a claim
> code per checkpoint. Prefer a guided path? `COURSE.md` still runs an
> agent-taught mode, and [`paths/`](paths/README.md) sequences courses into badge
> routes. Continue on [flypython.com](https://flypython.com/).

<p align="center">
  <img src="assets/verify-demo.svg" width="720" alt="Terminal demo: a course verify.py checkpoint report. A reflection checkpoint prints its claim code after explicit --attest confirmation; unfinished tasks stay open.">
</p>

FlyPython is a practical, bilingual repository for writing good Python and
turning it into products people can rely on. It combines AI-coding methods,
task playbooks, runnable examples, reusable templates, and reviewed primary
sources for APIs, automation, agents, Skills, and MCP.

It is not a beginner link dump. The goal is to help you move from “the agent
wrote code” to “a user outcome is verified.” The repository owns the reviewed
source content and data; [flypython.com](https://flypython.com/) turns pinned
versions into a browsable learning experience.

**Current release:** `v0.1.1` — see [CHANGELOG.md](CHANGELOG.md); release and
delivery status is tracked in the
[repository-to-website operating model](docs/REPO_TO_WEBSITE.md).

## Start in three minutes

You need a coding agent that can run commands and reach the network
(Claude Code, the Codex app, Cursor, DeepSeek Harness, Kimi Code, or
ZCode — chat-only web AIs cannot run these courses). Install the
[FlyPython Skill](https://flypython.com/skills/flypython/SKILL.md) in
your agent, then paste this one sentence:

> Read https://flypython.com/skills/flypython/SKILL.md and start the FlyPython course `da-eda`.

The agent authorizes you with a one-time link (you never hand it a
password), fetches the course files itself — you download nothing — and
drives the challenges with you. New to driving an agent? Start with the
tool course for *your* agent: [Hands-on Python with Claude Code](courses/hands-on-python-with-claude-code/COURSE.md),
[Codex app](courses/hands-on-with-openai-codex/COURSE.md), [Cursor](courses/hands-on-with-cursor/COURSE.md),
[DeepSeek Harness](courses/hands-on-with-deepseek-harness/COURSE.md),
[Kimi Code](courses/hands-on-with-kimi-code/COURSE.md), or
[ZCode](courses/hands-on-with-zcode/COURSE.md).

Maintainers can still reproduce an example locally without any agent:

```bash
git clone https://github.com/flypythoncom/python.git
cd python
python examples/product-slug/verify.py starter --expect-failure
python examples/product-slug/verify.py solution
```

## Verify and record a course

In the course folder, run `python verify.py` after each change. It tests only
`starter/` and reports every checkpoint:

- `[open]` — the task is unfinished.
- `[passed]` — the tests pass and `verify.py` prints a claim code.
- `[pending]` — a reflection checkpoint: answer that lesson's questions, then
  run `python verify.py --attest l01` (repeat for each completed reflection)
  to get its `[attested]` code.

Submit only `[passed]` and `[attested]` codes through your agent or the
dashboard. `check --json` is the versioned v2 interface; `progress --json`
remains for older signed-receipt integrations.

## Choose what you need to accomplish

| Goal | Start here | What you will produce |
| --- | --- | --- |
| Learn by solving challenges | [Challenge courses](courses/) · [Learning paths](paths/README.md) | A verified project + checkpoint claim codes from `verify.py` |
| Write and change Python safely | [AI Coding workflow](guides/ai-coding/workflow.md) | A bounded change with explicit context and evidence |
| Turn Python into a reliable product | [Product quality guide](guides/python-engineering/product-quality.md) | A tested, observable, reversible product path |
| Finish a recurring engineering task | [Playbooks](playbooks/README.md) | A bug fix, API change, integration, dependency upgrade, or release |
| Practice instead of only reading | [Runnable examples](examples/README.md) | Local testable projects with failing starters and verified solutions |
| Give an agent better instructions | [Templates](templates/README.md) | Task contracts, plans, reviews, IDE rules, and verification records |
| Build agents, Skills, MCP, APIs, or automation | [Reviewed source catalog](catalog/README.md) | A primary-source path selected for your use case |
| Find current Python projects | [Project Radar review queue](catalog/projects/README.md) | An evidence-backed shortlist after maintainer review |

The working loop is simple: define the user outcome, inspect the real context,
make the smallest testable change, verify behavior, review side effects, and
record what remains unverified. AI accelerates the loop; it does not replace
engineering judgment.

Prefer a guided reading path and ongoing updates? Continue on
[flypython.com](https://flypython.com/). The repository remains the inspectable
source; the website helps you choose the next useful step.

## For AI Agents and LLMs

If you are an LLM agent or coding assistant (Cursor, Windsurf, Claude Code, Copilot, Perplexity):
- Ingest repository index: [`llms.txt`](llms.txt) or [`catalog.json`](catalog.json)
- Universal IDE rules template: [`templates/AGENT_RULES.example.md`](templates/AGENT_RULES.example.md)
- Machine-readable manifest: [`content-manifest.json`](content-manifest.json)
- Official web knowledge dump: `https://flypython.com/llms-full.txt`

## Reviewed source catalog

Four maintainer-reviewed learning paths cover foundations, web and APIs,
automation, and AI agents:

<!-- catalog-index:start -->
<!-- Generated by tools/render_readmes.py; edit catalog/ instead. -->
> **33 reviewed resources** · Catalog reviewed 2026-09-06 · 25 intermediate or advanced · Primary sources first

- [**Python foundations**](catalog/README.md#path-foundations) — Learn the language, environments, dependencies, typing, and tests that reliable Python work depends on. (8 resources)
- [**Web and APIs**](catalog/README.md#path-web-apis) — Build typed services and applications that connect Python logic to users and other systems. (7 resources)
- [**Automation**](catalog/README.md#path-automation) — Turn repeatable work into maintainable scripts, browser workflows, and data pipelines. (7 resources)
- [**AI agents**](catalog/README.md#path-ai-agents) — Learn tools, structured output, state, evaluation, and the safety boundaries of agent systems. (11 resources)

Full tables — why each source is included, its level, and its access and risk notes — live in [the catalog README](catalog/README.md).

Missing an important official source? [Propose a resource or report a correction](https://github.com/flypythoncom/python/issues/new/choose).
<!-- catalog-index:end -->

## What this repository owns

- First-party bilingual guides and task playbooks.
- Runnable, verifiable Python examples and reusable agent-work templates.
- Reviewed official documentation, standards, and project sources.
- Deterministic manifests, validation, exports, and safe link audits.
- A human-review queue for the [Python Project Radar](catalog/projects/README.md).

The website owns presentation, navigation, search, newsletter, and future paid
experiences. It consumes a deliberate pinned version of this repository; it
must not silently fork or rewrite the source claims.
Maintainers can follow the [repository-to-website operating model](docs/REPO_TO_WEBSITE.md)
to add measurable calls to action without inventing unavailable products.

## Repository structure

```text
assets/                README images (verify.py terminal demo)
catalog/
  README.md            browsable reviewed catalog (English, generated)
  README_cn.md         browsable reviewed catalog (Chinese, generated)
  catalog.yml          catalog status and review date
  paths.yml            bilingual learning-path definitions
  resources/           one reviewed resource per YAML file
  projects/            human-review queue for current Python projects
courses/              challenge courses with TASK.md contracts and verify.py claim codes
paths/                learning paths sequencing courses into badge routes
guides/               Python engineering and AI-coding methods
playbooks/            repeatable task procedures and definitions of done
examples/             small runnable projects with automated verification
templates/            task, plan, review, and verification starters
schema/
  *.schema.json       versioned machine-readable contracts
catalog.json         deterministic public export for consumers
radar.json            deterministic Project Radar export for consumers
content-manifest.json versioned paths, summaries, and checksums for the website
tools/                generation, validation, example, and link-audit commands
tests/                content consistency and behavior tests
docs/                 consumer contract and curation policy
```

`catalog.json` and `content-manifest.json` are generated; do not edit them by
hand. Website consumers read both from a pinned commit, verify checksums, and
record that revision in their own lock file. They must not fetch a moving branch
during a production build.

Example immutable URL:

```text
https://raw.githubusercontent.com/flypythoncom/python/<full-commit-sha>/catalog.json
```

The content manifest lets flypython.com render the matching bilingual guide or
playbook without owning a second editable copy.

## Contribute

Propose a resource, report a correction, or improve a course. Read
[CONTRIBUTING.md](CONTRIBUTING.md) first — it covers the local setup, the
deterministic checks CI runs, and how to regenerate the generated exports.
Also read the [curation policy](docs/CURATION_POLICY.md) before proposing a
resource or changing its classification, and the
[consumer contract](docs/CONSUMING.md) for website integrations.
