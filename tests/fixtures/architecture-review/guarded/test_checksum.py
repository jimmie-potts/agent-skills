import unittest
from checksum import checksum


class ChecksumTests(unittest.TestCase):
    def test_wraparound(self):
        self.assertEqual(checksum([255, 1]), 0)

    def test_empty(self):
        self.assertEqual(checksum([]), 0)
