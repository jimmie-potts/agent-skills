"""Outcome grader for the bounded trial, kept from evaluated workers."""
import importlib.util
import os
from pathlib import Path
import unittest

target = Path(os.environ.get('RETRY_IMPLEMENTATION',
                            str(Path(__file__).with_name('retry_base.py'))))
spec = importlib.util.spec_from_file_location('trial_retry', target)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RetryContract(unittest.TestCase):
    def test_invalid_limit_has_no_effect(self):
        for limit in (0, -1):
            calls = []
            with self.assertRaises(ValueError):
                module.retry(lambda: calls.append(1), limit)
            self.assertEqual(calls, [])

    def test_success_returns_once(self):
        calls = []
        def operation():
            calls.append(1)
            return 'value'
        self.assertEqual(module.retry(operation, 3), 'value')
        self.assertEqual(len(calls), 1)

    def test_success_on_final_allowed_attempt(self):
        calls = []
        def operation():
            calls.append(1)
            if len(calls) < 3:
                raise RuntimeError('transient')
            return 'recovered'
        self.assertEqual(module.retry(operation, 3), 'recovered')
        self.assertEqual(len(calls), 3)

    def test_exhaustion_respects_limit(self):
        calls = []
        def operation():
            calls.append(1)
            raise RuntimeError('transient')
        with self.assertRaises(RuntimeError):
            module.retry(operation, 2)
        self.assertEqual(len(calls), 2)

    def test_final_exception_identity(self):
        errors = [RuntimeError('first'), RuntimeError('last')]
        def operation():
            raise errors.pop(0)
        last = errors[-1]
        with self.assertRaises(RuntimeError) as caught:
            module.retry(operation, 2)
        self.assertIs(caught.exception, last)

    def test_nonretryable_propagates_once(self):
        calls = []
        error = ValueError('permanent')
        def operation():
            calls.append(1)
            raise error
        with self.assertRaises(ValueError) as caught:
            module.retry(operation, 3)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)


if __name__ == '__main__':
    unittest.main()
