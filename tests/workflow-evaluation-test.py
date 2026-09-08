#!/usr/bin/env python3
"""Check the bounded evaluation grader with known broken/working fixtures."""
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures/workflow-evaluation'


class WorkflowEvaluationTest(unittest.TestCase):
    def grade(self, implementation):
        environment = os.environ.copy()
        environment.update(RETRY_IMPLEMENTATION=str(FIXTURES / implementation),
                           PYTHONDONTWRITEBYTECODE='1')
        return subprocess.run(
            [sys.executable, str(FIXTURES / 'test_retry.py')],
            env=environment, cwd=ROOT, capture_output=True, text=True,
            check=False)

    def test_reference_satisfies_contract(self):
        result = self.grade('retry_reference.py')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_recorded_proposals_satisfy_contract(self):
        for implementation in ('retry_trial1.py', 'retry_trial2.py',
                               'retry_paired1.py', 'retry_paired2.py'):
            with self.subTest(implementation=implementation):
                result = self.grade(implementation)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_grader_rejects_known_contract_defects(self):
        result = self.grade('retry_base.py')
        self.assertEqual(result.returncode, 1, result.stderr)
        for failure in ('test_invalid_limit_has_no_effect',
                        'test_exhaustion_respects_limit',
                        'test_nonretryable_propagates_once',
                        'test_final_exception_identity'):
            self.assertIn(failure, result.stderr)


if __name__ == '__main__':
    unittest.main()
