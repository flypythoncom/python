# Task contract: bounded async batch fetcher with retries

Change only `starter/fetcher.py`.

- Implement `async_batch_fetch(items: list[dict], fetch_fn: Callable[[dict], Awaitable[dict]], max_concurrency: int = 3, max_retries: int = 3) -> list[dict]`.
- Concurrency bounding:
  - At most `max_concurrency` calls to `fetch_fn` may be executing concurrently at any moment.
- Retry & Backoff contract:
  - `fetch_fn` returns `{"status_code": int, "data": ...}` or raises an exception.
  - If `status_code` in `{429, 500, 502, 503, 504}` or an exception is raised, retry up to `max_retries` times.
  - Permanent client errors (status 400..499 except 429) must NOT be retried.
  - On retry, back off by `0.01 * (2 ** attempt)` seconds.
- Result collection:
  - Return a list of result dictionaries preserving input item order.
  - Each result dict must contain:
    - `"item"`: original input item dict.
    - `"success"`: `bool` (True if final status_code == 200).
    - `"status_code"`: `int | None`.
    - `"data"`: response data or None.
    - `"attempts"`: `int` (total attempts made, starting at 1).
    - `"error"`: error message string or None.
- Individual item failures must never raise uncaught exceptions to abort other items.

Done means `python examples/async-fetcher/verify.py starter` exits successfully.
