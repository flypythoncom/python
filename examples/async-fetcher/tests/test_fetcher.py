from __future__ import annotations

import asyncio
import unittest

from fetcher import async_batch_fetch


class TestAsyncBatchFetcher(unittest.TestCase):
    def test_rejects_invalid_concurrency(self) -> None:
        async def mock_fetch(item: dict) -> dict:
            return {"status_code": 200, "data": item}

        async def run_invalid(value: object) -> None:
            # Bound the regression test itself: Semaphore(0) used to hang.
            await asyncio.wait_for(
                async_batch_fetch([{"id": 1}], mock_fetch, max_concurrency=value),
                timeout=1,
            )

        for invalid in (0, -1, True, False, 1.5, "2", None, float("nan"), float("inf")):
            with self.subTest(max_concurrency=invalid):
                with self.assertRaisesRegex(ValueError, "max_concurrency must be a positive integer"):
                    asyncio.run(run_invalid(invalid))
                with self.assertRaisesRegex(ValueError, "max_concurrency must be a positive integer"):
                    asyncio.run(async_batch_fetch([], mock_fetch, max_concurrency=invalid))

    def test_single_concurrency_and_empty_input(self) -> None:
        async def mock_fetch(item: dict) -> dict:
            return {"status_code": 200, "data": item["id"]}

        self.assertEqual(asyncio.run(async_batch_fetch([], mock_fetch, max_concurrency=1)), [])
        results = asyncio.run(async_batch_fetch([{"id": 1}], mock_fetch, max_concurrency=1))
        self.assertTrue(results[0]["success"])
        self.assertEqual(results[0]["data"], 1)

    def test_bounded_concurrency(self) -> None:
        active_concurrency = 0
        peak_concurrency = 0

        async def mock_fetch(item: dict) -> dict:
            nonlocal active_concurrency, peak_concurrency
            active_concurrency += 1
            peak_concurrency = max(peak_concurrency, active_concurrency)
            await asyncio.sleep(0.01)
            active_concurrency -= 1
            return {"status_code": 200, "data": item["id"]}

        items = [{"id": i} for i in range(10)]
        results = asyncio.run(async_batch_fetch(items, mock_fetch, max_concurrency=2))

        self.assertEqual(len(results), 10)
        self.assertLessEqual(peak_concurrency, 2)
        self.assertTrue(all(r["success"] for r in results))

    def test_retries_transient_failure(self) -> None:
        attempts_by_id = {}

        async def mock_flaky_fetch(item: dict) -> dict:
            i = item["id"]
            attempts_by_id[i] = attempts_by_id.get(i, 0) + 1
            if attempts_by_id[i] < 3:
                return {"status_code": 429, "data": None}
            return {"status_code": 200, "data": "ok"}

        items = [{"id": 1}]
        results = asyncio.run(async_batch_fetch(items, mock_flaky_fetch, max_retries=3))

        self.assertEqual(len(results), 1)
        self.assertTrue(results[0]["success"])
        self.assertEqual(results[0]["attempts"], 3)

    def test_does_not_retry_404_error(self) -> None:
        call_count = 0

        async def mock_404_fetch(item: dict) -> dict:
            nonlocal call_count
            call_count += 1
            return {"status_code": 404, "data": None}

        items = [{"id": 1}]
        results = asyncio.run(async_batch_fetch(items, mock_404_fetch, max_retries=3))

        self.assertEqual(call_count, 1)
        self.assertFalse(results[0]["success"])
        self.assertEqual(results[0]["status_code"], 404)

    def test_records_exhausted_retries_without_crashing(self) -> None:
        async def mock_failing_fetch(item: dict) -> dict:
            raise ConnectionResetError("Server disconnected")

        items = [{"id": 1}, {"id": 2}]
        results = asyncio.run(async_batch_fetch(items, mock_failing_fetch, max_retries=2))

        self.assertEqual(len(results), 2)
        self.assertFalse(results[0]["success"])
        self.assertIn("Server disconnected", results[0]["error"])


if __name__ == "__main__":
    unittest.main()
