import unittest
from checkout import checkout
from invoice import invoice


class CommerceTests(unittest.TestCase):
    def test_small_order(self):
        self.assertEqual(checkout([1000])["total_cents"], 1500)
        self.assertEqual(invoice([1000])["amount_due"], 1500)

    def test_large_order(self):
        self.assertEqual(checkout([7000])["total_cents"], 7000)
        self.assertEqual(invoice([7000])["amount_due"], 7000)
