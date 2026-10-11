#!/usr/bin/env python3
"""Disposable demonstrations of instruction procedures, not a production updater.

Ownership/installation gates are supplied facts; these fixtures do not qualify
host enforcement. Real Git commands and filesystem replacement verify effects.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


def git(path, *args, check=True):
    return subprocess.run(['git', '-C', str(path), *args], check=check,
                          text=True, capture_output=True)


def snapshot(path):
    return (git(path, 'symbolic-ref', '--short', 'HEAD').stdout.strip(),
            git(path, 'rev-parse', 'HEAD').stdout.strip(),
            git(path, 'status', '--porcelain=v1', '--untracked-files=all').stdout)


class CheckoutRefreshTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.remote, self.local, self.delivery = [root / n for n in ('remote', 'canonical', 'delivery')]
        subprocess.run(['git', 'init', '--bare', str(self.remote)], check=True, capture_output=True)
        subprocess.run(['git', 'clone', str(self.remote), str(self.local)], check=True, capture_output=True)
        git(self.local, 'config', 'user.name', 'Synthetic owner')
        git(self.local, 'config', 'user.email', 'fixture@example.invalid')
        git(self.local, 'checkout', '-b', 'trunk')
        (self.local / 'data').write_text('base\n')
        git(self.local, 'add', 'data')
        git(self.local, 'commit', '-m', 'base')
        git(self.local, 'push', 'origin', 'trunk')
        git(self.local, 'worktree', 'add', '-b', 'delivery', str(self.delivery))
        (self.delivery / 'incoming').write_text('delivered\n')
        git(self.delivery, 'add', 'incoming')
        git(self.delivery, 'commit', '-m', 'delivery')
        self.merge = git(self.delivery, 'rev-parse', 'HEAD').stdout.strip()
        git(self.delivery, 'push', 'origin', 'HEAD:trunk')
        self.mutations = 0

    def refresh(self, *, owner=True, pinned=False, installed=False,
                source_only=False, changed=None, uncertain=False, offline=False):
        # This test-only driver exercises the documented order with simulated
        # exclusive ownership and installation routing. It is not shipped code.
        before = snapshot(self.local)
        if offline:
            result = git(self.local, 'fetch', str(self.remote / 'absent'), 'trunk', check=False)
        else:
            result = git(self.local, 'fetch', 'origin', 'trunk', check=False)
        if result.returncode:
            return 'retained/pending'
        target = git(self.local, 'rev-parse', 'FETCH_HEAD').stdout.strip()
        if git(self.local, 'merge-base', '--is-ancestor', self.merge, target, check=False).returncode:
            return 'retained/pending'
        if not owner or pinned or before[0] != 'trunk':
            return 'retained/pending'
        if installed:
            return 'retained/pending' if source_only else 'owning installation procedure'
        if before[2] or git(self.local, 'merge-base', '--is-ancestor', before[1], target, check=False).returncode:
            return 'retained/pending'
        if changed:
            owner = changed()
        if not owner or snapshot(self.local) != before:
            return 'retained/pending'
        if before[1] == target:
            return 'already current'
        self.mutations += 1
        result = git(self.local, 'merge', '--ff-only', target, check=False)
        if result.returncode or uncertain:
            return 'retained/pending'
        return 'updated' if snapshot(self.local) == ('trunk', target, '') else 'retained/pending'

    def test_fast_forward_and_noop(self):
        self.assertEqual(self.refresh(), 'updated')
        self.assertEqual(snapshot(self.local)[1], self.merge)
        self.assertEqual(self.refresh(), 'already current')
        self.assertEqual(self.mutations, 1)

    def test_dirty_and_untracked_collision_preserve_bytes(self):
        for name in ('data', 'incoming'):
            with self.subTest(name=name):
                path = self.local / name
                old = path.read_bytes() if path.exists() else None
                path.write_bytes(b'local owner bytes\n')
                before = snapshot(self.local)
                self.assertEqual(self.refresh(), 'retained/pending')
                self.assertEqual(snapshot(self.local), before)
                self.assertEqual(path.read_bytes(), b'local owner bytes\n')
                if old is None:
                    path.unlink()  # Only this fixture's injected file.
                else:
                    path.write_bytes(old)

    def test_divergence_preserves_local_commit(self):
        (self.local / 'data').write_text('local commit\n')
        git(self.local, 'add', 'data')
        git(self.local, 'commit', '-m', 'local-only')
        before = snapshot(self.local)
        self.assertEqual(self.refresh(), 'retained/pending')
        self.assertEqual(snapshot(self.local), before)

    def test_wrong_branch_pin_unknown_or_conflicting_owner(self):
        before = snapshot(self.local)
        for options in ({'pinned': True}, {'owner': False}, {'owner': None}):
            self.assertEqual(self.refresh(**options), 'retained/pending')
            self.assertEqual(snapshot(self.local), before)
        git(self.local, 'checkout', '-b', 'other')  # Fixture setup, never updater.
        before = snapshot(self.local)
        self.assertEqual(self.refresh(), 'retained/pending')
        self.assertEqual(snapshot(self.local), before)

    def test_lost_ownership_and_changed_preflight(self):
        self.assertEqual(self.refresh(changed=lambda: False), 'retained/pending')
        self.assertEqual(self.mutations, 0)
        def dirty():
            (self.local / 'late').write_text('other writer\n')
            return True
        self.assertEqual(self.refresh(changed=dirty), 'retained/pending')
        self.assertEqual((self.local / 'late').read_text(), 'other writer\n')
        self.assertEqual(self.mutations, 0)

    def test_installation_routing_source_only_and_offline(self):
        before = snapshot(self.local)
        self.assertEqual(self.refresh(installed=True), 'owning installation procedure')
        self.assertEqual(self.refresh(installed=True, source_only=True), 'retained/pending')
        self.assertEqual(self.refresh(offline=True), 'retained/pending')
        self.assertEqual(snapshot(self.local), before)
        self.assertEqual(self.mutations, 0)

    def test_git_lock_failure_preserves_state(self):
        lock = self.local / '.git/index.lock'
        lock.write_text('synthetic competing lock\n')
        before = snapshot(self.local)
        self.assertEqual(self.refresh(), 'retained/pending')
        self.assertEqual(snapshot(self.local), before)
        self.assertEqual(lock.read_text(), 'synthetic competing lock\n')

    def test_lost_response_reconciles_without_repeat_mutation(self):
        self.assertEqual(self.refresh(uncertain=True), 'retained/pending')
        self.assertEqual(snapshot(self.local)[1], self.merge)
        self.assertEqual(self.refresh(), 'already current')
        self.assertEqual(self.mutations, 1)


class RecoveryReplacementTest(unittest.TestCase):
    def test_history_preservation_and_interrupted_replacement(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reports = root / 'reports'
            reports.mkdir()
            # Required current facts stay directly available. The evidence index
            # names an immutable inventory rather than embedding every report.
            facts = dict(work='acme/search#4', authority='ready-PR-only', owner='C',
                         candidate='H3/D3', accepted='H3 local checks', pending='CI',
                         corrections=2, rounds=3, attempts=1, start='T0',
                         elapsed='6h', deadline='T10', effect='K3/P3 unknown',
                         next='reconcile publication', evidence='reports/index.json')
            for i in range(40):
                (reports / f'round-{i}.txt').write_text(f'B0/H{i} immutable review/failure\n')
            hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in reports.iterdir()}
            (reports / 'index.json').write_text(json.dumps(hashes, sort_keys=True))
            record = root / 'RESUME.md'
            current = json.dumps(facts, sort_keys=True) + '\n'
            legacy = current + ('superseded checkpoint\n' * 1000)
            record.write_text(legacy)
            original = root / 'legacy-original.md'
            original.write_bytes(record.read_bytes())
            staged = root / 'RESUME.next'
            staged.write_text(current)
            # Interrupted preparation still leaves the old valid record.
            self.assertEqual(record.read_text(), legacy)
            self.assertEqual(json.loads(staged.read_text()), facts)
            os.replace(staged, record)
            self.assertEqual(json.loads(record.read_text()), facts)
            self.assertEqual(original.read_text(), legacy)
            before_size = record.stat().st_size
            # More completed history at equivalent active state does not change R.
            (reports / 'older-checkpoints.md').write_text('historical detail\n' * 2000)
            self.assertEqual(record.stat().st_size, before_size)
            for name, digest in hashes.items():
                self.assertEqual(hashlib.sha256((reports / name).read_bytes()).hexdigest(), digest)
            # A path alone cannot turn changed/missing evidence into acceptance.
            linked = reports / 'round-3.txt'
            linked.write_text('changed bytes\n')
            self.assertNotEqual(hashlib.sha256(linked.read_bytes()).hexdigest(), hashes[linked.name])


if __name__ == '__main__':
    unittest.main()
