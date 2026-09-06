from __future__ import annotations

import unittest

from validator import validate_transaction_payload


class TestTransactionValidator(unittest.TestCase):
    def test_valid_snake_case_payload(self) -> None:
        ok, res = validate_transaction_payload({
            "user_id": 42,
            "amount": 99.95,
            "status": "completed",
        })
        self.assertTrue(ok)
        self.assertEqual(res, {"user_id": 42, "amount": 99.95, "status": "completed"})

    def test_handles_camel_case_and_dirty_amount(self) -> None:
        ok, res = validate_transaction_payload({
            "userId": "101",
            "amount": " $120.50 ",
            "status": "PENDING",
        })
        self.assertTrue(ok)
        self.assertEqual(res, {"user_id": 101, "amount": 120.50, "status": "pending"})

    def test_rejects_missing_fields_without_crashing(self) -> None:
        ok, errors = validate_transaction_payload({})
        self.assertFalse(ok)
        self.assertIn("user_id", errors)
        self.assertIn("amount", errors)
        self.assertIn("status", errors)

    def test_rejects_invalid_amount_and_status(self) -> None:
        ok, errors = validate_transaction_payload({
            "user_id": 1,
            "amount": -50.0,
            "status": "unknown_state",
        })
        self.assertFalse(ok)
        self.assertIn("amount", errors)
        self.assertIn("status", errors)


if __name__ == "__main__":
    unittest.main()
