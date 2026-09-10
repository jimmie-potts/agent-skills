#!/usr/bin/env python3
"""Check the bounded evaluation grader with known broken/working fixtures."""
import os
import hashlib
import json
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

    def test_native_receipt_matches_recorded_bytes(self):
        receipt = json.loads((FIXTURES / 'native-qualification-receipt.json').read_text())
        for name, record in receipt['checks'].items():
            self.assertEqual(hashlib.sha256((FIXTURES / name).read_bytes()).hexdigest(),
                             record['sha256'], name)
        artifacts = {
            'terra_initial_native': 'retry_native_terra.py',
            'terra_initial_injected': 'retry_native_injected.py',
            'terra_correction_native': 'retry_native_terra.py',
            'terra_correction_injected': 'retry_native_injected.py',
            'sol_native': 'retry_native_sol.py',
        }
        self.assertEqual([event['stage'] for event in receipt['events']],
                         list(artifacts))
        outcomes = {}
        for event in receipt['events']:
            artifact = artifacts[event['stage']]
            path = FIXTURES / artifact
            if artifact not in outcomes:
                outcomes[artifact] = self.grade(artifact).returncode
            self.assertEqual(event['exit_code'], outcomes[artifact], event['stage'])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                             event['artifact_sha256'], event['stage'])
            self.assertEqual(event['checker_sha256'],
                             receipt['checks']['test_retry.py']['sha256'])

    def test_native_qualification_proposals(self):
        for implementation in ('retry_native_terra.py', 'retry_native_sol.py'):
            with self.subTest(implementation=implementation):
                result = self.grade(implementation)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_native_injected_candidate_is_rejected(self):
        result = self.grade('retry_native_injected.py')
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('test_nonretryable_propagates_once', result.stderr)
        self.assertIn('3 != 1', result.stderr)
        self.assertIn('FAILED (failures=1)', result.stderr)

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
