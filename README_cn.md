# FlyPython Python 资源目录

[English](README.md) · [中文](README_cn.md)

这个仓库是 [flypython.com](https://flypython.com/) 展示 Python 资源时使用的、经过
审核的数据源。它不是第二个网站，也不再包含网站渲染器、主题或部署配置。

## 这里维护什么

- 官方文档、正式标准和项目一手来源的规范链接；
- 经过人工审核的中英文收录理由；
- 学习路径、难度、访问要求、审核日期与安全信息；
- 确定性的校验、JSON 导出和安全链接审计工具；
- 公开的贡献与策展规则。

主站负责学习指南、任务型 Playbook、导航和视觉展示；本仓库负责覆盖面更广的目录数据
及其可审查的维护流程。

## 仓库结构

```text
catalog/
  catalog.yml        目录状态和审核日期
  paths.yml          中英文学习路径定义
  resources/         每项资源一个 YAML 文件
schema/
  catalog-v1.schema.json
catalog.json         提供给网站使用的确定性公开导出
tools/               校验、导出和链接审计工具
tests/               目录与网络安全测试
docs/                策展政策
```

`catalog.json` 由 `catalog/` 生成，不能手工修改。消费方应从完整 commit SHA 读取导出、
校验文件摘要，并在自己的锁文件中记录该版本；生产构建不能直接追随持续变化的
`master`。

固定版本地址示例：

```text
https://raw.githubusercontent.com/flypythoncom/python/<full-commit-sha>/catalog.json
```

导出包含主站可以直接使用的中英文路径说明、资源理由、级别、访问条件和风险字段。
第一方教程和任务 Playbook 仍然只放在网站仓库。

## 本地校验

使用 `.python-version` 指定的 Python，并安装锁定的开发依赖：

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.lock.txt
```

修改目录源文件后重新生成导出并运行校验：

```bash
python tools/export_catalog.py
python -m pytest
python tools/validate_catalog.py
python tools/export_catalog.py --check
```

网络链接检查不会在 Pull Request 中运行，而是由维护者通过定时或手动的
**Catalog link audit** 工作流执行。

提交资源或修改分类前，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 和
[策展政策](docs/CURATION_POLICY.md)。网站接入还应遵循
[消费方契约](docs/CONSUMING.md)。
