#!/usr/bin/env python3
"""Couple a repository-owned preflight to one explicitly authorized GitHub merge."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import json
import re
import subprocess
import sys
from urllib.parse import quote


class Blocked(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Blocked(reason)


def binding(value):
    require(isinstance(value, dict), 'missing binding')
    require(set(value) == {'repository', 'pr', 'baseRef', 'base', 'head', 'mergeBase',
                           'strategy', 'requiredGates'}, 'missing or unexpected binding fields')
    require(isinstance(value['repository'], str) and re.fullmatch(r'[\w.-]+/[\w.-]+', value['repository']), 'invalid repository')
    require(type(value['pr']) is int and value['pr'] > 0, 'invalid PR')
    require(isinstance(value['baseRef'], str) and value['baseRef'] and not value['baseRef'].startswith('-'), 'invalid base ref')
    for key in ('base', 'head', 'mergeBase'):
        require(isinstance(value[key], str) and re.fullmatch('[0-9a-f]{40}', value[key]), f'invalid {key}')
    require(value['strategy'] in ('merge', 'squash', 'rebase'), 'invalid merge strategy')
    gates = value['requiredGates']
    require(isinstance(gates, list) and gates and all(isinstance(x, str) and x for x in gates), 'missing required gate list')
    require(len(set(gates)) == len(gates), 'duplicate required gate')


def same_candidate(candidate, expected):
    require(isinstance(candidate, dict), 'missing candidate identity')
    for key in ('repository', 'pr', 'baseRef', 'base', 'head', 'mergeBase'):
        require(type(candidate.get(key)) is type(expected[key]) and candidate[key] == expected[key], f'changed or wrong {key}')
    require(candidate.get('state') == 'open' and candidate.get('draft') is False, 'candidate is not open and ready')


def check_report(report, expected, started, finished):
    require(isinstance(report, dict), 'malformed preflight report')
    require(report.get('result') == 'satisfied' and type(report.get('exitCode')) is int and report['exitCode'] == 0, 'preflight is not satisfied')
    require(report.get('readFailures') == [], 'missing or failed reads')
    same_candidate(report.get('candidate'), expected)
    read_at = datetime.fromisoformat(report['readAt'].replace('Z', '+00:00'))
    require(read_at.tzinfo is not None and started <= read_at <= finished, 'preflight report is stale or future-dated')
    gates = report.get('gates')
    require(isinstance(gates, list) and gates, 'missing gate evidence')
    seen = set()
    for gate in gates:
        require(isinstance(gate, dict), 'malformed gate')
        name = gate.get('id')
        require(isinstance(name, str) and name and name not in seen, 'missing or duplicate gate ID')
        seen.add(name)
        require(gate.get('status') in ('satisfied', 'not-applicable'), f'unresolved gate: {name}')
        require(isinstance(gate.get('rule'), str) and gate['rule'].strip(), f'missing rule: {name}')
        require(isinstance(gate.get('evidence'), dict), f'missing evidence: {name}')
        reasons = gate.get('reasons')
        require(isinstance(reasons, list) and all(isinstance(x, str) and x.strip() for x in reasons), f'malformed reasons: {name}')
        require(bool(reasons) or bool(gate['evidence']), f'empty evidence: {name}')
        if gate['status'] == 'not-applicable':
            require(bool(reasons), f'missing exception reason: {name}')
    require(set(expected['requiredGates']) <= seen, 'missing required gate')


def now():
    return datetime.now(timezone.utc)


def run_guard(expected, preflight, read_candidate, merge, *, execute=False, clock=now):
    """Trusted adapters own policy; this function owns ordering and the action count.

    Callbacks: preflight(binding)->(exit, JSON text); read_candidate(binding)->
    candidate; merge(binding)->opaque provider response. Never retries a merge.
    """
    expected = deepcopy(expected)
    receipt = {'status': 'blocked', 'mergeCalls': 0, 'binding': expected,
               'baseGuard': 'pre-dispatch read only; server race remains'}
    try:
        binding(expected)
        started = clock()
        code, output = preflight(deepcopy(expected))
        require(type(code) is int and code == 0, 'preflight command failed')
        report = json.loads(output)
        check_report(report, expected, started, clock())
        # Keep this fresh read next to dispatch. No repair or retry in between.
        same_candidate(read_candidate(deepcopy(expected)), expected)
        if not execute:
            return dict(receipt, status='checked', preflight=report)
    except Exception as error:
        return dict(receipt, reason=str(error))
    receipt.update(status='reconcile', mergeCalls=1, preflight=report)
    try:
        receipt['response'] = merge(deepcopy(expected))
    except Exception as error:
        receipt['responseError'] = str(error)
    # Read after success, head rejection, timeout or any ambiguous response.
    # A caller must retain this result and reconcile before a new invocation.
    try:
        candidate = read_candidate(deepcopy(expected))
        receipt['readback'] = candidate
        if (candidate.get('repository') == expected['repository']
                and candidate.get('pr') == expected['pr']
                and candidate.get('head') == expected['head']
                and candidate.get('baseRef') == expected['baseRef']
                and candidate.get('state') == 'merged'
                and re.fullmatch('[0-9a-f]{40}', candidate.get('mergeCommit') or '')):
            receipt['status'] = 'merged-readback'
    except Exception as error:
        receipt['readbackError'] = str(error)
    return receipt


def command(argv, **kwargs):
    return subprocess.run(argv, text=True, capture_output=True, timeout=120, **kwargs)


def github_read(expected):
    def get(path):
        result = command(['gh', 'api', '--hostname', 'github.com', path])
        require(result.returncode == 0, 'GitHub read unavailable')
        return json.loads(result.stdout)
    repo, number = expected['repository'], expected['pr']
    pr = get(f'repos/{repo}/pulls/{number}')
    compare = get(f'repos/{repo}/compare/{expected["base"]}...{pr["head"]["sha"]}')
    # Target tip is the final provider read before dispatch.
    ref = get(f'repos/{repo}/git/ref/heads/{quote(expected["baseRef"], safe="")}')
    return dict(repository=pr['base']['repo']['full_name'], pr=pr['number'],
                baseRef=pr['base']['ref'], base=ref['object']['sha'],
                head=pr['head']['sha'], mergeBase=compare['merge_base_commit']['sha'],
                state='merged' if pr.get('merged') else pr['state'], draft=pr['draft'],
                mergeCommit=pr.get('merge_commit_sha'))


def github_merge(expected):
    # No free-form merge flags, shell, admin bypass, retry or automatic closure.
    result = command(['gh', 'pr', 'merge', str(expected['pr']), '--repo',
                      'https://github.com/' + expected['repository'],
                      '--' + expected['strategy'], '--match-head-commit', expected['head']])
    return dict(exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binding', required=True, help='reviewed comparison and repository-owned required gate list as JSON')
    parser.add_argument('--execute', action='store_true', help='explicit authorized merge action; default only checks')
    parser.add_argument('preflight', nargs=argparse.REMAINDER, help='-- followed by trusted read-only preflight argv; JSON binding sent to stdin')
    args = parser.parse_args()
    argv = args.preflight[1:] if args.preflight[:1] == ['--'] else args.preflight
    try:
        require(bool(argv), 'missing preflight command')
        with open(args.binding, encoding='utf-8') as stream:
            expected = json.load(stream)
        def preflight(value):
            result = command(argv, input=json.dumps(value))
            return result.returncode, result.stdout
        receipt = run_guard(expected, preflight, github_read, github_merge, execute=args.execute)
    except (ValueError, OSError) as error:
        receipt = dict(status='blocked', mergeCalls=0, reason=str(error))
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt['status'] in ('checked', 'merged-readback') else 1


if __name__ == '__main__':
    sys.exit(main())
