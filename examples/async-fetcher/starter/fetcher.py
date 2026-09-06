"""Naive unconstrained async fetcher without semaphore bounding or retry handling."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any


async def async_batch_fetch(
    items: list[dict[str, Any]],
    fetch_fn: Callable[[dict[str, Any]], Awaitable[dict[str, Any]]],
    max_concurrency: int = 3,
    max_retries: int = 3,
) -> list[dict[str, Any]]:
    # Naive: Unbounded gather without Semaphore or retry on error
    tasks = [fetch_fn(item) for item in items]
    responses = await asyncio.gather(*tasks)

    results = []
    for item, resp in zip(items, responses, strict=False):
        results.append({
            "item": item,
            "success": resp.get("status_code") == 200,
            "status_code": resp.get("status_code"),
            "data": resp.get("data"),
            "attempts": 1,
            "error": None,
        })
    return results
