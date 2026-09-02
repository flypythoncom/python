# 任务契约：带受控并发与重试的异步抓取器

仅修改 `starter/fetcher.py`。

- 实现 `async_batch_fetch(items: list[dict], fetch_fn: Callable[[dict], Awaitable[dict]], max_concurrency: int = 3, max_retries: int = 3) -> list[dict]`。
- 并发控制要求：
  - 任何时刻并发执行 `fetch_fn` 的协程数量不得超过 `max_concurrency`。
- 重试与退避策略：
  - `fetch_fn` 返回 `{"status_code": int, "data": ...}` 或抛出异常。
  - 状态码为 `{429, 500, 502, 503, 504}` 或发生异常时，最多重试 `max_retries` 次。
  - 确定性客户端错误（400..499，排除 429）**严禁**重试。
  - 重试时采用指数退避休眠 `0.01 * (2 ** attempt)` 秒。
- 结果聚合规范：
  - 返回结果列表并严格保持与输入 `items` 的顺序一致。
  - 每个结果字典包含以下字段：
    - `"item"`：原始输入字典。
    - `"success"`：`bool`（最终 status_code == 200 时为 True）。
    - `"status_code"`：`int | None`。
    - `"data"`：响应数据或 None。
    - `"attempts"`：`int`（实际执行尝试次数，初始为 1）。
    - `"error"`：错误描述字符串或 None。
- 单个任务失败绝不能抛出未捕获异常中断整个批处理。

完成标准：`python examples/async-fetcher/verify.py starter` 成功退出。
