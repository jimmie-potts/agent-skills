#!/usr/bin/env python3
"""Action-spy integration tests; no live provider mutation."""
import importlib.util
from pathlib import Path
import sys
import unittest
import json
from copy import deepcopy
from datetime import datetime, timezone
from unittest.mock import patch
from types import SimpleNamespace
sys.dont_write_bytecode = True
PATH = Path(__file__).resolve().parents[1] / 'skills/deliver-work/scripts/merge_guard.py'
SPEC = importlib.util.spec_from_file_location('merge_guard', PATH)
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


TIME = datetime(2026, 10, 1, 12, tzinfo=timezone.utc)


def binding():
    return dict(repository='owner/repo', pr=7, baseRef='main', base='a'*40,
                head='b'*40, mergeBase='a'*40, strategy='squash',
                requiredGates=['identity', 'ci-pr', 'review'])


def candidate():
    return dict(repository='owner/repo', pr=7, baseRef='main', base='a'*40,
                head='b'*40, mergeBase='a'*40, state='open', draft=False)


def report():
    return dict(tool='delivery-preflight', schema=1, readAt=TIME.isoformat(),
                candidate=candidate(), result='satisfied', exitCode=0, readFailures=[],
                gates=[dict(id=name, status='satisfied', rule='repository-policy',
                            reasons=[], evidence={'source': 'fixture-evidence'})
                       for name in binding()['requiredGates']])


def exercise(document=None, live=None, exit_code=0, output=None, execute=True, merge_error=None):
    events = []
    def preflight(expected):
        events.append('preflight')
        return exit_code, output if output is not None else json.dumps(document or report())
    def read(expected):
        events.append('read')
        if isinstance(live, Exception): raise live
        return deepcopy(live if live is not None else candidate())
    def merge(expected):
        events.append(('merge', deepcopy(expected)))
        if merge_error: raise merge_error
        return {'exitCode': 0}
    result = guard.run_guard(binding(), preflight, read, merge, execute=execute, clock=lambda: TIME)
    return result, events


