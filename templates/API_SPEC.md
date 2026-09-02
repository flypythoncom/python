# Public API Specification

- **Endpoint**: `POST /v1/transactions`
- **Authentication**: `Bearer <api_key>`
- **Idempotency**: Supported via `Idempotency-Key` header

## Request Contract

```json
{
  "user_id": 101,
  "amount": 99.95,
  "currency": "USD",
  "status": "pending"
}
```

## Response Contract (200 OK)

```json
{
  "transaction_id": "txn_8f7b2c",
  "user_id": 101,
  "amount": 99.95,
  "currency": "USD",
  "status": "pending",
  "created_at": "2026-09-02T12:00:00Z"
}
```

## Error Contract (4xx / 5xx)

```json
{
  "error": {
    "code": "INVALID_PARAM",
    "message": "amount must be greater than 0",
    "field": "amount"
  }
}
```
