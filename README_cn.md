# FlyPython Python 资源目录

[![GitHub stars](https://img.shields.io/github/stars/flypythoncom/python?style=flat-square&label=stars)](https://github.com/flypythoncom/python/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/flypythoncom/python?style=flat-square&label=forks)](https://github.com/flypythoncom/python/forks)
[![Catalog](https://img.shields.io/badge/catalog-reviewed-157878?style=flat-square)](https://python.flypython.com/zh/)

[English](README.md) · [中文](README_cn.md)

FlyPython 是 [FlyPython 学习站](https://flypython.com/)背后的社区公开资源目录。
本仓库维护覆盖面更广、可公开审核的来源地图；主站负责编辑型学习路径和更精简的精选资源。

## 从这里开始

- [查看实用 Python 学习路线](https://flypython.com/learn)
- [浏览主站精选资源](https://flypython.com/resources)
- [构建并测试无需 API Key 的 Python Agent 循环](https://flypython.com/learn/python-ai-agent-roadmap)
- [浏览完整中文目录](https://python.flypython.com/zh/)

## 四条路径

1. **Python 基础** — 语言、环境、依赖、类型与测试
2. **Web 与 API** — 类型化服务、数据验证、HTTP 客户端与应用
3. **自动化** — 文件、进程、浏览器、爬取与数据工作流
4. **AI Agent** — 工具、结构化输出、状态、评测与安全边界

唯一的目录数据源是 [`_data/resources.yml`](_data/resources.yml)。英文页和中文页
都读取同一份数据，不再在多个 Markdown 文件中复制完整资源清单。

## 收录标准

- 优先选择官方文档、正式标准与项目的一手来源。
- 说明每条资源为什么值得使用，而不是堆放未经筛选的链接。
- 记录审核日期、API Key 要求与需要关注的安全边界。
- 如实标记实验性内容，不用流行度推断“生产可用”。

提交新资源或修改分类前，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 本地预览

```bash
bundle install
bundle exec jekyll serve
```

目录发布在 [python.flypython.com/zh/](https://python.flypython.com/zh/)。
