import unittest
from service import quote


class QuoteTests(unittest.TestCase):
    def test_empty_cart_and_shipping(self):
        self.assertEqual(quote([], 500), 500)

    def test_aggregation(self):
        self.assertEqual(quote([101, 205], 500), 806)

    def test_rejects_negative_values(self):
        with self.assertRaises(ValueError):
            quote([100, -1], 500)
