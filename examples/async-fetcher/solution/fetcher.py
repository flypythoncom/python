"""Resilient async batch fetcher with Semaphore concurrency control, exponential backoff, and error isolation."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

RETRYABLE_STATUSES = {429, 500, 502, 503, 504}


async def _fetch_single(
    item: dict[str, Any],
    fetch_fn: Callable[[dict[str, Any]], Awaitable[dict[str, Any]]],
    semaphore: asyncio.Semaphore,
    max_retries: int,
) -> dict[str, Any]:
    attempts = 0
    last_status: int | None = None
    last_error: str | None = None
    last_data: Any = None

    for attempt in range(max_retries):
        attempts += 1
        async with semaphore:
            try:
                resp = await fetch_fn(item)
                status = resp.get("status_code")
                last_status = status
                last_data = resp.get("data")

                if status == 200:
                    return {
                        "item": item,
                        "success": True,
                        "status_code": 200,
                        "data": last_data,
                        "attempts": attempts,
                        "error": None,
                    }

                # Permanent client error (400..499 except 429) -> don't retry
                if status is not None and 400 <= status < 500 and status not in RETRYABLE_STATUSES:
                    return {
                        "item": item,
                        "success": False,
                        "status_code": status,
                        "data": last_data,
                        "attempts": attempts,
                        "error": f"Client error: {status}",
                    }

                last_error = f"HTTP error {status}"
            except Exception as exc:
                last_error = str(exc)

        # Backoff before next retry if attempts remain
        if attempt < max_retries - 1:
            await asyncio.sleep(0.01 * (2 ** attempt))

    return {
        "item": item,
        "success": False,
        "status_code": last_status,
        "data": last_data,
        "attempts": attempts,
        "error": last_error or "Exceeded maximum retries",
    }


async def async_batch_fetch(
    items: list[dict[str, Any]],
    fetch_fn: Callable[[dict[str, Any]], Awaitable[dict[str, Any]]],
    max_concurrency: int = 3,
    max_retries: int = 3,
) -> list[dict[str, Any]]:
    semaphore = asyncio.Semaphore(max_concurrency)
    tasks = [_fetch_single(item, fetch_fn, semaphore, max_retries) for item in items]
    return await asyncio.gather(*tasks)
