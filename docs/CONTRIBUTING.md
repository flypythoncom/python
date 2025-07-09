---
title: "Contributing to FlyPython"
description: "How to contribute to the FlyPython project"
---

# 🤝 Contributing to FlyPython

感谢您对 FlyPython 项目的关注！我们欢迎各种形式的贡献。

## 📋 贡献方式 / Ways to Contribute

### 🔗 资源推荐 / Resource Recommendations
- 推荐优质的Python学习资源
- 分享有用的工具和库
- 提供最新的教程和课程信息

### 🐛 问题报告 / Issue Reporting
- 报告失效的链接
- 指出内容错误或过时信息
- 建议改进网站功能

### 📝 内容改进 / Content Improvement
- 改进文档质量
- 添加描述和分类
- 翻译内容（中英文）

### 💻 技术贡献 / Technical Contributions
- 改进网站设计
- 优化性能
- 添加新功能

## 🔄 贡献流程 / Contribution Process

### 1. Fork 项目
```bash
# 克隆你的 fork
git clone https://github.com/YOUR-USERNAME/python.git
cd python
```

### 2. 创建分支
```bash
# 创建新分支用于你的更改
git checkout -b feature/your-feature-name
# 或者
git checkout -b fix/issue-description
```

### 3. 进行更改
- 遵循现有的格式和风格
- 确保链接有效
- 添加适当的描述

### 4. 测试更改
```bash
# 本地测试 Jekyll 网站
bundle install
bundle exec jekyll serve

# 检查链接有效性
python tools/check_links.py
```

### 5. 提交更改
```bash
git add .
git commit -m "feat: add new Python tutorial resource"
# 或者
git commit -m "fix: update broken link in finance section"
```

### 6. 推送并创建 Pull Request
```bash
git push origin your-branch-name
```

然后在 GitHub 上创建 Pull Request。

## 📝 提交信息规范 / Commit Message Convention

使用语义化提交信息：

- `feat:` 添加新功能或资源
- `fix:` 修复问题或错误
- `docs:` 更新文档
- `style:` 格式化或样式更改
- `refactor:` 重构代码
- `test:` 添加或修改测试
- `chore:` 维护任务

### 示例 / Examples:
```
feat: add new machine learning tutorial section
fix: update broken DataCamp links
docs: improve installation instructions
style: format README according to style guide
```

## 📚 内容质量标准 / Content Quality Standards

### 资源推荐标准
1. **相关性**: 必须与Python学习相关
2. **质量**: 内容准确、实用、最新
3. **可访问性**: 链接有效，内容可访问
4. **多样性**: 涵盖不同难度级别和应用领域

### 链接要求
- 提供工作的URL
- 添加描述说明
- 注明语言（中文/英文）
- 标注难度级别（如适用）

### 格式要求
- 使用Markdown格式
- 遵循现有的结构和风格
- 添加适当的emoji和分类标签

## 🔍 代码审查 / Code Review

所有贡献都将经过代码审查：

1. **内容审查**: 确保资源质量和相关性
2. **格式检查**: 验证Markdown格式和链接
3. **技术审查**: 检查代码质量和性能
4. **兼容性测试**: 确保与GitHub Pages兼容

## 🆘 获取帮助 / Getting Help

如果您有任何问题：

1. 查看现有的 [Issues](https://github.com/flypython/python/issues)
2. 创建新的 Issue 描述您的问题
3. 在 Pull Request 中提问

## 📄 许可证 / License

通过贡献到这个项目，您同意您的贡献将在与项目相同的许可证下授权。

## 🙏 致谢 / Acknowledgments

感谢所有贡献者使 FlyPython 成为更好的Python学习资源！

---

**🚀 Happy Contributing!** 让我们一起让Python学习变得更好！ 