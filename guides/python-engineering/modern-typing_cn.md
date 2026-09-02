---
id: python-modern-typing
type: guide
title: 现代 Python 类型系统实战
summary: 将明确的 Python 类型作为机器可读的契约，指导可靠的 AI 辅助编程与工程交付。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# 现代 Python 类型系统实战

在 AI Coding 时代，类型注解不是可有可无的装饰。它们是机器可解析的边界契约，能够有效约束大模型的
代码生成范围，并在代码运行前拦截逻辑倒退。

## 1. 使用 Protocol 实现结构化子类型（鸭子类型契约）

避免为测试桩或服务适配器构建繁重的类继承层级。使用 `typing.Protocol` 定义轻量级的行为接口：

```python
from typing import Protocol

class DataRepository(Protocol):
    def get_by_id(self, item_id: str) -> dict | None: ...
    def save(self, item_id: str, data: dict) -> None: ...
```

无论是测试用的 Mock 对象还是真实的数据库适配器，只要签名匹配即可满足 `DataRepository` 契约，
使单元测试运行极快，并解耦业务逻辑与存储实现。

## 2. 使用 TypedDict 与 Pydantic 建立严格边界契约

处理来自外部不可信的 JSON 数据时，内部使用 `typing.TypedDict` 描述确定性结构，在系统网络边界处
使用 [Pydantic documentation](https://pydantic.dev/docs/validation/latest/get-started/) 进行反序列化和严格校验。

```python
from typing import TypedDict

class UserProfile(TypedDict):
    user_id: int
    username: str
    is_active: bool
```

## 3. 使用泛型保留容器与管道的类型信息

使用 `typing.TypeVar` 或现代 Python 3.12+ 泛型语法（如 `class Container[T]: ...`），确保在缓存层、
任务队列与 API 包装器中保持类型连续性，避免退化为无约束的 `Any`。

## 4. 在开发与 CI 流程中进行静态验证

类型注解只有在被强制检查时才具备确定性价值。在 CI 流水线中运行 [Mypy documentation](https://mypy.readthedocs.io/en/stable/)
或 Pyright，确保公共接口类型完备。

更多类型系统权威规范可参考官方 [Python typing documentation](https://typing.python.org/en/latest/)。
