import re


def normalize_product_slug(name: str) -> str:
    """Return a normalized ASCII URL identifier for a product name."""

    normalized = name.strip().lower()
    normalized = re.sub(r"[\s_-]+", "-", normalized)
    normalized = re.sub(r"[^a-z0-9-]", "", normalized)
    normalized = normalized.strip("-")
    if not normalized:
        raise ValueError("product name must contain an ASCII letter or digit")
    return normalized
