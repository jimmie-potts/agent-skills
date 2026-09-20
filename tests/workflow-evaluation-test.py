#!/usr/bin/env python3
"""Check the bounded evaluation grader with known broken/working fixtures."""
import os
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures/workflow-evaluation'
MEASURE_SPEC = importlib.util.spec_from_file_location(
    'context_measure', ROOT / 'tests/context-reporting-measure.py')
MEASURE = importlib.util.module_from_spec(MEASURE_SPEC)
MEASURE_SPEC.loader.exec_module(MEASURE)


class ContextMeasurementTest(unittest.TestCase):
    def response(self):
        return {
            'sources': ['AGENTS.md'],
            'cases': [dict(id=f'L{i}', host=host, reads=['AGENTS.md', 'AGENTS.md'],
                           worker_reads=['AGENTS.md'], brief='é 猫',
                           **{'return': '', 'updates': []})
                      for i in range(1, 6) for host in ('codex', 'claude')],
        }

    def test_counts_exact_unicode_bytes_words_and_role_exposures(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'AGENTS.md').write_bytes(b'one\r\ntwo\n')
            response = self.response()
            response['sources'].append('external: /not-readable/fixture.md')
            response['sources'].append(MEASURE.FIXED_INPUT)
            receipt = MEASURE.measure(root, response, 'fixture')
        first = receipt['cases'][0]
        self.assertEqual(first['messages']['brief'], {'bytes': 6, 'words': 2})
        self.assertEqual(first['messages']['return'], {'bytes': 0, 'words': 0})
        self.assertEqual(first['coordinator_actual']['bytes'], 9)
        self.assertEqual(first['worker_proposed']['bytes'], 9)
        self.assertEqual(receipt['combined_union']['bytes'], 9)
        self.assertEqual(receipt['external_sources_excluded'],
                         ['external: /not-readable/fixture.md'])
        self.assertEqual(receipt['fixed_inputs_excluded'], [MEASURE.FIXED_INPUT])
        self.assertEqual(receipt['source_inventory']['AGENTS.md']['sha256'],
                         hashlib.sha256(b'one\r\ntwo\n').hexdigest())

    def test_rejects_missing_duplicate_cases_and_undeclared_reads(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for defect in ('missing', 'duplicate', 'undeclared'):
                response = self.response()
                if defect == 'missing':
                    response['cases'].pop()
                elif defect == 'duplicate':
                    response['cases'][-1] = response['cases'][0]
                else:
                    response['sources'] = []
                with self.subTest(defect=defect), self.assertRaises(ValueError):
                    MEASURE.measure(root, response, 'fixture')

    def test_rejects_paths_outside_instruction_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'skills').mkdir()
            (root / 'skills/escape.md').symlink_to(root.parent / 'outside.md')
            (root / 'AGENTS.md').write_text('instructions')
            (root / 'skills/alias.md').symlink_to(root / 'AGENTS.md')
            for name in ('../outside.md', '/outside.md', 'skills/../AGENTS.md',
                         'skills//x.md', 'skills/x.env', 'other.md',
                         'skills/escape.md', 'skills/alias.md'):
                with self.subTest(path=name), self.assertRaises(ValueError):
                    MEASURE.source_path(root, name)


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
