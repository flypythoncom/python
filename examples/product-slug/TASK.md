# Task contract: normalize a product slug

Change only `starter/product_slug.py`.

- `normalize_product_slug(name)` returns a lowercase ASCII slug.
- A run of whitespace, `_`, or `-` becomes one `-`.
- Other punctuation is removed without creating duplicate separators.
- Leading and trailing separators are removed.
- An empty result raises `ValueError`.
- Do not add dependencies or change tests.

Done means `python examples/product-slug/verify.py starter` exits successfully.
