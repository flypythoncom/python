# Task contract: validate untrusted transaction payload

Change only `starter/validator.py`.

- Implement `validate_transaction_payload(raw: dict) -> tuple[bool, dict]`.
- Return `(True, sanitized_dict)` on success, or `(False, errors_dict)` on failure.
- Key normalization:
  - Support both `userId` and `user_id` -> output normalized `user_id: int`.
  - Support both `amount` as float/int or dirty currency string (e.g. `"$120.50"` or `" 120.50 "`) -> output `amount: float` rounded to 2 decimal places. Amount must be > 0.
  - `status` must be one of `{"pending", "completed", "failed"}` (case-insensitive) -> output lowercase string.
- If payload is missing required fields or has invalid values, populate `errors_dict` mapping field name to error message.
- Do not raise unhandled exceptions on malformed input.

Done means `python examples/pydantic-validation/verify.py starter` exits successfully.
