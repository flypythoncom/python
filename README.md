# FlyPython Python Resource Catalog

[![GitHub stars](https://img.shields.io/github/stars/flypythoncom/python?style=flat-square&label=stars)](https://github.com/flypythoncom/python/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/flypythoncom/python?style=flat-square&label=forks)](https://github.com/flypythoncom/python/forks)
[![Catalog](https://img.shields.io/badge/catalog-reviewed-157878?style=flat-square)](https://python.flypython.com/)

[English](README.md) · [中文](README_cn.md)

FlyPython is the broad, community-maintained resource catalog behind the
[FlyPython learning hub](https://flypython.com/). It keeps the larger source map
public and reviewable while the main site provides editorial learning paths and a
smaller featured collection.

## Start here

- [Follow the practical Python roadmap](https://flypython.com/learn)
- [Browse the featured resource index](https://flypython.com/resources)
- [Build and test a no-key Python agent loop](https://flypython.com/learn/python-ai-agent-roadmap)
- [Explore the full community catalog](https://python.flypython.com/)

## Four paths

1. **Python foundations** — language, environments, dependencies, typing, and tests
2. **Web and APIs** — typed services, validation, HTTP clients, and applications
3. **Automation** — files, processes, browsers, crawling, and data workflows
4. **AI agents** — tools, structured output, state, evaluation, and safety boundaries

The canonical catalog lives in [`_data/resources.yml`](_data/resources.yml).
The English and Chinese site pages read from that same file; the full resource
list is not copied into the README files.

## Quality bar

- Prefer official documentation, standards, and first-party project sources.
- Explain why each resource matters instead of publishing an unranked link dump.
- Record the review date, API-key requirement, and relevant safety boundary.
- Label experiments honestly; do not infer production readiness from popularity.

See [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a resource or changing
its classification.

## Local preview

```bash
bundle install
bundle exec jekyll serve
```

The catalog is published at [python.flypython.com](https://python.flypython.com/).
