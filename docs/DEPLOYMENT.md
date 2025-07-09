---
title: "Deployment Guide"
description: "How to deploy FlyPython website"
---

# 🚀 FlyPython 部署指南 / Deployment Guide

本文档说明如何部署和维护 FlyPython 网站。

## 🏗️ 架构概览 / Architecture Overview

```
FlyPython Website
├── GitHub Repository (Source)
├── GitHub Pages (Hosting)
├── Jekyll (Static Site Generator)
├── Cayman Theme (UI Framework)
└── Custom CSS/JS (Enhancements)
```

## 📁 项目结构 / Project Structure

```
python/
├── _config.yml           # Jekyll 配置
├── _layouts/             # 页面布局模板
│   └── default.html
├── _includes/            # 可重用组件
│   └── head-custom.html
├── _data/               # 数据文件
│   └── navigation.yml
├── assets/              # 静态资源
│   └── css/
│       └── custom.css
├── docs/                # 文档目录
├── tools/               # 维护工具
│   └── check_links.py
├── README.md            # 英文主页
├── README_cn.md         # 中文主页
├── 404.md              # 错误页面
├── robots.txt          # SEO配置
├── CNAME               # 域名配置
└── Gemfile             # Ruby依赖
```

## 🌐 GitHub Pages 部署 / GitHub Pages Deployment

### 自动部署 / Automatic Deployment

GitHub Pages 会自动构建和部署：

1. **推送到主分支** → 自动触发构建
2. **Jekyll 处理** → 生成静态文件
3. **部署到 GitHub Pages** → 网站更新

### 部署配置

```yaml
# _config.yml 关键配置
url: "https://python.flypython.com"
baseurl: ""
remote_theme: pages-themes/cayman@v0.2.0
plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag
```

### 域名配置

```
# CNAME 文件内容
python.flypython.com
```

## 🔧 本地开发 / Local Development

### 环境要求

- Ruby 2.7+
- Bundler
- Jekyll

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/flypython/python.git
cd python

# 2. 安装依赖
bundle install

# 3. 启动本地服务器
bundle exec jekyll serve

# 4. 访问网站
# http://localhost:4000
```

### 开发命令

```bash
# 本地开发服务器
bundle exec jekyll serve --watch --drafts

# 构建静态文件
bundle exec jekyll build

# 检查链接有效性
python tools/check_links.py

# 清理构建文件
bundle exec jekyll clean
```

## 📊 性能监控 / Performance Monitoring

### 构建时间优化

```yaml
# 排除不必要的文件
exclude:
  - tools/
  - docs/DEPLOYMENT.md
  - link_audit_report.md
  - content_update_summary.md
```

### 资源优化

- **图片压缩**: 使用WebP格式
- **CSS压缩**: 启用SASS压缩
- **JavaScript最小化**: 使用Jekyll插件

## 🔍 SEO 配置 / SEO Configuration

### 关键配置

```yaml
# SEO设置
title: FlyPython
description: "Python学习资源聚合"
lang: zh-CN
plugins:
  - jekyll-seo-tag
  - jekyll-sitemap
```

### Sitemap 自动生成

- **sitemap.xml**: 自动生成
- **robots.txt**: 手动配置
- **Meta标签**: 自动添加

## 🛡️ 安全性 / Security

### HTTPS 配置

- GitHub Pages 自动提供 HTTPS
- 强制 HTTPS 重定向已启用

### 依赖管理

```bash
# 更新依赖
bundle update

# 安全审计
bundle audit
```

## 📈 分析和监控 / Analytics & Monitoring

### Google Analytics（可选）

```yaml
# _config.yml
google_analytics: UA-XXXXXXXX-X
```

### 性能指标

- **页面加载时间**: < 3秒
- **首字节时间**: < 1秒
- **可用性**: 99.9%

## 🔄 CI/CD 流程 / CI/CD Pipeline

### GitHub Actions 工作流

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [ master ]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: 3.0
      - name: Install dependencies
        run: bundle install
      - name: Build site
        run: bundle exec jekyll build
      - name: Check links
        run: python tools/check_links.py
```

## 🚨 故障排除 / Troubleshooting

### 常见问题

1. **构建失败**
   ```bash
   # 检查依赖
   bundle install
   bundle exec jekyll build --verbose
   ```

2. **链接失效**
   ```bash
   # 运行链接检查
   python tools/check_links.py
   ```

3. **样式问题**
   ```bash
   # 清理缓存
   bundle exec jekyll clean
   bundle exec jekyll build
   ```

### 调试命令

```bash
# 详细构建日志
bundle exec jekyll build --verbose

# 增量构建
bundle exec jekyll build --incremental

# 跟踪模式
bundle exec jekyll build --trace
```

## 📅 维护计划 / Maintenance Schedule

### 定期任务

- **每周**: 检查链接有效性
- **每月**: 更新依赖包
- **每季度**: 内容审核和更新
- **每年**: 重大版本升级

### 更新流程

1. 创建新分支
2. 更新内容
3. 本地测试
4. 提交 Pull Request
5. 代码审查
6. 合并到主分支
7. 自动部署

---

## 📞 支持联系 / Support Contact

如有部署问题，请：

1. 查看 [GitHub Issues](https://github.com/flypython/python/issues)
2. 创建新的 Issue
3. 联系维护团队

**🎯 目标**: 保持网站高可用性和最佳性能！ 