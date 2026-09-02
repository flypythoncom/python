# 公开接口契约规范（API Specification）

- **接口路径**：`POST /v1/transactions`
- **鉴权方式**：`Bearer <api_key>`
- **幂等机制**：通过 `Idempotency-Key` 请求头支持

## 请求结构契约（Request Body）

```json
{
  "user_id": 101,
  "amount": 99.95,
  "currency": "USD",
  "status": "pending"
}
```

## 成功响应契约（200 OK）

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

## 统一错误响应结构（4xx / 5xx）

```json
{
  "error": {
    "code": "INVALID_PARAM",
    "message": "amount must be greater than 0",
    "field": "amount"
  }
}
```
