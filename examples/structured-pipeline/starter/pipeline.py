from __future__ import annotations


def run_pipeline(items: list[dict], batch_size: int = 2) -> dict:
    """Starter implementation: fragile, does not isolate batch errors, crashes on invalid item."""
    # Bug: ignores batch_size guardrails, directly iterates without error catching or type verification
    results = []
    for item in items:
        # Will crash if id is missing or value is non-positive or wrong type
        results.append({
            "id": item["id"],
            "processed_value": round(item["value"] * 1.1, 2),
        })
    return {
        "total": len(items),
        "successful": len(results),
        "failed": 0,
        "results": results,
        "errors": [],
    }
