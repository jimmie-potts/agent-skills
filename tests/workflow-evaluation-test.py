#!/usr/bin/env python3
"""Check the bounded evaluation grader with known broken/working fixtures."""
import os
import hashlib
import importlib.util
import json
from pathlib import Path
import re
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


class ReviewerCasesTest(unittest.TestCase):
    DIRECTORY = ROOT / 'tests/fixtures/reviewer-cases'
    SOURCE = re.compile(
        r'\[#(\d+)\]\(https://github\.com/jimmie-potts/agent-device-hub/'
        r'(pull|issues)/(\d+)\)')
    SECRET = re.compile(
        r'(?i)["\']?\b(api[_-]?key|token|secret|password|passwd)\b["\']?\s*[:=]'
        r'|(?-i:\bBearer)\s+\S')

    def sections(self, name):
        text = (self.DIRECTORY / name).read_text()
        parts = re.split(r'^## (RV\d\d)\b.*$', text, flags=re.MULTILINE)
        ids = parts[1::2]
        self.assertEqual(len(ids), len(set(ids)), f'{name} repeats a case ID')
        return dict(zip(ids, parts[2::2]))

    def test_inputs_and_graders_pair_up(self):
        cases, graders = self.sections('cases.md'), self.sections('graders.md')
        self.assertGreaterEqual(len(cases), 5)
        self.assertEqual(list(cases), [f'RV{n:02}' for n in range(1, len(cases) + 1)])
        self.assertEqual(list(cases), list(graders))
        for case, body in cases.items():
            with self.subTest(case=case):
                for part in ('**Requirement.**', '**Diff.**', '```diff'):
                    self.assertIn(part, body)

    def test_inputs_carry_no_sources_or_answers(self):
        text = (self.DIRECTORY / 'cases.md').read_text()
        for leak in ('http', 'github', '**Defect.**', '**Source.**',
                     '**Counts when**', 'agent-device-hub'):
            self.assertNotIn(leak, text)
        self.assertIsNone(re.search(r'#\d', text))

    def test_each_grader_links_its_real_miss(self):
        for case, body in self.sections('graders.md').items():
            with self.subTest(case=case):
                for part in ('**Defect.**', '**Counts when**',
                             '**Expected severity.**', '**Near misses.**'):
                    self.assertIn(part, body)
                source = body.split('**Source.**', 1)[1]
                links = self.SOURCE.findall(source)
                self.assertTrue(all(label == number for label, _, number in links))
                self.assertIn('introduced in', ' '.join(source.split()).lower())
                self.assertGreaterEqual(
                    sum(kind == 'pull' for _, kind, _ in links), 2)
                self.assertIn('issues', [kind for _, kind, _ in links])

    def test_cases_stay_synthetic(self):
        for path in self.DIRECTORY.iterdir():
            text = path.read_text()
            with self.subTest(path=path.name):
                self.assertIsNone(re.search(r'\b\d{1,3}(\.\d{1,3}){3}\b', text))
                self.assertIsNone(re.search(r'[\w.+-]+@[\w-]+\.\w', text))
                self.assertNotRegex(text, r'/(Users|home)/\w')
                self.assertIsNone(self.SECRET.search(text))

    def test_secret_pattern_matches_common_shapes(self):
        for sample in ('{"token": "abc"}', '"secret":"x"', 'password = "hunter2"',
                       'Authorization: Bearer abc', 'API_KEY=abc', "'passwd': 'x'"):
            with self.subTest(sample=sample):
                self.assertIsNotNone(self.SECRET.search(sample))
        for sample in ('tokens are refused', 'a secret-free fixture',
                       'no password here', 'bearer of news'):
            with self.subTest(sample=sample):
                self.assertIsNone(self.SECRET.search(sample))

    def test_sections_refuse_a_repeated_case_id(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / 'cases.md').write_text('## RV01: A\nx\n## RV01: B\ny\n')
            original, self.DIRECTORY = self.DIRECTORY, Path(directory)
            try:
                with self.assertRaises(AssertionError):
                    self.sections('cases.md')
            finally:
                self.DIRECTORY = original

    def test_format_names_the_withholding_rule(self):
        text = ' '.join((self.DIRECTORY / 'case-format.md').read_text().split())
        for part in ('`cases.md`', '`graders.md`', 'by access', 'instruction-only',
                     'authorize no trial', 'issues/82'):
            self.assertIn(part, text)


if __name__ == '__main__':
    unittest.main()
