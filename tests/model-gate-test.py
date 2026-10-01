#!/usr/bin/env python3
"""Behavioral policy tests with synthetic evidence, not host qualification."""
import importlib.util
from pathlib import Path
import unittest
import json
import subprocess
import sys
from copy import deepcopy

sys.dont_write_bytecode = True

PATH = Path(__file__).resolve().parents[1] / 'skills/deliver-work/scripts/model_gate.py'
SPEC = importlib.util.spec_from_file_location('model_gate', PATH)
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def request(**changes):
    setting = dict(name='model', value='model-a', required=True,
                   verified=False, observed=[], declared=[], requested=[])
    setting.update(changes)
    return dict(role='coordinator', phase='pickup', settings=[setting], aliases=[])


def evidence(value):
    return dict(value=value, source='synthetic host record')


class ModelGateTests(unittest.TestCase):
    def test_required_mismatch_never_calls_action(self):
        calls = []
        result = gate.run_if_allowed(request(observed=[evidence('model-b')]),
                                     lambda: calls.append('implementation'))
        self.assertEqual(result['decision'], 'stop')
        self.assertEqual(calls, [])

    def test_decision_cases_and_action_counts(self):
        cases = [
            ('match', request(observed=[evidence('model-a')]), 'continue'),
            ('conflict', request(observed=[evidence('model-a'), evidence('model-b')]), 'stop'),
            ('declared', request(declared=[evidence('model-a')]), 'continue'),
            ('missing', request(), 'ask'),
            ('request is not evidence', request(requested=[evidence('model-a')]), 'ask'),
            ('advisory difference', request(required=False, observed=[evidence('model-b')]), 'continue'),
            ('advisory unknown', request(required=False), 'continue'),
            ('unproved alias', request(observed=[evidence('alias-a')]), 'stop'),
            ('verified required', request(verified=True, declared=[evidence('model-a')]), 'stop'),
            ('verified match', request(verified=True, observed=[evidence('model-a')]), 'continue'),
            ('observed overrides declaration', request(observed=[evidence('model-b')], declared=[evidence('model-a')]), 'stop'),
            ('old declaration retained', request(observed=[evidence('model-a')], declared=[evidence('model-b')]), 'continue'),
            ('declared mismatch', request(declared=[evidence('model-b')]), 'stop'),
            ('conflicting declarations', request(declared=[evidence('model-a'), evidence('model-b')]), 'stop'),
        ]
        for label, document, expected in cases:
            for phase in ('pickup', 'resume', 'setting-change'):
                with self.subTest(case=label, phase=phase):
                    document['phase'] = phase
                    calls = []
                    result = gate.run_if_allowed(document, lambda: calls.append('delegate'))
                    self.assertEqual(result['decision'], expected)
                    self.assertEqual(len(calls), int(expected == 'continue'))
                    self.assertEqual(result['settings'][0]['evidence'], document['settings'][0])

    def test_declaration_fallback_never_claims_runtime_verification(self):
        result = gate.evaluate(request(declared=[evidence('model-a')]))
        self.assertEqual(result['settings'][0]['runtime_verification'], 'unknown')
        self.assertEqual(result['settings'][0]['reason'], 'declaration only')

    def test_alias_requires_provenance_and_is_setting_scoped(self):
        document = request(observed=[evidence('alias-a')])
        document['aliases'] = [dict(name='model', alias='alias-a', canonical='model-a', source='qualified provider mapping')]
        self.assertEqual(gate.evaluate(document)['decision'], 'continue')
        document['aliases'][0]['name'] = 'reasoning'
        self.assertEqual(gate.evaluate(document)['decision'], 'stop')
        document['aliases'][0]['source'] = ''
        self.assertEqual(gate.evaluate(document)['decision'], 'stop')

    def test_separate_roles_and_unknown_effort(self):
        for role in ('coordinator', 'worker-1', 'standards-reviewer'):
            document = request(observed=[evidence('model-a')])
            document['role'] = role
            setting = request(name='reasoning', value='high', required=False)['settings'][0]
            document['settings'].append(setting)
            result = gate.evaluate(document)
            self.assertEqual(result['role'], role)
            self.assertEqual(result['settings'][1]['runtime_verification'], 'unknown')
            setting['required'] = True
            self.assertEqual(gate.evaluate(document)['decision'], 'ask')

    def test_malformed_evidence_fails_closed(self):
        valid = request(observed=[evidence('model-a')])
        variants = [None, [], {}, dict(valid, settings=[]), dict(valid, phase='later')]
        for field, value in [('observed', None), ('declared', ['model-a']),
                             ('required', 'yes'), ('value', ''), ('requested', [{}])]:
            document = deepcopy(valid)
            document['settings'][0][field] = value
            variants.append(document)
        for document in variants:
            calls = []
            self.assertEqual(gate.run_if_allowed(document, lambda: calls.append(1))['decision'], 'stop')
            self.assertEqual(calls, [])

    def test_prelaunch_only_permits_bootstrap_not_assignment(self):
        for verified in (False, True):
            document = request(verified=verified, requested=[evidence('model-a')])
            document['phase'] = 'pre-launch'
            calls = []
            result = gate.run_if_allowed(document, lambda: calls.append('work'))
            self.assertEqual(result['decision'], 'bootstrap-only')
            self.assertEqual(result['settings'][0]['runtime_verification'], 'unknown')
            self.assertEqual(calls, [])
            document['phase'] = 'pickup'
            self.assertEqual(gate.evaluate(document)['decision'], 'ask')
            document['settings'][0]['declared'] = [evidence('model-a')]
            self.assertEqual(gate.evaluate(document)['decision'], 'stop' if verified else 'continue')
        for values, outcome in [([], 'ask'), ([evidence('model-b')], 'stop')]:
            document = request(requested=values)
            document['phase'] = 'pre-launch'
            self.assertEqual(gate.evaluate(document)['decision'], outcome)

    def test_cli_reports_unknown_and_nonzero_blocks(self):
        for document, expected in [(request(), 2), (request(observed=[evidence('model-b')]), 1),
                                   (request(declared=[evidence('model-a')]), 0)]:
            completed = subprocess.run([sys.executable, str(PATH), '-'], input=json.dumps(document),
                                       text=True, capture_output=True)
            self.assertEqual(completed.returncode, expected)
            self.assertIn(json.loads(completed.stdout)['decision'], ('continue', 'ask', 'stop'))
        completed = subprocess.run([sys.executable, str(PATH), '-'], input='{', text=True, capture_output=True)
        self.assertEqual(completed.returncode, 1)


if __name__ == '__main__':
    unittest.main()
