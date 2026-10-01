#!/usr/bin/env python3
"""Small publication and bounded check-wait primitives for trusted GitHub adapters.

No credential setup, generic command dispatch, workflow reruns or issue changes.
Callbacks are trusted I/O boundaries, not a sandbox. See github-io.md.
"""
from copy import deepcopy
from pathlib import Path
import math
import re
import time


def normalized(body):
    return body.replace('\r\n', '\n').replace('\r', '\n')


def read_body(path):
    """Read a UTF-8 body before dispatch; reject unreadable or whitespace-only input."""
    body = Path(path).read_bytes().decode('utf-8')
    _require(body.strip(), 'empty publication body')
    return body


def publish(body, marker, author, write, read, *, reconcile_only=False):
    """One write at most; reconcile uncertain prior attempts without another write.

    write(body) uses a structured body or UTF-8 body-file argument. read() must
    return all pages for the selected target, or raise. Caller owns authority,
    target binding and durable intent/receipt storage across invocations.
    """
    receipt = dict(status='invalid', writeCalls=0)
    if (not isinstance(body, str) or not body.strip() or not isinstance(marker, str)
            or not marker.strip() or not body.startswith(marker)
            or not isinstance(author, str) or not author.strip()):
        return dict(receipt, reason='nonempty body, leading publication marker and author required')
    receipt['status'] = 'unresolved'
    if not reconcile_only:
        receipt['writeCalls'] = 1
        try:
            receipt['response'] = write(body)
        except Exception as error:
            receipt['writeError'] = str(error)
    try:
        rows = read()
        if not isinstance(rows, list):
            raise ValueError('readback must contain all pages')
        matches = [row for row in rows if row.get('author') == author
                   and isinstance(row.get('body'), str) and row['body'].startswith(marker)]
        if len(matches) == 1 and matches[0].get('id') and matches[0].get('url'):
            if normalized(matches[0]['body']) == normalized(body):
                receipt.update(status='verified', object=matches[0])
                return receipt
        receipt['reason'] = 'missing, ambiguous or changed authoritative publication identity/body'
    except Exception as error:
        receipt['readError'] = str(error)
    return receipt


def _require(condition, reason):
    if not condition:
        raise ValueError(reason)


def _policy(target, policy):
    _require(isinstance(target, dict) and re.fullmatch(r'[\w.-]+/[\w.-]+', target.get('repository', '')),
             'invalid repository')
    _require(type(target.get('pr')) is int and target['pr'] > 0, 'invalid PR')
    _require(isinstance(target.get('head'), str) and re.fullmatch('[0-9a-f]{40}', target['head']), 'invalid head')
    _require(isinstance(policy, dict) and isinstance(policy.get('source'), str) and policy['source'].strip(), 'missing policy source')
    required = policy.get('required')
    _require(isinstance(required, list) and required and all(isinstance(x, str) and x.strip() for x in required), 'empty or invalid required checks')
    _require(len(set(required)) == len(required), 'duplicate required checks')
    filtered = policy.get('filtered')
    _require(isinstance(filtered, dict) and set(filtered) <= set(required)
             and all(isinstance(x, str) and x.strip() for x in filtered.values()), 'invalid intentional filter evidence')
    # An entirely filtered set needs a distinct project-owned no-CI decision;
    # this check-wait helper does not certify that decision as successful CI.
    selected = set(required) - set(filtered)
    _require(selected, 'no applicable checks; cannot claim green CI')
    return selected


def evaluate(target, policy, snapshot):
    """Classify a complete normalized read. Never infer applicability from absence."""
    wanted = _policy(target, policy)
    _require(isinstance(snapshot, dict), 'malformed check snapshot')
    if any(snapshot.get(key) != target[key] for key in ('repository', 'pr', 'head')):
        return dict(status='stale', reason='selected repository/PR/head changed')
    _require(snapshot.get('complete') is True, 'missing pages or incomplete provider reads')
    checks = snapshot.get('checks')
    _require(isinstance(checks, list), 'missing check list')
    applicable = {}
    for row in checks:
        _require(isinstance(row, dict), 'malformed check row')
        if row.get('head') != target['head'] or row.get('association') != f'pull_request:{target["pr"]}':
            continue
        name = row.get('name')
        if name not in wanted:
            continue
        _require(name not in applicable, 'ambiguous current check attempts; adapter must select latest applicable attempt')
        _require(bool(row.get('id')), 'missing provider check identity')
        _require(row.get('status') in ('queued', 'in_progress', 'completed'), 'unknown check status')
        applicable[name] = row
    missing = sorted(wanted - applicable.keys())
    failed = sorted(name for name, row in applicable.items()
                    if row['status'] == 'completed' and row.get('conclusion') != 'success')
    if failed:
        return dict(status='failed', failed=failed, missing=missing)
    if missing:
        return dict(status='not-started', missing=missing)
    running = sorted(name for name, row in applicable.items() if row['status'] != 'completed')
    if running:
        return dict(status='running/time-limit', running=running)
    return dict(status='successful')


def wait_checks(target, policy, read, *, budget, interval=5, clock=time.monotonic,
                sleep=time.sleep, cancelled=lambda: False):
    """Bounded read-only wait using a trusted read(remaining_seconds) adapter.

    read must honor the supplied remaining I/O budget across every page and
    refresh the PR head with each snapshot. It supplies latest applicable
    checks from Actions, check-run providers (including Depot), or statuses.
    The adapter, not the helper, discovers policy and verifies associations.
    """
    receipt = dict(status='unavailable', reads=0)
    try:
        target, policy = deepcopy(target), deepcopy(policy)
        _policy(target, policy)
        _require(type(budget) in (int, float) and math.isfinite(budget) and budget > 0, 'budget must be finite and positive')
        _require(type(interval) in (int, float) and math.isfinite(interval) and interval > 0, 'interval must be finite and positive')
        deadline = clock() + budget
        receipt.update(target=target, policy=policy)
        while True:
            if cancelled():
                return dict(receipt, status='cancelled')
            remaining = deadline - clock()
            if remaining <= 0:
                return dict(receipt, timeLimit=True)
            receipt['reads'] += 1
            snapshot = read(remaining)
            result = evaluate(target, policy, snapshot)
            for key in ('missing', 'running', 'failed', 'reason'):
                receipt.pop(key, None)
            receipt.update(result, snapshot=snapshot)
            if cancelled():
                return dict(receipt, status='cancelled')
            # A late read cannot be claimed as a within-budget success.
            if clock() > deadline:
                return dict(receipt, status='unavailable', reason='adapter exceeded read budget', timeLimit=True)
            if result['status'] in ('successful', 'failed', 'stale'):
                return receipt
            remaining = deadline - clock()
            if remaining <= 0:
                return dict(receipt, timeLimit=True)
            sleep(min(interval, remaining))
    except Exception as error:
        return dict(receipt, status='unavailable', reason=str(error))
