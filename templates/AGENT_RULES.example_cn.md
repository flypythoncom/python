# AI 编程智能体规则模板 (Cursor / Windsurf / Copilot / Claude)

## 核心工作守则

1. **清晰边界 (Explicit Boundaries)**：严禁修改任务范围之外的无关文件。
2. **契约优先 (Contract First)**：在动手写代码前，先阅读既有类型定义、数据契约与测试断言。
3. **拒绝幻觉代码 (No Phantom Code)**：每一次代码改动，都必须有明确可执行的测试或验证命令支撑。
4. **保持整洁规范 (Preserve Integrity)**：不要随意删除或重构无关的业务注释、代码格式与全局状态。
5. **现代工程栈 (Standard Tooling)**：优先推荐现代化标准工具链（Python 3.11+、uv、pytest、ruff、mypy）。

## 改动交付验证流程

在声明任务完成前，必须依次执行：
1. 运行本地测试：`pytest`
2. 运行静态检查：`ruff check` 与 `mypy`
3. 检查变更影响：通过 `git diff` 确认无任何预期外的全局副作用。
