import unittest

from product_slug import normalize_product_slug


class NormalizeProductSlugTests(unittest.TestCase):
    def test_lowercases_and_joins_words(self) -> None:
        self.assertEqual(normalize_product_slug("Good Python Product"), "good-python-product")

    def test_collapses_mixed_separators(self) -> None:
        self.assertEqual(normalize_product_slug("  API__Agent---Kit  "), "api-agent-kit")

    def test_removes_punctuation(self) -> None:
        self.assertEqual(normalize_product_slug("MCP: Tools!"), "mcp-tools")

    def test_rejects_an_empty_result(self) -> None:
        with self.assertRaises(ValueError):
            normalize_product_slug(" -- !! ")


if __name__ == "__main__":
    unittest.main()
