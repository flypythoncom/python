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
  Catalog reviewed {{ site.data.resources.catalog.reviewed_on | escape }}
  <span aria-hidden="true">·</span>
  Primary sources first
</p>

{% include catalog-grid.html resources=catalog_resources %}

## How this catalog relates to FlyPython

This repository keeps the broader community resource map public and reviewable.
The main [FlyPython learning hub](https://flypython.com/) turns a smaller set of
those sources into practical learning paths, tested examples, and clear next
steps. Start with the
[no-key Python agent guide](https://flypython.com/learn/python-ai-agent-roadmap)
if you want a complete project before choosing an agent framework.
