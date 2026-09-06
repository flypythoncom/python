# Task contract: build a resilient structured CLI pipeline with exit codes and error handling

Change only `starter/pipeline.py`.

- `run_pipeline(items: list[dict], batch_size: int = 2) -> dict` processes records in batches.
- Each record must be a dict containing non-empty `'id'` (str) and positive `'value'` (int or float).
- Valid items must be transformed into `{'id': item['id'], 'processed_value': round(item['value'] * 1.1, 2)}`.
- Invalid items must not crash the batch; they must be collected in an `'errors'` list with `{'id': item.get('id', 'unknown'), 'reason': str(error)}`.
- The function must return a summary dict: `{'total': int, 'successful': int, 'failed': int, 'results': list[dict], 'errors': list[dict]}`.
- If `batch_size < 1`, raise `ValueError`.
- Do not add external dependencies; use only Python standard library.

Done means `python examples/structured-pipeline/verify.py starter` exits successfully.
