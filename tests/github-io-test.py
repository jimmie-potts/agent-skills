#!/usr/bin/env python3
"""Exercise publication and revision-scoped waits with fake adapters only."""
import importlib.util
from pathlib import Path
import unittest
import tempfile
import sys
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('github_io', ROOT / 'skills/deliver-work/scripts/github_io.py')
io = importlib.util.module_from_spec(spec)
spec.loader.exec_module(io)
HEAD = 'a' * 40
TARGET = dict(repository='owner/repo', pr=42, head=HEAD)
POLICY = dict(source='workflow@' + HEAD, required=['validate', 'depot'], filtered={})


def snapshot(checks=None, **values):
    return dict(TARGET, complete=True, checks=checks or [], **values)


def check(name='validate', status='completed', conclusion='success', **values):
    return dict(name=name, status=status, conclusion=conclusion, head=HEAD,
                association='pull_request:42', id=name + ':1', **values)


class Clock:
    def __init__(self): self.value = 0
    def now(self): return self.value
    def sleep(self, seconds): self.value += seconds


class PublicationTest(unittest.TestCase):
    def test_exact_body_and_ambiguous_write_reconciles_once(self):
        body = '<!-- unique -->\n# Café 雪\n`x` $HOME \'quoted\' "double"\n\n- line\n'
        effects = []
        def write(value):
            effects.append(value)
            raise TimeoutError('lost reply')
        def read():
            return [dict(id=1, body=body, author='owner', url='https://github.com/owner/repo/issues/42#issuecomment-1')]
        result = io.publish(body, '<!-- unique -->', 'owner', write, read)
        self.assertEqual(effects, [body])
        self.assertEqual(result['status'], 'verified')
        self.assertEqual(result['writeCalls'], 1)

    def test_file_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'body.md'
            with self.assertRaises(OSError): io.read_body(path)
            for content in (b'  \n', b'\xff'):
                path.write_bytes(content)
                with self.assertRaises((ValueError, UnicodeError)): io.read_body(path)
            path.write_bytes('雪\n$HOME `code`\n'.encode())
            self.assertEqual(io.read_body(path), '雪\n$HOME `code`\n')

    def test_blank_rejected_before_any_effect(self):
        for body in ('', ' \n\t', None):
            effects = []
            result = io.publish(body, '<!-- unique -->', 'owner', effects.append, lambda: [])
            self.assertEqual(result['status'], 'invalid')
            self.assertEqual(effects, [])

    def test_unknown_write_never_retries(self):
        for rows in ([], [dict(id=1, body='<!-- unique -->changed', author='owner')],
                     [dict(id=1, body='<!-- unique -->body', author='other')],
                     [dict(id=1, body='<!-- unique -->body', author='owner')]*2):
            effects = []
            result = io.publish('<!-- unique -->body', '<!-- unique -->', 'owner', effects.append, lambda: rows)
            self.assertEqual(result['status'], 'unresolved')
            self.assertEqual(len(effects), 1)

    def test_preexisting_reconciled_without_write(self):
        row = dict(id=2, body='<!-- unique -->\r\nbody', author='owner', url='url')
        effects = []
        result = io.publish('<!-- unique -->\nbody', '<!-- unique -->', 'owner', effects.append, lambda:[row], reconcile_only=True)
        self.assertEqual(result['status'], 'verified')
        self.assertEqual(effects, [])


class WaitTest(unittest.TestCase):
    def wait(self, rows, policy=None, cancelled=lambda:False):
        clock = Clock()
        seen = []
        def read(remaining):
            seen.append(remaining)
            value = rows[min(len(seen)-1, len(rows)-1)]
            if isinstance(value, Exception): raise value
            return value
        result = io.wait_checks(TARGET, policy or POLICY, read, budget=3, interval=1,
                                clock=clock.now, sleep=clock.sleep, cancelled=cancelled)
        self.assertLessEqual(clock.value, 3)
        self.assertTrue(all(0 <= value <= 3 for value in seen))
        return result

    def test_delayed_creation_and_provider_neutral_checks(self):
        r = self.wait([snapshot(), snapshot([check(), check('depot', 'in_progress', None)]), snapshot([check(),check('depot')])])
        self.assertEqual(r['status'], 'successful')
        self.assertNotIn('missing', r)
        self.assertNotIn('running', r)

    def test_absence_and_partial_association(self):
        self.assertEqual(self.wait([snapshot()])['status'], 'not-started')
        self.assertEqual(self.wait([snapshot([check()])])['status'], 'not-started')

    def test_terminal_failures_and_missing_required_job(self):
        for outcome in ('failure', 'cancelled', 'skipped', 'neutral', 'timed_out', 'action_required'):
            r = self.wait([snapshot([check(conclusion=outcome), check('depot')])])
            self.assertEqual(r['status'], 'failed')
        self.assertEqual(self.wait([snapshot([check()], association_complete=True)])['status'], 'not-started')

    def test_timeout_running(self):
        r = self.wait([snapshot([check(status='in_progress', conclusion=None),check('depot')])])
        self.assertEqual(r['status'], 'running/time-limit')

    def test_wrong_association_and_head_are_not_success(self):
        for key, value in [('head', 'b'*40), ('association', 'push')]:
            row = check(); row[key] = value
            self.assertEqual(self.wait([snapshot([row,check('depot')])])['status'], 'not-started')
        changed = snapshot(); changed['head'] = 'b'*40
        self.assertEqual(self.wait([changed])['status'], 'stale')

    def test_pagination_errors_and_ambiguous_checks_unavailable(self):
        incomplete = snapshot([check(),check('depot')]); incomplete['complete'] = False
        for row in [incomplete, RuntimeError('API down'), snapshot([check(),check(),check('depot')])]:
            self.assertEqual(self.wait([row])['status'], 'unavailable')

    def test_policy_filter_and_empty_policy(self):
        policy = dict(source='policy@revision', required=['validate','depot'], filtered={'depot':'paths exclude this job for this candidate'})
        self.assertEqual(self.wait([snapshot([check()])], policy)['status'], 'successful')
        for policy in [dict(source='',required=['validate'],filtered={}),dict(source='policy',required=[],filtered={}),
                       dict(source='policy',required=['validate'],filtered={'validate':''})]:
            self.assertEqual(self.wait([snapshot()],policy)['status'], 'unavailable')

    def test_read_overrun_and_cancellation_after_read(self):
        for cancel in (False, True):
            clock = Clock()
            flag = [False]
            def read(remaining):
                clock.value += remaining + 1
                flag[0] = cancel
                return snapshot([check(), check('depot')])
            result = io.wait_checks(TARGET, POLICY, read, budget=3,
                                    clock=clock.now, sleep=clock.sleep,
                                    cancelled=lambda:flag[0])
            self.assertEqual(result['status'], 'cancelled' if cancel else 'unavailable')
            self.assertEqual(result['reads'], 1)

    def test_cancellation_has_zero_reads(self):
        self.assertEqual(self.wait([RuntimeError('must not read')],cancelled=lambda:True)['status'], 'cancelled')


if __name__ == '__main__': unittest.main()
