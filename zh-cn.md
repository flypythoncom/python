---
layout: default
title: 面向 AI 时代的 Python 资源目录
description: 经过审核的 Python 一手资源目录，覆盖基础、Web API、自动化与 AI Agent。
lang: zh-CN
permalink: /zh/
image:
  path: /assets/images/og-image.png
  width: 1200
  height: 630
  alt: FlyPython Python 资源目录
---
{% assign catalog_resources = site.data.resources.resources | where: "status", "active" %}

# 从值得信任的一手来源学习 Python。

FlyPython 收录官方文档、正式标准和项目的一手资源。通过四条路径找到下一份可靠资料，
再回到主学习站，用完整项目和清晰上下文把知识真正用起来。

<div class="cta-row" aria-label="主要操作">
  <a class="button button-primary" href="https://flypython.com/learn">从学习路线开始</a>
  <a class="button" href="https://flypython.com/resources">浏览主站精选资源</a>
  <a class="button" href="https://github.com/flypythoncom/python">在 GitHub 参与维护</a>
</div>

<p class="catalog-note">
  <strong>{{ catalog_resources.size }} 条有效资源</strong>
  <span aria-hidden="true">·</span>
  目录审核于 {{ site.data.resources.catalog.reviewed_on }}
  <span aria-hidden="true">·</span>
  一手来源优先
</p>

<nav class="path-grid" aria-label="学习路径">
  {% for path in site.data.resources.catalog.paths %}
    {% assign path_resources = catalog_resources | where: "path", path.id %}
    <a class="path-card" href="#{{ path.id }}">
      <span class="path-number">0{{ path.order }}</span>
      <strong>{{ path.title_zh }}</strong>
      <span>{{ path.summary_zh }}</span>
      <small>{{ path_resources.size }} 条资源</small>
    </a>
  {% endfor %}
</nav>

{% for path in site.data.resources.catalog.paths %}
  {% assign path_resources = catalog_resources | where: "path", path.id %}
  <section class="path-section" id="{{ path.id }}" aria-labelledby="{{ path.id }}-title">
    <header class="section-heading">
      <div>
        <span class="section-eyebrow">路径 0{{ path.order }}</span>
        <h2 id="{{ path.id }}-title">{{ path.title_zh }}</h2>
      </div>
      <p>{{ path.summary_zh }}</p>
    </header>

    <div class="resource-grid">
      {% for resource in path_resources %}
        <article class="resource-card{% if resource.featured %} featured{% endif %}">
          <div class="resource-card-header">
            {% case resource.source_type %}
              {% when "official-docs" %}<span class="source-badge">官方文档</span>
              {% when "official-standard" %}<span class="source-badge">正式标准</span>
              {% when "official-project" %}<span class="source-badge">官方项目</span>
            {% endcase %}
            {% if resource.featured %}<span class="featured-badge">精选</span>{% endif %}
          </div>
          <h3><a href="{{ resource.url }}">{{ resource.title }}</a></h3>
          <p>{{ resource.why_zh }}</p>
          <ul class="resource-meta" aria-label="资源元数据">
            {% case resource.level %}
              {% when "beginner" %}<li>入门</li>
              {% when "intermediate" %}<li>进阶</li>
              {% when "advanced" %}<li>高级</li>
              {% when "all-levels" %}<li>所有阶段</li>
            {% endcase %}
            <li>来源语言：{{ resource.language | upcase }}</li>
            <li>审核于 {{ resource.reviewed_on }}</li>
          </ul>
          {% if resource.requires_key or resource.risk == "medium" %}
            <p class="resource-caution">
              {% if resource.requires_key %}<span>典型用法需要 API Key</span>{% endif %}
              {% if resource.requires_key and resource.risk == "medium" %}<span aria-hidden="true">·</span>{% endif %}
              {% if resource.risk == "medium" %}<span>请检查权限与外部副作用</span>{% endif %}
            </p>
          {% endif %}
        </article>
      {% endfor %}
    </div>
  </section>
{% endfor %}

## 这个目录与 FlyPython 主站的关系

本仓库公开维护覆盖面更广的社区资源地图；[FlyPython 学习站](https://flypython.com/)
从中挑选更小的一组来源，组织成实用学习路径、经过测试的示例和清晰的下一步。
如果你想先完成一个项目再选择 Agent 框架，可以从
[无需 API Key 的 Python Agent 指南](https://flypython.com/learn/python-ai-agent-roadmap)开始。
