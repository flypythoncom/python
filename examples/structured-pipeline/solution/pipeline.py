from __future__ import annotations


def run_pipeline(items: list[dict], batch_size: int = 2) -> dict:
    """Robust pipeline implementation with isolation and input boundaries."""
    if batch_size < 1:
        raise ValueError("batch_size must be >= 1")

    results = []
    errors = []

    for item in items:
        try:
            if not isinstance(item, dict):
                raise TypeError("Record must be a dictionary")

            raw_id = item.get("id")
            if not isinstance(raw_id, str) or not raw_id.strip():
                raise ValueError("Record 'id' must be a non-empty string")

            value = item.get("value")
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise TypeError("Record 'value' must be a numeric int or float")

            if value <= 0:
                raise ValueError("Record 'value' must be positive")

            results.append({
                "id": raw_id,
                "processed_value": round(value * 1.1, 2),
            })
        except Exception as exc:
            item_id = item.get("id", "unknown") if isinstance(item, dict) else "unknown"
            errors.append({
                "id": str(item_id) if item_id else "unknown",
                "reason": str(exc),
            })

    return {
        "total": len(items),
        "successful": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors,
    }
