import unittest
from ledger import LedgerUnavailable, post


class Client:
    def post(self, cents):
        raise TimeoutError("Provider timeout")


class LedgerTests(unittest.TestCase):
    def test_provider_error_does_not_escape(self):
        with self.assertRaises(LedgerUnavailable):
            post(Client(), 100)
