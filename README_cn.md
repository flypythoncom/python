# FlyPython

[python.flypython.com](https://python.flypython.com)

FlyPython 是一个双语 Jekyll 站点，主题聚焦 Python Agent 开发、AI 工程实践和长期有效的学习资源整理。

## 站点结构

- [index.md](index.md) 是英文首页。
- [zh-cn.md](zh-cn.md) 是中文首页。
- [_layouts/default.html](_layouts/default.html) 提供共享页面骨架、目录脚本和语言切换。
- [assets/css/custom.css](assets/css/custom.css) 提供卡片、折叠分组和整体视觉样式。
- [tools/check_links.py](tools/check_links.py) 用于检查首页外链状态。

## 本地维护

- 安装 Python 依赖：`python3 -m pip install -r requirements.txt`
- 运行链接检查：`python3 tools/check_links.py`
- Jekyll 依赖声明在 [Gemfile](Gemfile)

## 说明

- `reports/` 下的链接检查结果是生成文件，已加入忽略，不应提交。
- 当前本地 Ruby 需要升级到 `3.x` 及以上，才能成功安装 `github-pages` 依赖集。
