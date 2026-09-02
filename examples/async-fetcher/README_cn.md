---
id: example-async-fetcher
type: example
title: 带受控并发与重试的异步抓取器
summary: 使用 Semaphore 信号量控制并发、指数退避重试与错误隔离，实现韧性异步任务批处理。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# 带受控并发与重试的异步抓取器

无限制的异步并发（如直接对成千上万个任务调用 `asyncio.gather`）极易引发套接字耗尽、
429 限流风暴与下游服务雪崩。生产级批处理器必须通过 Semaphore 限制最大并发数，针对瞬时
网络故障（429、503、超时）进行退避重试，对确定性错误（400、404）快速失败，并对单个任务
的失败进行隔离，绝不导致整个批处理异常中断。

```bash
python examples/async-fetcher/verify.py starter --expect-failure
python examples/async-fetcher/verify.py solution
```

第一条命令复现朴素 starter 的并发溢出与崩溃；第二条命令验证具备容错能力的 solution。
把 [TASK_cn.md](TASK_cn.md) 提交给 coding agent，让其仅修改 `starter/fetcher.py` 并运行：

```bash
python examples/async-fetcher/verify.py starter
```