class GuardTests(unittest.TestCase):
    def test_failed_preflight_has_zero_merge_calls(self):
        for code in (1, 2, 3, -1):
            result, events = exercise(exit_code=code)
            self.assertEqual(result['status'], 'blocked')
            self.assertEqual(events, ['preflight'])

    def test_failed_or_missing_evidence_blocks(self):
        variants = []
        for key, value in [('candidate', None), ('result', 'unresolved'), ('exitCode', 1),
                           ('readFailures', [{}]), ('gates', []), ('readAt', '2026-09-01T00:00:00Z')]:
            item = report(); item[key] = value; variants.append(item)
        for key, value in [('status', 'incomplete'), ('status', 'read-failure'),
                           ('status', 'not-evaluated'), ('status', 'pending'),
                           ('evidence', None), ('evidence', {}), ('rule', '')]:
            item = report(); item['gates'][0][key] = value; variants.append(item)
        item = report(); item['gates'].pop(); variants.append(item)
        item = report(); item['gates'].append(deepcopy(item['gates'][0])); variants.append(item)
        for item in variants:
            result, events = exercise(document=item)
            self.assertEqual(result['status'], 'blocked', item)
            self.assertEqual(events, ['preflight'], item)
        for output in ('{', 'null', '[]', '{}', 'npm banner\n{}'):
            result, events = exercise(output=output)
            self.assertEqual(result['mergeCalls'], 0)

    def test_wrong_identity_in_report_or_final_read_blocks(self):
        for key, value in [('repository', 'other/repo'), ('pr', 8), ('baseRef', 'other'),
                           ('head', 'c'*40), ('base', 'c'*40), ('mergeBase', 'c'*40),
                           ('state', 'closed'), ('draft', True)]:
            with self.subTest(key=key):
                item = report(); item['candidate'][key] = value
                self.assertEqual(exercise(document=item)[0]['mergeCalls'], 0)
                live = candidate(); live[key] = value
                result, events = exercise(live=live)
                self.assertEqual(result['mergeCalls'], 0)
                self.assertEqual(events, ['preflight', 'read'])

    def test_unavailable_read_and_preflight_exception_block(self):
        self.assertEqual(exercise(live=OSError('offline'))[0]['mergeCalls'], 0)
        calls = []
        def failing(_): raise TimeoutError('timed out')
        result = guard.run_guard(binding(), failing, lambda _: candidate(), lambda _: calls.append(1))
        self.assertEqual(result['status'], 'blocked'); self.assertEqual(calls, [])

    def test_satisfied_action_once_followed_by_readback(self):
        result, events = exercise()
        self.assertEqual(events, ['preflight', 'read', ('merge', binding()), 'read'])
        self.assertEqual(result['status'], 'reconcile')
        self.assertEqual(result['mergeCalls'], 1)

    def test_check_mode_is_read_only(self):
        result, events = exercise(execute=False)
        self.assertEqual(result['status'], 'checked')
        self.assertEqual(events, ['preflight', 'read'])

    def test_head_rejection_and_ambiguous_response_never_retry(self):
        for error in (TimeoutError('ambiguous'), OSError('head rejected')):
            result, events = exercise(merge_error=error)
            self.assertEqual(result['status'], 'reconcile')
            self.assertEqual(result['mergeCalls'], 1)
            self.assertEqual(events[-1], 'read')
            self.assertEqual(sum(isinstance(x, tuple) for x in events), 1)

    def test_success_requires_identity_and_merge_revision_readback(self):
        reads = 0
        def read(_):
            nonlocal reads
            reads += 1
            value = candidate()
            if reads == 2: value.update(state='merged', mergeCommit='d'*40)
            return value
        result = guard.run_guard(binding(), lambda _: (0, json.dumps(report())), read,
                                 lambda _: {'exitCode': 0}, execute=True, clock=lambda: TIME)
        self.assertEqual(result['status'], 'merged-readback')

    def test_server_base_race_is_not_claimed_atomic(self):
        # Server base moves after the final read; only server protections can guard this.
        live = candidate(); events = []
        def merge(_): live['base'] = 'c'*40; events.append('merge'); return {'exitCode': 0}
        result = guard.run_guard(binding(), lambda _: (0, json.dumps(report())), lambda _: deepcopy(live),
                                 merge, execute=True, clock=lambda: TIME)
        self.assertEqual(events, ['merge'])
        self.assertIn('server race remains', result['baseGuard'])
        self.assertEqual(result['status'], 'reconcile')

    def test_normal_merge_argv_has_exact_head_guard_and_no_bypass(self):
        with patch.object(guard, 'command', return_value=SimpleNamespace(returncode=0, stdout='', stderr='')) as command:
            guard.github_merge(binding())
        self.assertEqual(command.call_args.args[0], ['gh', 'pr', 'merge', '7', '--repo',
                         'https://github.com/owner/repo', '--squash', '--match-head-commit', 'b'*40])

    def test_project_not_applicable_exception_is_preserved(self):
        item = report()
        item['gates'].append(dict(id='ci-main', status='not-applicable', rule='project-policy',
                                  reasons=['applies after merge'], evidence={}))
        self.assertEqual(exercise(document=item, execute=False)[0]['status'], 'checked')
        item['gates'][-1]['reasons'] = []
        self.assertEqual(exercise(document=item)[0]['mergeCalls'], 0)

    def test_representative_hub_preflight_keeps_every_gate(self):
        document = json.loads((PATH.parents[3] / 'tests/fixtures/merge-guard/hub-source.json').read_text())
        expected = binding()
        expected.update(repository=document['candidate']['repository'], pr=999,
                        requiredGates=[g['id'] for g in document['gates']])
        calls = []
        def check(value):
            return guard.run_guard(expected, lambda _: (0, json.dumps(value)),
                                   lambda _: document['candidate'], lambda _: calls.append(1),
                                   execute=True, clock=lambda: TIME)
        self.assertEqual(check(document)['mergeCalls'], 1)
        self.assertEqual(calls, [1])
        for index in range(len(document['gates'])):
            changed = deepcopy(document); changed['gates'][index]['status'] = 'unresolved'
            self.assertEqual(check(changed)['mergeCalls'], 0)
        changed = deepcopy(document); changed['gates'].pop()
        self.assertEqual(check(changed)['mergeCalls'], 0)
        # A guide-only CI exception remains the project's evaluated evidence.
        changed = deepcopy(document)
        changed['gates'][1]['evidence'] = {'mode':'guide-only-exception', 'revision':'b'*40,
                                          'receipt':'fixture-guide-receipt', 'record':'fixture-guide-record'}
        self.assertEqual(check(changed)['mergeCalls'], 1)


if __name__ == '__main__':
    unittest.main()
