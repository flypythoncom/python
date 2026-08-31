---
layout: default
title: Python Resource Catalog for the AI Era
description: A reviewed catalog of primary Python sources for foundations, web APIs, automation, and AI agents.
lang: en-US
permalink: /
image:
  path: /assets/images/og-image.png
  width: 1200
  height: 630
  alt: FlyPython Python Resource Catalog
---
{% assign catalog_resources = site.data.resources.resources | where: "status", "active" %}

# Learn Python from sources worth trusting.

FlyPython is a reviewed map of official documentation, standards, and
first-party project resources. Use the four paths to find the next reliable
source, then return to the main learning hub for guided projects and context.

<div class="cta-row" aria-label="Primary actions">
  <a class="button button-primary" href="https://flypython.com/learn">Start with the roadmap</a>
  <a class="button" href="https://flypython.com/resources">Browse the featured index</a>
  <a class="button" href="https://github.com/flypythoncom/python">Contribute on GitHub</a>
</div>

<p class="catalog-note">
  <strong>{{ catalog_resources.size }} active resources</strong>
  <span aria-hidden="true">·</span>
  Catalog reviewed {{ site.data.resources.catalog.reviewed_on }}
  <span aria-hidden="true">·</span>
  Primary sources first
</p>

<nav class="path-grid" aria-label="Learning paths">
  {% for path in site.data.resources.catalog.paths %}
    {% assign path_resources = catalog_resources | where: "path", path.id %}
    <a class="path-card" href="#{{ path.id }}">
      <span class="path-number">0{{ path.order }}</span>
      <strong>{{ path.title_en }}</strong>
      <span>{{ path.summary_en }}</span>
      <small>{{ path_resources.size }} resources</small>
    </a>
  {% endfor %}
</nav>

{% for path in site.data.resources.catalog.paths %}
  {% assign path_resources = catalog_resources | where: "path", path.id %}
  <section class="path-section" id="{{ path.id }}" aria-labelledby="{{ path.id }}-title">
    <header class="section-heading">
      <div>
        <span class="section-eyebrow">Path 0{{ path.order }}</span>
        <h2 id="{{ path.id }}-title">{{ path.title_en }}</h2>
      </div>
      <p>{{ path.summary_en }}</p>
    </header>

    <div class="resource-grid">
      {% for resource in path_resources %}
        <article class="resource-card{% if resource.featured %} featured{% endif %}">
          <div class="resource-card-header">
            <span class="source-badge">{{ resource.source_type | replace: "-", " " }}</span>
            {% if resource.featured %}<span class="featured-badge">Featured</span>{% endif %}
          </div>
          <h3><a href="{{ resource.url }}">{{ resource.title }}</a></h3>
          <p>{{ resource.why_en }}</p>
          <ul class="resource-meta" aria-label="Resource metadata">
            <li>{{ resource.level | replace: "-", " " }}</li>
            {% case resource.language %}
              {% when "en" %}<li>English</li>
              {% when "zh" %}<li>Chinese</li>
              {% when "multilingual" %}<li>Multilingual</li>
            {% endcase %}
            <li>Reviewed {{ resource.reviewed_on }}</li>
          </ul>
          {% if resource.requires_key or resource.risk == "medium" %}
            <p class="resource-caution">
              {% if resource.requires_key %}<span>API key required for typical use</span>{% endif %}
              {% if resource.requires_key and resource.risk == "medium" %}<span aria-hidden="true">·</span>{% endif %}
              {% if resource.risk == "medium" %}<span>Review permissions and side effects</span>{% endif %}
            </p>
          {% endif %}
        </article>
      {% endfor %}
    </div>
  </section>
{% endfor %}

## How this catalog relates to FlyPython

This repository keeps the broader community resource map public and reviewable.
The main [FlyPython learning hub](https://flypython.com/) turns a smaller set of
those sources into practical learning paths, tested examples, and clear next
steps. Start with the
[no-key Python agent guide](https://flypython.com/learn/python-ai-agent-roadmap)
if you want a complete project before choosing an agent framework.
