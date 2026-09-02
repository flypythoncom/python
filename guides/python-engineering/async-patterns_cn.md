---
id: python-async-patterns
type: guide
title: 异步 Python 可靠模式与避坑指南
summary: 通过避免常见异步反模式与规范管理任务生命周期，构建高韧性的并发 Python 应用。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# 异步 Python 可靠模式与避坑指南

异步 Python (`asyncio`) 为 IO 密集型应用提供了极高的并发吞吐量，例如基于
[FastAPI documentation](https://fastapi.tiangolo.com/) 构建的 Web 服务或基于
[HTTPX documentation](https://www.python-httpx.org/) 的数据管道。
但在 AI 辅助编码中，Agent 容易生成隐蔽的异步并发缺陷。

## 1. 严禁在事件循环中调用阻塞 IO

在协程中直接调用同步阻塞操作（如 `time.sleep` 或阻塞式网络请求）会冻结整个事件循环，
导致其他所有并发协程饥饿停滞。必须通过 `asyncio.to_thread()` 将无法异步化的操作委托至后台线程池：

```python
import asyncio

def blocking_io_task(): ...

async def handle_request():
    result = await asyncio.to_thread(blocking_io_task)
```

## 2. 优先使用 TaskGroup 替代裸 gather

在 Python 3.11+ 中，推荐使用 `asyncio.TaskGroup` 实现结构化并发。相比 `asyncio.gather`，
`TaskGroup` 保证当其中任何一个子任务发生未捕获异常时，会自动取消并清理其余同级任务，
彻底杜绝孤儿悬挂任务泄露。

```python
import asyncio

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_user(1))
        task2 = tg.create_task(fetch_orders(1))
```

## 3. 使用 Semaphore 限制最大并发

严禁对大规模数据集直接发起无界并发。始终使用 `asyncio.Semaphore` 限制并发上限，
防止打满系统文件描述符或触发下游服务 429 限流风暴。

## 4. 完备处理协程取消与资源释放

在协程被取消（CancelledError）时，必须通过 `try...finally` 或异步上下文管理器
确保数据库连接、HTTP 会话及锁资源被正确释放。
