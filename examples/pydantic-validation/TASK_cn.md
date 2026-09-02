# 任务契约：验证不可信交易请求体

仅修改 `starter/validator.py`。

- 实现 `validate_transaction_payload(raw: dict) -> tuple[bool, dict]`。
- 成功时返回 `(True, sanitized_dict)`，校验失败时返回 `(False, errors_dict)`。
- 字段规范化契约：
  - 同时支持 `userId` 与 `user_id` -> 输出规范化字段 `user_id: int`。
  - 支持 `amount` 为数字或带符号字符串（如 `"$120.50"`、`" 120.50 "`）-> 输出保留两位小数的 `amount: float`，且数值必须大于 0。
  - `status` 必须为 `{"pending", "completed", "failed"}` 之一（不区分大小写）-> 输出全小写字符串。
- 缺少必填字段或格式非法时，在 `errors_dict` 中填充以字段名为键、错误描述为值的映射。
- 遇到非法数据时不得抛出未捕获异常崩溃。

完成标准：`python examples/pydantic-validation/verify.py starter` 成功退出。
