"""Naive implementation with unhandled KeyError, dirty string errors, and crash on invalid status."""

from __future__ import annotations

from typing import Any


def validate_transaction_payload(raw: Any) -> tuple[bool, dict[str, Any]]:
    # Naive access will crash on non-dict or camelCase keys
    user_id = int(raw["user_id"])
    amount = float(raw["amount"])
    status = raw["status"]

    if amount <= 0:
        return False, {"amount": "must be greater than 0"}

    return True, {
        "user_id": user_id,
        "amount": amount,
        "status": status,
    }
