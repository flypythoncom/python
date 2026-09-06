from __future__ import annotations

import unittest

from pipeline import run_pipeline


class TestStructuredPipeline(unittest.TestCase):
    def test_all_valid_records(self) -> None:
        items = [
            {"id": "item-1", "value": 10},
            {"id": "item-2", "value": 20.5},
        ]
        result = run_pipeline(items, batch_size=2)
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["successful"], 2)
        self.assertEqual(result["failed"], 0)
        self.assertEqual(result["errors"], [])
        self.assertEqual(
            result["results"],
            [
                {"id": "item-1", "processed_value": 11.0},
                {"id": "item-2", "processed_value": 22.55},
            ],
        )

    def test_invalid_batch_size_raises(self) -> None:
        with self.assertRaises(ValueError):
            run_pipeline([], batch_size=0)

    def test_isolates_and_records_malformed_records(self) -> None:
        items = [
            {"id": "valid-1", "value": 100},
            {"id": "", "value": 50},  # empty id
            {"id": "bad-val", "value": -5},  # non-positive
            {"id": "bad-type", "value": "hundred"},  # string instead of number
            {"id": "valid-2", "value": 50},
        ]
        result = run_pipeline(items, batch_size=2)
        self.assertEqual(result["total"], 5)
        self.assertEqual(result["successful"], 2)
        self.assertEqual(result["failed"], 3)
        self.assertEqual(len(result["errors"]), 3)
        failed_ids = [err["id"] for err in result["errors"]]
        self.assertIn("bad-val", failed_ids)
        self.assertIn("bad-type", failed_ids)

    def test_empty_input(self) -> None:
        result = run_pipeline([], batch_size=10)
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["successful"], 0)
        self.assertEqual(result["failed"], 0)
        self.assertEqual(result["results"], [])
        self.assertEqual(result["errors"], [])


if __name__ == "__main__":
    unittest.main()
