"""Robust transaction payload sanitizer and validator with structured error reporting."""

from __future__ import annotations

import re
from typing import Any

ALLOWED_STATUSES = {"pending", "completed", "failed"}
CLEAN_CURRENCY_RE = re.compile(r"^[$\s]*([0-9]+(?:\.[0-9]+)?)[$\s]*$")


def validate_transaction_payload(raw: Any) -> tuple[bool, dict[str, Any]]:
    if not isinstance(raw, dict):
        return False, {"_schema": "payload must be a JSON object"}

    errors: dict[str, str] = {}
    sanitized: dict[str, Any] = {}

    # 1. user_id (support user_id or userId)
    raw_user_id = raw.get("user_id", raw.get("userId"))
    if raw_user_id is None:
        errors["user_id"] = "field is required"
    else:
        try:
            val = int(raw_user_id)
            if val <= 0:
                errors["user_id"] = "must be a positive integer"
            else:
                sanitized["user_id"] = val
        except (ValueError, TypeError):
            errors["user_id"] = "must be a valid integer"

    # 2. amount (support numeric or dirty string "$120.50")
    raw_amount = raw.get("amount")
    if raw_amount is None:
        errors["amount"] = "field is required"
    elif isinstance(raw_amount, (int, float)):
        if raw_amount <= 0:
            errors["amount"] = "must be greater than 0"
        else:
            sanitized["amount"] = round(float(raw_amount), 2)
    elif isinstance(raw_amount, str):
        match = CLEAN_CURRENCY_RE.match(raw_amount.strip())
        if match:
            try:
                parsed = float(match.group(1))
                if parsed <= 0:
                    errors["amount"] = "must be greater than 0"
                else:
                    sanitized["amount"] = round(parsed, 2)
            except ValueError:
                errors["amount"] = "must be a valid numeric amount"
        else:
            errors["amount"] = "must be a valid numeric amount"
    else:
        errors["amount"] = "must be a valid numeric amount"

    # 3. status (case-insensitive enum)
    raw_status = raw.get("status")
    if raw_status is None:
        errors["status"] = "field is required"
    elif isinstance(raw_status, str):
        lowered = raw_status.strip().lower()
        if lowered not in ALLOWED_STATUSES:
            errors["status"] = f"must be one of {sorted(ALLOWED_STATUSES)}"
        else:
            sanitized["status"] = lowered
    else:
        errors["status"] = f"must be one of {sorted(ALLOWED_STATUSES)}"

    if errors:
        return False, errors
    return True, sanitized
