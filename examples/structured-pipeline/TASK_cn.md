# 任务契约：构建鲁棒的结构化批处理流水线（带错误隔离与统计）

仅修改 `starter/pipeline.py`。

- `run_pipeline(items: list[dict], batch_size: int = 2) -> dict` 分批处理输入记录。
- 传入的每条记录必须是包含非空字符串 `'id'` 以及正数（int 或 float）`'value'` 的字典。
- 合法记录应被转换为 `{'id': item['id'], 'processed_value': round(item['value'] * 1.1, 2)}`。
- 非法记录绝不能导致整批中断崩溃，必须被收集进 `'errors'` 列表，格式为 `{'id': item.get('id', 'unknown'), 'reason': str(error)}`。
- 函数必须返回统一统计字典：`{'total': int, 'successful': int, 'failed': int, 'results': list[dict], 'errors': list[dict]}`。
- 若 `batch_size < 1`，必须抛出 `ValueError`。
- 不引入外部依赖，仅使用 Python 标准库。

完成标准：`python examples/structured-pipeline/verify.py starter` 成功退出。
