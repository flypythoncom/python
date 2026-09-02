def normalize_product_slug(name: str) -> str:
    """Return a URL-like identifier for a product name."""

    return name.lower().replace(" ", "-")
