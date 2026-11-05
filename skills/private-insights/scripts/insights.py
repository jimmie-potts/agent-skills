#!/usr/bin/env python3
"""Write one private, advisory delivery report from read-only GitHub evidence.

Every GitHub request goes through GhClient.get, which can only issue GET to a
repos/ path. The script reads no session store, home directory or memory
database; it opens only the private output directory and paths named on its
command line. All input text is data and reaches the report only through quote().
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import statistics
import subprocess
import sys
from urllib.parse import urlencode
from zoneinfo import ZoneInfo

SELECTED_REPOSITORIES = (
    'jimmie-potts/agent-device-hub',
    'jimmie-potts/codex-nanoleaf',
    'jimmie-potts/divoom-app-upgrade',
    'jimmie-potts/agent-skills',
    'jimmie-potts/dotfiles',
)
EXIT_USAGE, EXIT_SETUP_GAP, EXIT_CHECK = 2, 3, 4
PER_PAGE = 100
MAX_PAGES = 100
RUN_SEARCH_CAP = 1000  # GitHub returns at most this many runs for a created= search.
MAX_ACTIONS = 5
MAX_SNAPSHOT_BYTES = 5_000_000
FAILED = {'failure', 'timed_out', 'startup_failure'}
NOT_RUN = {'skipped', 'neutral', 'stale', 'action_required'}
TOKEN = re.compile(r'[A-Za-z0-9][A-Za-z0-9._:\[\]-]{0,63}')
SHA = re.compile(r'[0-9a-f]{40}')
SECRET_PATTERNS = (
    re.compile(r'\b(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{16,}'),
    re.compile(r'\bsk-[A-Za-z0-9_-]{16,}'),
    re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
    re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
    re.compile(r'(?i)\b(?:password|passwd|api[_-]?key|secret|token)\s*[=:]\s*\S+'),
)
PRIVATE_PATH = re.compile(r'(?:/Users/|/home/|[A-Za-z]:\\Users\\)[^\s`|]+')


class GitHubError(Exception):
    """A failed read. Its text holds only a status, never response content."""


class GitHubUnavailable(Exception):
    """The gh command itself cannot run: a setup gap, not a coverage gap."""


class Incomplete(Exception):
    """A collection could not be proven complete."""


class TooManyRuns(Exception):
    pass


class SetupGap(Exception):
    pass


class GhClient:
    """The only route to GitHub. GET to repos/ paths, no fields, no input body."""

    PATH = re.compile(r'repos/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_./-]+)?')

    def __init__(self, runner=subprocess.run, timeout=60):
        self.runner = runner
        self.timeout = timeout

    def argv(self, route, query):
        if not self.PATH.fullmatch(route) or '..' in route:
            raise ValueError('refusing a GitHub path outside repos/')
        target = route + ('?' + urlencode(sorted(query.items())) if query else '')
        return ['gh', 'api', '--method', 'GET', target]

    def get(self, route, **query):
        env = dict(os.environ, GH_PROMPT_DISABLED='1', GH_NO_UPDATE_NOTIFIER='1')
        try:
            done = self.runner(self.argv(route, query), capture_output=True, text=True,
                               timeout=self.timeout, env=env)
        except FileNotFoundError as exc:
            raise GitHubUnavailable('the gh command is not available') from exc
        except subprocess.TimeoutExpired as exc:
            raise GitHubError('request timed out') from exc
        if done.returncode != 0:
            status = re.search(r'HTTP (\d{3})', done.stderr or '')
            raise GitHubError(f'HTTP {status[1]}' if status else 'request failed')
        try:
            return json.loads(done.stdout)
        except ValueError as exc:
            raise GitHubError('unreadable response') from exc


# Time and window ---------------------------------------------------------

def parse_time(value):
    if not isinstance(value, str) or not value:
        return None
    try:
        moment = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None
    return moment.astimezone(timezone.utc) if moment.tzinfo else None


def iso(moment):
    return moment.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def in_window(value, window):
    moment = parse_time(value)
    return moment is not None and window['start'] <= moment < window['end']


def resolve_window(start, end, zone, now):
    """Default to the preceding seven days. Named bounds must carry an offset."""
    try:
        display = ZoneInfo(zone)
    except Exception as exc:
        raise ValueError(f'unknown display timezone: {zone}') from exc
    finish = parse_time(end) if end else now.replace(microsecond=0)
    if end and finish is None:
        raise ValueError('--end needs an ISO 8601 time with an offset')
    begin = parse_time(start) if start else finish - timedelta(days=7)
    if start and begin is None:
        raise ValueError('--start needs an ISO 8601 time with an offset')
    if begin >= finish:
        raise ValueError('the window start must precede its end')
    if finish > now:
        raise ValueError('the window end is in the future')
    return dict(start=begin, end=finish, zone=zone, display=display)


# Private destination -----------------------------------------------------

def require_private_dir(raw):
    """Refuse anything but an existing owner-only directory outside any checkout."""
    if not raw:
        raise SetupGap('no private output directory is configured. Create one outside any '
                       'Git checkout with mode 700 and pass it as --output-dir. '
                       'GitHub is never a fallback destination.')
    path = Path(raw)
    if not path.is_absolute():
        raise SetupGap('--output-dir must be an absolute path')
    try:
        info = os.lstat(path)
    except OSError as exc:
        raise SetupGap('the private output directory does not exist; create it with mode 700') from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise SetupGap('--output-dir must be a real directory, not a symlink or file')
    if info.st_uid != os.geteuid() or info.st_mode & 0o777 != 0o700:
        raise SetupGap('the private output directory must be owned by this user with mode 700')
    real = Path(os.path.realpath(path))  # A symlinked ancestor can lead into a checkout.
    for ancestor in (real, *real.parents):
        if os.path.lexists(ancestor / '.git'):
            raise SetupGap('the private output directory is inside a Git checkout')
    return path


def read_markers(raw):
    if not raw:
        return ()
    try:
        lines = Path(raw).read_text(encoding='utf-8').splitlines()
    except (OSError, UnicodeError) as exc:
        raise SetupGap('the secret-marker file cannot be read') from exc
    return tuple(line.strip() for line in lines if line.strip())


# Quoting -----------------------------------------------------------------

INERT = re.compile(r'[`|<>\x00-\x1f\x7f]')


def marker_forms(markers):
    """Each marker as supplied and as quote() would render it, longest first."""
    forms = set()
    for marker in markers:
        collapsed = re.sub(r'\s+', ' ', marker).strip()
        forms.update(form for form in (marker, collapsed, INERT.sub("'", collapsed)) if form)
    return sorted(forms, key=len, reverse=True)


def scrub(text, markers=()):
    for marker in marker_forms(markers):
        text = text.replace(marker, '[redacted]')
    for pattern in SECRET_PATTERNS:
        text = pattern.sub('[redacted]', text)
    return PRIVATE_PATH.sub('[private path]', text)


def quote(value, markers=(), limit=80):
    """Render input as one inert code span. Its text is never a direction."""
    text = scrub(re.sub(r'\s+', ' ', str(value)), markers)
    text = scrub(INERT.sub("'", text), markers).strip()
    if len(text) > limit:
        text = text[:limit - 1] + '…'
    return f'`{text}`' if text else '`(empty)`'


# Collection --------------------------------------------------------------

def _read_counted(client, path, key, cap, query):
    seen, total, page = {}, None, 1
    while True:
        try:
            data = client.get(path, per_page=PER_PAGE, page=page, **query)
        except GitHubError as exc:
            raise Incomplete(f'page {page} failed ({exc})') from exc
        if not isinstance(data, dict) or not isinstance(data.get(key), list) \
                or type(data.get('total_count')) is not int:
            raise Incomplete(f'page {page} was malformed')
        if total is None:
            total = data['total_count']
            if cap is not None and total > cap:
                raise TooManyRuns()
        elif data['total_count'] != total:
            raise Incomplete(f"total changed from {total} to {data['total_count']} during pagination")
        for item in data[key]:
            if not isinstance(item, dict) or 'id' not in item:
                raise Incomplete(f'page {page} held a record without an id')
            seen.setdefault(item['id'], item)
        if len(seen) >= total or not data[key]:
            break
        page += 1
        if page > MAX_PAGES:
            raise Incomplete('page limit reached')
    if len(seen) != total:
        raise Incomplete(f'collected {len(seen)} distinct of {total} reported')
    return list(seen.values())


def list_counted(client, path, key, cap=None, **query):
    """Read every page, dedupe by id, and prove the count. Retry the whole list once."""
    failure = None
    for _ in range(2):
        try:
            return _read_counted(client, path, key, cap, query)
        except Incomplete as exc:
            failure = exc
    raise failure


def list_runs(client, repo, start, end):
    """Bisect a window whose search would exceed GitHub's result cap."""
    path = f'repos/{repo}/actions/runs'
    try:
        return list_counted(client, path, 'workflow_runs', cap=RUN_SEARCH_CAP,
                            created=f'{iso(start)}..{iso(end)}')
    except TooManyRuns:
        if end - start <= timedelta(minutes=1):
            raise Incomplete('more runs than one search can return in a minute') from None
    middle = start + (end - start) / 2
    merged = {}
    for run in list_runs(client, repo, start, middle) + list_runs(client, repo, middle, end):
        merged[run['id']] = run
    return list(merged.values())


def read_pulls_once(client, repo, start):
    rows, page = {}, 1
    while True:
        try:
            data = client.get(f'repos/{repo}/pulls', state='all', sort='updated',
                              direction='desc', per_page=PER_PAGE, page=page)
        except GitHubError as exc:
            raise Incomplete(f'PR page {page} failed ({exc})') from exc
        if not isinstance(data, list) or not all(isinstance(pull, dict) for pull in data):
            raise Incomplete(f'PR page {page} was malformed')
        older = False
        for pull in data:
            updated = parse_time(pull.get('updated_at'))
            if updated is None or type(pull.get('number')) is not int:
                raise Incomplete(f'PR page {page} held a malformed record')
            if updated < start:
                older = True
            else:
                rows.setdefault(pull['number'], pull)
        if older or len(data) < PER_PAGE:
            return rows
        page += 1
        if page > MAX_PAGES:
            raise Incomplete('PR page limit reached')


def list_pulls(client, repo, start):
    """Read PRs by update time until two whole passes agree on numbers and update times.

    The list has no total, and a PR updated between pages moves ahead of the cursor,
    so one pass cannot prove it saw every PR.
    """
    previous, failure = None, None
    for _ in range(3):
        try:
            current = read_pulls_once(client, repo, start)
        except Incomplete as exc:
            previous, failure = None, exc
            continue
        stamps = {number: pull['updated_at'] for number, pull in current.items()}
        if previous == stamps:
            return list(current.values())
        previous, failure = stamps, Incomplete('the PR list changed between reads')
    raise failure


def read_policy(client, repo, window):
    """Record the workflow files in force at read time and changes in the window."""
    try:
        listing = client.get(f'repos/{repo}/contents/.github/workflows')
    except GitHubError as exc:
        if str(exc) != 'HTTP 404':
            raise Incomplete(f'workflow listing failed ({exc})') from exc
        listing = []
    if not isinstance(listing, list):
        raise Incomplete('workflow listing was malformed')
    pairs = sorted((str(item.get('name')), str(item.get('sha'))) for item in listing)
    fingerprint = hashlib.sha256(json.dumps(pairs).encode()).hexdigest()[:12]
    changes, page = {}, 1
    while True:
        try:
            data = client.get(f'repos/{repo}/commits', path='.github/workflows',
                              since=iso(window['start']), until=iso(window['end']),
                              per_page=PER_PAGE, page=page)
        except GitHubError as exc:
            if str(exc) == 'HTTP 409':  # An empty repository has no commits to list.
                break
            raise Incomplete(f'workflow history page {page} failed ({exc})') from exc
        if not isinstance(data, list):
            raise Incomplete('workflow history was malformed')
        for commit in data:
            if SHA.fullmatch(str(commit.get('sha'))):
                changes[commit['sha']] = True
        if len(data) < PER_PAGE:
            break
        page += 1
    return dict(fingerprint=fingerprint, files=len(pairs), changes=sorted(changes))


def is_qualification(run):
    return 'qualification' in f"{run.get('path', '')} {run.get('name', '')}".lower()


def wants_jobs(run):
    """Jobs explain reruns, failures and qualification; other runs stay at run level."""
    return run.get('status') == 'completed' and (
        run.get('run_attempt', 1) > 1 or run.get('conclusion') in FAILED or is_qualification(run))


def collect_repository(client, repo, window):
    item = dict(repository=repo, state='unavailable', gaps={}, runs=[], pulls=[], attempts={},
                jobs={}, checks={}, policy=None, jobs_selected=0, heads_selected=0)
    try:
        meta = client.get(f'repos/{repo}')
        if not isinstance(meta, dict):
            raise GitHubError('unreadable response')
    except GitHubError as exc:
        for source in ('repository', 'runs', 'pulls'):
            item['gaps'][source] = f'repository read failed ({exc})'
        return item
    item['state'] = 'archived' if meta.get('archived') else 'active'
    item['default_branch'] = meta.get('default_branch')
    try:
        item['policy'] = read_policy(client, repo, window)
    except Incomplete as exc:
        item['gaps']['policy'] = str(exc)
    try:
        runs = list_runs(client, repo, window['start'], window['end'])
        item['runs'] = [run for run in runs if in_window(run.get('created_at'), window)]
    except Incomplete as exc:
        item['gaps']['runs'] = str(exc)
    try:
        item['pulls'] = list_pulls(client, repo, window['start'])
    except Incomplete as exc:
        item['gaps']['pulls'] = str(exc)
    unread, unread_jobs = 0, 0
    for run in item['runs']:
        latest = run.get('run_attempt', 1)
        attempts = {latest: run}
        for number in range(1, latest):
            try:
                attempt = client.get(f"repos/{repo}/actions/runs/{run['id']}/attempts/{number}")
                if not isinstance(attempt, dict) or attempt.get('run_attempt') != number:
                    raise GitHubError('mismatched attempt')
                attempts[number] = attempt
            except GitHubError:
                attempts[number] = None
                unread += 1
        item['attempts'][run['id']] = attempts
        if wants_jobs(run):
            item['jobs_selected'] += 1
            item['jobs'][run['id']] = {}
            for number, attempt in attempts.items():
                if attempt is None:
                    continue
                try:
                    item['jobs'][run['id']][number] = list_counted(
                        client, f"repos/{repo}/actions/runs/{run['id']}/attempts/{number}/jobs", 'jobs')
                except Incomplete:
                    unread_jobs += 1
    earlier = sum(run.get('run_attempt', 1) - 1 for run in item['runs'])
    selected = sum(1 for run in item['runs'] if wants_jobs(run) for attempt in item['attempts'][run['id']].values()
                   if attempt is not None)
    if unread:
        item['gaps']['attempts'] = f'{unread} of {earlier} earlier attempt records could not be read'
    if unread_jobs:
        item['gaps']['jobs'] = f'job records for {unread_jobs} of {selected} selected attempts could not be read'
    missing_checks = 0
    for pull in item['pulls']:
        head = (pull.get('head') or {}).get('sha')
        if not in_window(pull.get('merged_at'), window) or not head:
            continue
        item['heads_selected'] += 1
        try:
            item['checks'][pull['number']] = list_counted(
                client, f'repos/{repo}/commits/{head}/check-runs', 'check_runs', filter='all')
        except Incomplete:
            missing_checks += 1
    if missing_checks:
        item['gaps']['checks'] = (f"check records for {missing_checks} of {item['heads_selected']} merged heads "
                                  'could not be read')
    return item


# Execution records -------------------------------------------------------

SOURCED = re.compile(r'([^\s|(),+;]+) \((host-observed|user-stated|self-reported|unknown)\)')
AGENT = re.compile(r'[\w-]+: requested (\S+) at (\S+), model (.+?), level (.+)')
REQUESTED = re.compile(r'requested ([^\s,]+),\s*(?:model|level) (.+)')
COUNT = re.compile(r'\d+')


def strip_fences(body):
    lines, fenced = [], False
    for line in body.splitlines():
        if line.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
        elif not fenced:
            lines.append(line)
    return lines


def parse_sourced(cell):
    """Split `value (provenance)` items. Host-read is observed; accounts are declared."""
    result = dict(declared=[], observed=[], unknown=False)
    for part in cell.split(' + '):
        match = SOURCED.fullmatch(part.strip())
        if not match:
            return None
        if match[2] == 'unknown' or match[1] == 'unknown':
            result['unknown'] = True
        elif match[2] == 'host-observed':
            result['observed'].append(match[1])
        else:
            result['declared'].append(match[1])
    return result


def parse_setting(cell):
    setting = dict(requested=[], declared=[], observed=[], unknown=True)
    if cell is None:
        return setting
    text = cell.strip()
    match = REQUESTED.fullmatch(text)
    if match:
        if match[1] not in ('unknown', 'default'):
            setting['requested'].append(match[1])
        text = match[2]
    sourced = parse_sourced(text)
    if sourced:
        setting.update(sourced)
        setting['unknown'] = sourced['unknown'] or not (sourced['declared'] or sourced['observed'])
    return setting


def parse_agents(cell):
    """Return each listed context's settings, or None when the cell has free text."""
    if cell is None:
        return None
    if cell.strip().lower() == 'none':
        return []
    agents = []
    for entry in cell.split('; '):
        match = AGENT.fullmatch(entry.strip())
        sourced = parse_sourced(match[3]) if match else None
        if not sourced:
            return None
        agents.append(dict(requested=[match[1]] if match[1] not in ('unknown', 'default') else [],
                           declared=sourced['declared'], observed=sourced['observed'],
                           unknown=sourced['unknown']))
    return agents


def parse_execution_record(body):
    """Accept every shape in use and report unparsed fields as unknown, never zero."""
    lines = strip_fences(body or '')
    starts = [i for i, line in enumerate(lines) if line.strip() == '## Execution record']
    if not starts:
        return dict(shape='none')
    if len(starts) > 1:
        return dict(shape='ambiguous')
    section = []
    for line in lines[starts[0] + 1:]:
        if line.startswith('## '):
            break
        section.append(line)
    fields = {}
    for line in section:
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if line.lstrip().startswith('|') and len(cells) >= 2 and cells[0] not in ('Field', ''):
            if not set(cells[0]) <= set('-: '):
                fields[cells[0]] = '|'.join(cells[1:]).strip()
    if 'Coordinator model' not in fields:
        return dict(shape='unstructured')
    coordinator_model = parse_setting(fields.get('Coordinator model'))
    coordinator_level = parse_setting(fields.get('Coordinator level'))
    corrections = fields.get('Corrections', '')
    agents = [parse_agents(fields.get(name)) for name in ('Workers', 'Reviewers')]
    strict = all(parse_sourced(fields.get(name, '')) for name in ('Coordinator model', 'Coordinator level')) \
        and all(group is not None for group in agents) \
        and (COUNT.fullmatch(corrections) or corrections == 'unknown' or corrections.startswith('at least '))
    shape = 'free-text table'
    if strict:
        shape = 'current table' if 'Finding causes' in fields else 'table without finding causes'
    return dict(shape=shape, recommended=fields.get('Recommended'),
                model=coordinator_model, level=coordinator_level,
                agents=[agent for group in agents if group for agent in group],
                agents_parsed=all(group is not None for group in agents),
                corrections=int(corrections) if COUNT.fullmatch(corrections) else None)


def family(token):
    """Name a provider family from a written model. An alias stays as written."""
    lowered = token.lower()
    if re.match(r'(claude|opus|sonnet|haiku|fable)', lowered):
        return 'Claude'
    if re.match(r'(gpt|codex|sol\b|luna\b|astra\b)', lowered):
        return 'Codex'
    if lowered.startswith('grok'):
        return 'Grok'
    return None


# Snapshots ---------------------------------------------------------------

def load_snapshot(raw, index):
    """Read one explicitly named JSON file. Failure reduces coverage, nothing wider."""
    label = f'snapshot-{index}'
    path = Path(raw)
    try:
        info = os.lstat(path)
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_SNAPSHOT_BYTES:
            return dict(label=label, error='not a regular file within the size limit', records=[])
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, ValueError):
        return dict(label=label, error='could not be read as JSON', records=[])
    if not isinstance(data, dict) or data.get('schema') != 'private-insights-snapshot/1' \
            or not isinstance(data.get('records'), list):
        return dict(label=label, error='unknown snapshot schema', records=[])
    return dict(label=label, error=None, records=[r for r in data['records'] if isinstance(r, dict)],
                observed_from=parse_time(data.get('observed_from')), observed_to=parse_time(data.get('observed_to')))


def known_revisions(evidence):
    known = {}
    for item in evidence:
        for pull in item['pulls']:
            head = (pull.get('head') or {}).get('sha')
            if head:
                known.setdefault((item['repository'], pull['number']), set()).add(head)
        for run in item['runs']:
            numbers = [pr.get('number') for pr in run.get('pull_requests') or []]
            if len(numbers) == 1 and run.get('head_sha'):
                known.setdefault((item['repository'], numbers[0]), set()).add(run['head_sha'])
    return known


def attribute_snapshot(snapshot, known):
    """Attach a record only by exact repository, PR and full revision."""
    result = dict(label=snapshot['label'], error=snapshot['error'], total=len(snapshot['records']),
                  attributed=[], unattributed={}, observed_from=snapshot.get('observed_from'),
                  observed_to=snapshot.get('observed_to'))
    for position, record in enumerate(snapshot['records'], 1):
        repo, pull, head = record.get('repository'), record.get('pr'), record.get('head_sha')
        if not isinstance(head, str) or not SHA.fullmatch(head) or type(pull) is not int:
            reason = 'no exact PR and full revision'
        elif (repo, pull) not in known:
            reason = 'PR not observed in this window'
        elif head not in known[(repo, pull)]:
            reason = 'revision not observed on that PR'
        else:
            result['attributed'].append(record)
            continue
        result['unattributed'].setdefault(reason, []).append(position)
    return result


def known_int(value):
    return value if type(value) is int and value >= 0 else None


# Analysis ----------------------------------------------------------------

def new_bucket():
    return dict(original=0, original_failed=0, prior_unobserved=0, prior_unobserved_failed=0, rerun=0,
                rerun_failed=0, new_commit=0, new_commit_failed=0, same_tree=0, same_tree_failed=0,
                same_sha=0, same_sha_failed=0, ambiguous=0, ambiguous_failed=0, cancelled=0, skipped=0,
                unfinished=0, unread=0, total=0, runs=0, minutes=[])


def attempt_url(repo, run_id, number):
    return f'https://github.com/{repo}/actions/runs/{run_id}/attempts/{number}'


def classify_run(run, history, pulls, window, default_branch):
    """Name a new run against earlier runs for the same workflow and revision line."""
    numbers = [pr.get('number') for pr in run.get('pull_requests') or []]
    workflow = run.get('workflow_id') or run.get('path')
    event, branch = run.get('event'), run.get('head_branch')
    if len(numbers) > 1:
        return 'ambiguous', None
    if len(numbers) == 1:
        key = ('pr', workflow, numbers[0])
    elif event != 'pull_request' and branch == default_branch or not branch:
        key = ('revision', workflow, run.get('head_sha'))
    else:
        key = ('branch', workflow, branch)
    tree = (run.get('head_commit') or {}).get('tree_id')
    earlier = history.get(key)
    if earlier is None:
        if key[0] == 'revision':
            kind = 'original'
        elif key[0] == 'pr':
            pull = pulls.get(numbers[0])
            opened = parse_time(pull.get('created_at')) if pull else None
            kind = 'original' if opened and opened >= window['start'] else 'prior_unobserved'
        else:
            kind = 'prior_unobserved'
    elif run.get('head_sha') in earlier['shas']:
        kind = 'same_sha'
    elif not tree or None in earlier['trees']:
        kind = 'ambiguous'
    elif tree in earlier['trees']:
        kind = 'same_tree'
    else:
        kind = 'new_commit'
    if run.get('conclusion') not in NOT_RUN:  # A skipped run establishes no attempt.
        entry = history.setdefault(key, dict(shas=set(), trees=set(), failed_trees=set()))
        entry['shas'].add(run.get('head_sha'))
        entry['trees'].add(tree)
    return kind, key


def place_attempt(bucket, kind, attempt):
    bucket['total'] += 1
    if attempt is None:
        bucket['unread'] += 1
        return
    status, conclusion = attempt.get('status'), attempt.get('conclusion')
    if status != 'completed':
        bucket['unfinished'] += 1
    elif conclusion == 'cancelled':
        bucket['cancelled'] += 1
    elif conclusion in NOT_RUN:
        bucket['skipped'] += 1
    else:
        bucket[kind] += 1
        if conclusion in FAILED:
            bucket[kind + '_failed'] += 1
        started, finished = parse_time(attempt.get('run_started_at')), parse_time(attempt.get('updated_at'))
        if kind == 'original' and started and finished:
            bucket['minutes'].append((finished - started).total_seconds() / 60)


def analyze_jobs(item, run, attempts, result):
    """Separate executed jobs from those a rerun copied. A copy keeps its old times."""
    repo = item['repository']
    records = item['jobs'].get(run['id'])
    if records is None:
        return
    qualification = is_qualification(run)
    seen, executed = set(), set()
    for number in sorted(records):
        attempt = attempts.get(number) or {}
        began = parse_time(attempt.get('run_started_at'))
        copied, fresh = [], []
        for job in records[number]:
            if job['id'] in seen:  # Pagination can repeat a record across pages.
                result['jobs_duplicate'] += 1
                continue
            seen.add(job['id'])
            result['jobs_read'] += 1
            started = parse_time(job.get('started_at'))
            key = (job.get('name'), job.get('started_at'), job.get('completed_at'))
            if number > 1 and started and ((began and started < began) or key in executed):
                copied.append(job)
            elif job.get('conclusion') == 'skipped':
                result['jobs_skipped'] += 1
            else:
                fresh.append(job)
                if started:
                    executed.add(key)
        result['jobs_copied_qualification' if qualification else 'jobs_copied_other'] += len(copied)
        withheld = False
        if qualification and number > 1:
            result['qualification_reruns'] += 1
            images = [job for job in copied + fresh if 'image' in str(job.get('name')).lower()]
            if copied and not images:
                result['qualification_undetermined'].append(attempt_url(repo, run['id'], number))
                withheld = True
            elif any(job in copied for job in images):
                result['partial_no_image'].append(attempt_url(repo, run['id'], number))
                withheld = True
        if withheld:
            # Without its own image the attempt cannot qualify, so its job outcomes say nothing
            # about the product. They leave both the failures and their denominator.
            result['jobs_withheld'] += len(fresh)
            continue
        result['jobs_executed'] += len(fresh)
        for job in fresh:
            if job.get('conclusion') in FAILED:
                name = str(job.get('name'))
                result['failed_jobs'].setdefault(name, []).append(attempt_url(repo, run['id'], number))


def analyze_checks(item, result):
    seen_logical = set()
    for number, checks in item['checks'].items():
        result['heads_read'] += 1
        failed = False
        for check in checks:
            app = (check.get('app') or {}).get('slug') or 'unknown'
            logical = (number, app, check.get('name'), check.get('started_at'),
                       check.get('completed_at'), check.get('conclusion'))
            if logical in seen_logical:  # A rerun's copied job appears as a new check id.
                continue
            seen_logical.add(logical)
            result['checks_distinct'] += 1
            if app != 'github-actions':
                result['checks_other_app'] += 1
            failed = failed or check.get('conclusion') in FAILED
        if failed:
            result['heads_failed'].append(number)


def analyze_repository(item, window):
    repo = item['repository']
    pulls = {pull['number']: pull for pull in item['pulls']}
    result = dict(workflows={}, runs=len(item['runs']), attempts=0, after_window=0, multi_attempt=0,
                  failed_then_green=[], same_tree_recovered=[], partial_no_image=[], qualification_reruns=0,
                  qualification_undetermined=[], jobs_withheld=0,
                  jobs_read=0, jobs_duplicate=0, jobs_executed=0, jobs_skipped=0, jobs_copied_qualification=0,
                  jobs_copied_other=0, failed_jobs={}, heads_read=0, heads_failed=[], checks_distinct=0,
                  checks_other_app=0)
    history, default_branch = {}, item.get('default_branch', 'main')
    for run in sorted(item['runs'], key=lambda r: (r.get('created_at') or '', r['id'])):
        kind, key = classify_run(run, history, pulls, window, default_branch)
        bucket = result['workflows'].setdefault(str(run.get('name') or run.get('path') or 'unnamed'), new_bucket())
        bucket['runs'] += 1
        attempts = item['attempts'].get(run['id'], {1: run})
        failed_before = False
        for number in sorted(attempts):
            attempt = attempts[number]
            started = parse_time((attempt or {}).get('run_started_at'))
            if attempt is not None and started and started >= window['end']:
                result['after_window'] += 1
                continue
            place_attempt(bucket, kind if number == 1 else 'rerun', attempt)
            result['attempts'] += 1
            conclusion = (attempt or {}).get('conclusion')
            if conclusion == 'success' and failed_before:
                result['failed_then_green'].append(attempt_url(repo, run['id'], number))
                failed_before = False
            failed_before = failed_before or conclusion in FAILED
        result['multi_attempt'] += 1 if len(attempts) > 1 else 0
        tree = (run.get('head_commit') or {}).get('tree_id')
        entry = history.get(key) if key else None
        if entry is not None:
            if kind == 'same_tree' and run.get('conclusion') == 'success' and tree in entry['failed_trees']:
                result['same_tree_recovered'].append(attempt_url(repo, run['id'], 1))
            if run.get('conclusion') in FAILED:
                entry['failed_trees'].add(tree)
        analyze_jobs(item, run, attempts, result)
    analyze_checks(item, result)
    merged = [p for p in item['pulls'] if in_window(p.get('merged_at'), window)]
    closed = [p for p in item['pulls'] if not p.get('merged_at') and in_window(p.get('closed_at'), window)]
    opened = [p for p in item['pulls'] if p.get('state') == 'open' and in_window(p.get('created_at'), window)]
    open_times = []
    for pull in merged:
        began, ended = parse_time(pull.get('created_at')), parse_time(pull.get('merged_at'))
        if began and ended:
            open_times.append((ended - began).total_seconds() / 3600)
    references = set()
    for pull in merged:
        body = '\n'.join(strip_fences(pull.get('body') or ''))
        references.update(re.findall(r'(?i)\b(?:refs|closes|fixes|resolves)\s+#(\d+)', body))
    result.update(merged=merged, closed=closed, opened=opened, open_hours=open_times, references=len(references),
                  records=[dict(parse_execution_record(p.get('body')), pr=p['number'], repository=repo) for p in merged])
    return result


def observed_anything(item):
    return bool(item['runs'] or item['pulls'])


# Report ------------------------------------------------------------------

def table(headers, rows):
    lines = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join('---' for _ in headers) + ' |']
    lines += ['| ' + ' | '.join(str(cell) for cell in row) + ' |' for row in rows]
    return lines


def coverage(item, *sources):
    gaps = [f'{source}: {item["gaps"][source]}' for source in sources if source in item['gaps']]
    if gaps:
        return 'incomplete: ' + '; '.join(gaps)
    return 'complete: ' + ', '.join(sources)


def short(repo):
    return repo.split('/', 1)[1]


def policy_changes(policy):
    if policy is None:
        return 'unknown'
    changes = policy['changes']
    listed = ', '.join(f'`{sha[:12]}`' for sha in changes[:3])
    return f'{len(changes)}: {listed}' if changes else 'none'


def median_text(values, unit, digits=1):
    return f'{statistics.median(values):.{digits}f} {unit}' if values else 'not applicable'


def attempts_rows(item, analysis, markers=()):
    if 'runs' in item['gaps']:
        unknown = ['unknown'] * 12
        return [[short(item['repository']), 'all', *unknown, 'unknown', coverage(item, 'runs')]]
    rows = []
    for name in sorted(analysis['workflows']):
        bucket = analysis['workflows'][name]
        gap = bucket['unread'] > 0
        def cell(key, with_failed=True):
            value = bucket[key]
            text = f'at least {value}' if gap else str(value)
            failed = bucket.get(key + '_failed', 0)
            return f'{text} ({failed} failed)' if with_failed and failed else text
        median = median_text(bucket['minutes'], 'min')
        cover = f"incomplete: {bucket['unread']} of {bucket['total']} attempts unread" if gap else 'complete: runs, attempts'
        rows.append([short(item['repository']), quote(name, markers), cell('original'), cell('prior_unobserved'),
                     cell('rerun'), cell('new_commit'), cell('same_tree'), cell('same_sha'), cell('ambiguous'),
                     cell('cancelled'), cell('skipped'), cell('unfinished'), str(bucket['unread']), median,
                     f"{bucket['total']} attempts in {bucket['runs']} runs", cover])
    return rows


def friction_rows(item, analysis):
    repo = short(item['repository'])
    run_cover, job_cover, check_cover = (coverage(item, 'runs', 'attempts'), coverage(item, 'runs', 'attempts', 'jobs'),
                                         coverage(item, 'pulls', 'checks'))
    rows = []
    def add(measure, value, denominator, cover, source_gap, show=True):
        if source_gap:
            value = 'unknown'
            denominator = 'unknown'
        if show or source_gap:
            rows.append([repo, measure, value, denominator, cover])
    runs_gap = 'runs' in item['gaps']
    def floor(value, *sources):
        return f'at least {value}' if any(s in item['gaps'] for s in sources) else value
    multi = analysis['multi_attempt']
    add('Runs failed then green on one revision (recurrence, not proof of a product flake)',
        floor(len(analysis['failed_then_green']), 'attempts'), f'{multi} multi-attempt runs', run_cover, runs_gap, multi > 0)
    same_tree = sum(b['same_tree'] for b in analysis['workflows'].values())
    add('Same-tree new-SHA retries that went green after a failure', floor(len(analysis['same_tree_recovered']), 'attempts'),
        f'{same_tree} same-tree new-SHA retries', run_cover, runs_gap, same_tree > 0)
    undetermined = len(analysis['qualification_undetermined'])
    partial_cover = job_cover if not undetermined else \
        f"incomplete: {undetermined} of {analysis['qualification_reruns']} qualification reruns copied jobs but have no recognisable image job"
    add('Partial qualification reruns without their own image (cannot qualify; not a new product failure)',
        'unknown' if undetermined else floor(len(analysis['partial_no_image']), 'jobs', 'attempts'),
        f"{analysis['qualification_reruns']} qualification reruns with job records", partial_cover, runs_gap,
        analysis['qualification_reruns'] > 0)
    copied = analysis['jobs_copied_qualification'] + analysis['jobs_copied_other']
    jobs = analysis['jobs_read']
    add('Jobs copied from an earlier attempt, excluded from executed jobs (qualification / other)',
        f"{floor(analysis['jobs_copied_qualification'], 'jobs', 'attempts')} / {floor(analysis['jobs_copied_other'], 'jobs', 'attempts')}",
        f'{jobs} job records from {item["jobs_selected"]} rerun, failed or qualification runs', job_cover, runs_gap, copied > 0)
    failed_jobs = sum(len(v) for v in analysis['failed_jobs'].values())
    withheld = analysis['jobs_withheld']
    add('Failed job executions, copies and partial reruns excluded', floor(failed_jobs, 'jobs', 'attempts'),
        f"{analysis['jobs_executed']} executed jobs in those runs"
        + (f"; {withheld} jobs from partial or undetermined qualification reruns are in neither count" if withheld else ''),
        job_cover, runs_gap, analysis['jobs_executed'] > 0 or withheld > 0)
    add('Merged PR heads with a failed check execution', floor(len(analysis['heads_failed']), 'checks'),
        f"{analysis['heads_read']} merged heads read of {item['heads_selected']}", check_cover,
        'pulls' in item['gaps'], item['heads_selected'] > 0)
    add('Check executions from apps other than GitHub Actions', floor(analysis['checks_other_app'], 'checks'),
        f"{analysis['checks_distinct']} distinct checks at merged heads", check_cover,
        'pulls' in item['gaps'], item['heads_selected'] > 0)
    return rows


def settings_citations(records):
    parsed = [r for r in records if 'model' in r]
    lines = []
    for label, pick in (('Coordinator model', lambda r: [r['model']]), ('Coordinator level', lambda r: [r['level']]),
                        ('Worker and reviewer model contexts', lambda r: r['agents'])):
        parts = []
        for kind in ('requested', 'declared', 'observed'):
            parts.append(f"{kind} {cite([r for r in parsed if any(e[kind] for e in pick(r))])}")
        unknown = [r for r in parsed if any(e['unknown'] and not e['observed'] and not e['declared'] for e in pick(r))]
        parts.append(f'unknown {cite(unknown)}')
        lines.append(f'- {label}: ' + '; '.join(parts) + '.')
    return lines


def settings_rows(records, merged_total, pull_gap):
    parsed = [r for r in records if 'model' in r]
    cover = f'{len(parsed)} of {merged_total} merged PRs have Execution-record settings'
    if pull_gap:
        return [['Coordinator model', *['unknown'] * 4, 'unknown', f'incomplete: {pull_gap}']]
    contexts = [agent for record in parsed for agent in record['agents']]
    rows = []
    for label, entries in (('Coordinator model', [r['model'] for r in parsed]),
                           ('Coordinator level', [r['level'] for r in parsed]),
                           ('Worker and reviewer model contexts', contexts)):
        if not entries:
            rows.append([label, 'unknown', 'unknown', 'unknown', 'unknown', '0 records', cover])
            continue
        rows.append([label, sum(1 for e in entries if e['requested']), sum(1 for e in entries if e['declared']),
                     sum(1 for e in entries if e['observed']),
                     sum(1 for e in entries if e['unknown'] and not e['observed'] and not e['declared']),
                     f'{len(entries)} records', cover])
    return rows


def provider_lines(records, markers):
    parsed = [r for r in records if 'model' in r]
    if not parsed:
        return ['- Attributable provider evidence: none. Provider and model stay unknown for every delivery in '
                'this report, so common findings, provider-specific gaps and cross-provider handoffs cannot be '
                'separated. Branch names are not treated as provider identity.']
    families = {}
    handoffs = []
    for record in parsed:
        seen = set()
        for token in evidenced(record['model']):
            name = family(token)
            if name:
                seen.add(name)
                entry = families.setdefault(name, dict(records=[], observed=0, values=set()))
                entry['values'].add(token)
        for name in seen:
            families[name]['records'].append(record)
            families[name]['observed'] += 1 if record['model']['observed'] else 0
        for agent in record['agents']:
            seen.update(filter(None, (family(token) for token in evidenced(agent))))
        if len(seen) > 1:
            handoffs.append(record)
    lines = []
    gaps = {name: e for name, e in families.items() if e['observed'] < len(e['records'])}
    if len(families) >= 2 and len(gaps) == len(families):
        lines.append('- Common to the named providers: coordinator models lack host-observed evidence on some records for each.')
    else:
        lines.append('- Common to both providers: not established; it needs attributable records from each with the same gap.')
    for name in sorted(families):
        entry = families[name]
        values = ', '.join(quote(v, markers) for v in sorted(entry['values'])[:6])
        lines.append(f"- {name} records: {entry['observed']} of {len(entry['records'])} have a host-observed coordinator "
                     f"model; written values, aliases unresolved: {values}. Records: {cite(entry['records'])}.")
    unattributed = [r for r in parsed if not any(family(t) for t in evidenced(r['model']))]
    lines.append(f'- Records with no declared or observed provider: {len(unattributed)} of {len(parsed)}. '
                 f'Records: {cite(unattributed)}.')
    lines.append(f'- Records whose declared or observed values name more than one provider, a possible cross-provider '
                 f'handoff: {len(handoffs)} of {len(parsed)}. Records: {cite(handoffs)}.')
    return lines


def evidenced(setting):
    """Provider attribution uses what was declared or observed, never what was requested."""
    return setting['declared'] + setting['observed']


def cite(records, limit=3):
    """Link the first few PRs behind a number, naming how many more there are."""
    if not records:
        return 'none'
    links = [f"[{short(r['repository'])}#{r['pr']}](https://github.com/{r['repository']}/pull/{r['pr']})"
             for r in records[:limit]]
    more = len(records) - limit
    return ', '.join(links) + (f' and {more} more' if more > 0 else '')


def snapshot_lines(snapshots, window, markers):
    if not snapshots:
        return ['No snapshot was supplied, so no local history was read.']
    lines = []
    for snap in snapshots:
        if snap['error']:
            lines.append(f"- {snap['label']}: not used, {snap['error']}. No other source replaced it.")
            continue
        differs = snap['observed_from'] != window['start'] or snap['observed_to'] != window['end']
        span = 'unknown' if not (snap['observed_from'] and snap['observed_to']) else \
            f"{iso(snap['observed_from'])} to {iso(snap['observed_to'])}"
        lines.append(f"- {snap['label']}: {len(snap['attributed'])} of {snap['total']} records attributed by exact PR and "
                     f"revision: {cite(snap['attributed'])}. Observation span {span}"
                     f"{' differs from the report window; do not read it as the same cohort' if differs else ''}.")
        for reason, positions in sorted(snap['unattributed'].items()):
            listed = ', '.join(str(n) for n in positions[:5]) + (f' and {len(positions) - 5} more' if len(positions) > 5 else '')
            lines.append(f'  - Unattributed, left out of every count: {len(positions)} of {snap["total"]} ({reason}); '
                         f'record positions {listed}.')
        lines.append(f"  - Provider and model as supplied are not verified by this report: {snapshot_settings(snap, markers)}.")
    return lines


def snapshot_settings(snap, markers):
    values = set()
    for record in snap['attributed']:
        model = record.get('model')
        for kind in ('requested', 'declared', 'observed'):
            value = model.get(kind) if isinstance(model, dict) else None
            if isinstance(value, str) and TOKEN.fullmatch(value):
                values.add(f'{kind} {quote(value, markers)}')
    return ', '.join(sorted(values)) or 'none'


def usage_rows(snapshots, merged_total):
    rows = []
    attributed = [r for snap in snapshots for r in snap['attributed']]
    label = 'attributed snapshot records' if snapshots else 'no snapshot supplied'
    coverage_note = f'no source: GitHub holds no such field for {merged_total} merged PRs' if not attributed else \
        f'{len(attributed)} attributed snapshot records; GitHub holds no such field'
    def measure(name, values):
        known = [v for v in values if v is not None]
        if not known:
            rows.append([name, 'unknown', f'0 of {len(values)} {label}', coverage_note])
        else:
            rows.append([name, sum(known), f'{len(known)} of {len(values)} {label}', coverage_note])
    tokens = []
    for record in attributed:
        usage = record.get('usage') if isinstance(record.get('usage'), dict) else {}
        parts = [known_int(usage.get(k)) for k in ('input_tokens', 'output_tokens')]
        tokens.append(None if None in parts else sum(parts))
    measure('Usage tokens, not a bill', tokens)
    measure('Documented interruptions', [known_int(r.get('interruptions')) for r in attributed])
    outcomes = [r.get('attempt_outcome') for r in attributed]
    measure('Interrupted attempts in snapshots', [None if o not in ('completed', 'failed', 'interrupted') else int(o == 'interrupted')
                                     for o in outcomes])
    measure('Failed attempts in snapshots', [None if o not in ('completed', 'failed', 'interrupted') else int(o == 'failed')
                                for o in outcomes])
    return rows


def summary_totals(item, analysis):
    if 'runs' in item['gaps'] or 'attempts' in item['gaps'] or 'pulls' in item['gaps']:
        return None
    buckets = analysis['workflows'].values()
    def add(key):
        return sum(b[key] for b in buckets)
    return dict(attempts=analysis['attempts'], comparable_originals=add('original'),
                comparable_originals_failed=add('original_failed'), reruns=add('rerun'), new_commit=add('new_commit'),
                same_tree=add('same_tree'), cancelled=add('cancelled'), skipped=add('skipped'),
                merged=len(analysis['merged']), closed_unmerged=len(analysis['closed']))


def load_previous(directory, window):
    """Read earlier summaries from the private output directory only."""
    candidates = []
    for path in sorted(directory.glob('insights-*.json')):
        try:
            if not stat.S_ISREG(os.lstat(path).st_mode):
                continue
            data = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, UnicodeError, ValueError):
            continue
        if not isinstance(data, dict) or data.get('schema') != 'private-insights-summary/1':
            continue
        finish = parse_time((data.get('window') or {}).get('end'))
        if finish and finish <= window['start']:
            candidates.append((finish, data))
    return max(candidates, key=lambda pair: pair[0])[1] if candidates else None


def compare_previous(previous, summary, window):
    if previous is None:
        return ['No earlier report exists in the output directory, so no change is stated.']
    begin, finish = (parse_time(previous['window'].get(k)) for k in ('start', 'end'))
    reasons = []
    if not begin or not finish or finish - begin != window['end'] - window['start']:
        reasons.append('the previous window has a different length')
    if previous.get('repositories') != summary['repositories']:
        reasons.append('the previous report selected different repositories')
    if not previous.get('complete') or not summary['complete']:
        reasons.append('one of the two reports has incomplete coverage')
    if previous.get('policy') != summary['policy']:
        reasons.append('the workflow policy differs between the windows')
    if any((p or {}).get('changes') for p in summary['policy'].values()):
        reasons.append('a workflow file changed during this window')
    if any((p or {}).get('changes') for p in (previous.get('policy') or {}).values()):
        reasons.append('a workflow file changed during the previous window')
    if reasons:
        return ['Not compared: ' + '; '.join(reasons) + '. Unlike windows are not presented as a change.']
    rows = []
    span = f"{previous['window']['start']} to {previous['window']['end']}"
    for repo in summary['repositories']:
        now, then = summary['totals'].get(repo), (previous.get('totals') or {}).get(repo)
        if not now or not then:
            continue
        for key, label, base in (('comparable_originals', 'Comparable originals', 'attempts'),
                                 ('comparable_originals_failed', 'Comparable originals failed', 'comparable_originals'),
                                 ('reruns', 'Reruns', 'attempts'), ('merged', 'PRs merged', None)):
            before, after = known_int(then.get(key)), known_int(now.get(key))
            if before is None or after is None or before == after:
                continue
            denominator = f'{then.get(base)} then {now.get(base)} {base}' if base else 'PRs merged in each window'
            rows.append([short(repo), label, before, after, denominator, 'complete: both windows'])
    if not rows:
        return [f'Compared with {span}: no compared count changed. This window differs in its issue mix; no cause is claimed.']
    return [f'Compared with {span}. Issue mix differs, so these are counts, not causes.', '',
            *table(['Repository', 'Measure', 'Previous', 'Current', 'Denominator', 'Coverage'], rows)]


def propose_actions(analyses, evidence):
    """Propose only what known evidence supports, linked to an existing owner."""
    actions = []
    green = sum(len(a['failed_then_green']) for a in analyses)
    multi = sum(a['multi_attempt'] for a in analyses)
    recovered = sum(len(a['same_tree_recovered']) for a in analyses)
    same_tree = sum(b['same_tree'] for a in analyses for b in a['workflows'].values())
    partial = sum(len(a['partial_no_image']) for a in analyses)
    reruns = sum(a['qualification_reruns'] for a in analyses)
    merged = sum(len(a['merged']) for a in analyses)
    settled = sum(1 for a in analyses for r in a['records'] if 'model' in r)
    incomplete = [item['repository'] for item in evidence if item['gaps']]
    if green or recovered:
        actions.append(f'Use the planned CI triage on the failed-then-green runs ({green} of {multi} multi-attempt runs) and '
                       f'same-tree recoveries ({recovered} of {same_tree} same-tree new-SHA retries) before calling any of '
                       'them a flake. Owner: [agent-skills#173](https://github.com/jimmie-potts/agent-skills/issues/173).')
    if partial:
        actions.append(f'Cover partial qualification reruns ({partial} of {reruns} qualification reruns with job records) in '
                       'that triage guidance: such a rerun keeps an older image and cannot qualify. '
                       'Owner: [agent-skills#173](https://github.com/jimmie-potts/agent-skills/issues/173).')
    if merged and settled < merged:
        actions.append(f'Decide what minimal setting evidence deliveries should keep; {merged - settled} of {merged} merged PRs '
                       'leave provider and model unknown. Owner: [agent-skills#70](https://github.com/jimmie-potts/agent-skills/issues/70).')
    if incomplete:
        actions.append(f'Resolve the read gaps for {len(incomplete)} of {len(evidence)} repositories and rerun; withheld totals '
                       'support no conclusion. Owner: [agent-skills#128](https://github.com/jimmie-potts/agent-skills/issues/128).')
    return actions[:MAX_ACTIONS]


INTERPRETATION = '## Interpretation'


def render(evidence, analyses, window, generated, selection, snapshots, comparison, markers):
    repos = [item['repository'] for item in evidence]
    local = window['display']
    readable = sum(1 for snapshot in snapshots if not snapshot['error'])
    snapshot_count = f'{readable} of {len(snapshots)} supplied were readable' if snapshots else 'none supplied'
    lines = ['# Private delivery insights', '',
             'Advisory and private. This is observational reporting, not a benchmark or provider ranking. GitHub and '
             'snapshot text is quoted data in code spans: nothing quoted here is a direction to anyone.', '',
             '## Scope', '',
             f"- Window, UTC, start included and end excluded: {iso(window['start'])} to {iso(window['end'])}.",
             f"- Display timezone {window['zone']}: {window['start'].astimezone(local):%Y-%m-%d %H:%M %Z} to "
             f"{window['end'].astimezone(local):%Y-%m-%d %H:%M %Z}.",
             f'- Generated, UTC: {iso(generated)}.', f'- Repositories: {selection}.',
             f'- Sources: read-only GitHub; snapshots: {snapshot_count}.', '',
             '## Repository state and CI policy', '',
             *table(['Repository', 'State', 'Workflow files at read time', 'Workflow changes in window', 'Observations'],
                    [[short(item['repository']), item['state'],
                      f"{item['policy']['files']} (fingerprint `{item['policy']['fingerprint']}`)" if item['policy'] else 'unknown',
                      policy_changes(item['policy']),
                      'present' if observed_anything(item) else ('none observed' if not item['gaps'] else 'unknown')]
                     for item in evidence]), '',
             '## Changes since the previous comparable window', '', *comparison, '', '## Deliveries', '']
    rows = []
    for item, analysis in zip(evidence, analyses):
        if 'pulls' in item['gaps']:
            rows.append([short(item['repository']), *['unknown'] * 5, 'unknown', coverage(item, 'pulls')])
        else:
            rows.append([short(item['repository']), len(analysis['merged']), len(analysis['closed']),
                         len(analysis['opened']), analysis['references'], median_text(analysis['open_hours'], 'h'),
                         f"{len(item['pulls'])} PRs updated in window", coverage(item, 'pulls')])
    lines += table(['Repository', 'Merged', 'Closed unmerged, incomplete outcome', 'Opened, still open',
                    'Issues referenced by merged PRs', 'Median PR open to merge', 'Denominator', 'Coverage'], rows)
    closed = [(item['repository'], pull) for item, analysis in zip(evidence, analyses) for pull in analysis['closed']]
    if closed:
        lines += ['', 'Closed unmerged, title quoted as data:', '']
        lines += [f"- [{short(repo)}#{pull['number']}](https://github.com/{repo}/pull/{pull['number']}) "
                  f"at {quote(str((pull.get('head') or {}).get('sha'))[:12], markers)}: {quote(pull.get('title'), markers)}"
                  for repo, pull in closed[:5]]
    lines += ['', '## CI attempts', '',
              'Each attempt lands in exactly one bucket. Comparable originals are finished first attempts on a new revision '
              'or newly opened PR. Prior unobserved means the first run seen on a PR or branch whose earlier history lies '
              'outside the window. Compare within one workflow only.', '']
    rows = [row for item, analysis in zip(evidence, analyses) for row in attempts_rows(item, analysis, markers)]
    if rows:
        lines += table(['Repository', 'Workflow', 'Comparable originals', 'Prior unobserved', 'Reruns', 'New-commit attempts',
                        'Same-tree new SHA', 'Same-SHA new run', 'Ambiguous revision', 'Cancelled', 'Skipped or not run',
                        'Unfinished', 'Unread history', 'Median original wall time', 'Denominator', 'Coverage'], rows)
    else:
        lines.append('No workflow runs were created in this window in any selected repository; every run list was complete.')
    changed = [short(item['repository']) for item in evidence if item['policy'] and item['policy']['changes']]
    if changed:
        lines += ['', 'Workflow files changed during this window in ' + ', '.join(changed)
                  + ', so attempts before and after a change are not comparable.']
    excluded = sum(a['after_window'] for a in analyses)
    if excluded:
        observed = excluded + sum(a['attempts'] for a in analyses)
        lines += ['', f'{excluded} of {observed} attempts read started after the window end and are excluded.']
    lines += ['', '## Evidence-backed friction', '']
    rows = [row for item, analysis in zip(evidence, analyses) for row in friction_rows(item, analysis)]
    lines += table(['Repository', 'Measure', 'Value', 'Denominator', 'Coverage'], rows) if rows else \
        ['No rerun, failed job or merged-head evidence was observed.']
    citations = []
    for item, analysis in zip(evidence, analyses):
        repo = short(item['repository'])
        total = sum(len(v) for v in analysis['failed_jobs'].values())
        ranked = sorted(analysis['failed_jobs'].items(), key=lambda pair: (-len(pair[1]), pair[0]))
        for name, urls in ranked[:3]:
            links = ', '.join(f'[attempt]({url})' for url in urls[:3])
            citations.append(f'- {repo}: {quote(name, markers)} failed {len(urls)} of {total} failed job executions: {links}.')
        for label, urls in (('Failed then green', analysis['failed_then_green']),
                            ('Same-tree recovery', analysis['same_tree_recovered']),
                            ('Partial qualification rerun', analysis['partial_no_image'])):
            if urls:
                links = ', '.join(f'[attempt]({url})' for url in urls[:3])
                citations.append(f'- {repo}: {label}: {links}.')
        if analysis['heads_failed']:
            links = ', '.join(f"[#{n}](https://github.com/{item['repository']}/pull/{n})" for n in analysis['heads_failed'][:3])
            citations.append(f'- {repo}: merged heads with a failed check execution: {links}.')
    if citations:
        lines += ['', 'Citations, job names quoted as data:', '', *citations]
    all_records = [r for a in analyses for r in a['records']]
    merged_total = sum(len(a['merged']) for a in analyses)
    pull_gap = next((item['gaps']['pulls'] for item in evidence if 'pulls' in item['gaps']), None)
    lines += ['', '## Model settings', '',
              'Requested is what a record says was asked for. Declared is what a user or agent stated. Observed is read from '
              'the host. They are kept apart; a request never establishes what ran. Unknown stays unknown.', '',
              *table(['Setting', 'Requested', 'Declared', 'Observed', 'Unknown', 'Denominator', 'Coverage'],
                     settings_rows(all_records, merged_total, pull_gap))]
    if not pull_gap and any('model' in r for r in all_records):
        lines += ['', 'Records behind each count:', '', *settings_citations(all_records)]
    shapes = {}
    for record in all_records:
        shapes[record['shape']] = shapes.get(record['shape'], 0) + 1
    known = [r for r in all_records if r.get('corrections') is not None]
    first = sum(1 for r in known if r['corrections'] == 0)
    if pull_gap:
        lines += ['', 'Execution-record shapes and correction measures are unknown: the PR list is incomplete.']
    else:
        rows = [[f'Execution record shape: {name}', count, f'{merged_total} merged PRs', 'complete: PR bodies']
                for name, count in sorted(shapes.items())]
        if known:
            rows += [['Accepted with no correction pass', first, f'{len(known)} records with a known correction count',
                      f'{len(known)} of {merged_total} merged PRs'],
                     ['Accepted after correction', len(known) - first, f'{len(known)} records with a known correction count',
                      f'{len(known)} of {merged_total} merged PRs']]
        elif merged_total:
            rows.append(['Accepted with no correction pass', 'unknown', '0 records with a known correction count',
                         f'0 of {merged_total} merged PRs'])
        if rows:
            lines += ['', *table(['Measure', 'Value', 'Denominator', 'Coverage'], rows), '', 'Records behind each count:', '']
            lines += [f"- Execution record shape {name}: {cite([r for r in all_records if r['shape'] == name])}."
                      for name in sorted(shapes)]
            if known:
                lines += [f"- Accepted with no correction pass: {cite([r for r in known if r['corrections'] == 0])}.",
                          f"- Accepted after correction: {cite([r for r in known if r['corrections'] > 0])}."]
    lines += ['', '## Providers', '', *provider_lines(all_records, markers),
              '', '## Usage and interruptions', '',
              *table(['Measure', 'Value', 'Denominator', 'Coverage'], usage_rows(snapshots, merged_total)),
              '', '## Snapshots', '', *snapshot_lines(snapshots, window, markers),
              '', '## Missing evidence and limits', '']
    gaps = [f"- {short(item['repository'])}: {coverage(item, *item['gaps'])}." for item in evidence if item['gaps']]
    lines += gaps or ['- Every selected GitHub collection read completely.']
    lines += ['- Unobserved population: work that never reached GitHub, abandoned local attempts, local check runs, deleted '
              'runs, and reruns started in this window of runs created before it.',
              '- Job records cover rerun, failed and qualification runs only; check records cover merged heads only.',
              '- No flake-rate, time-saving, monetary or provider-ranking claim is made: this evidence has no valid '
              'comparable basis for one. Wall times are elapsed time, not effort.', '',
              '## Proposed actions', '',
              'Advisory. Nothing here was applied, filed or scheduled.', '']
    actions = propose_actions(analyses, evidence)
    lines += [f'{index}. {action}' for index, action in enumerate(actions, 1)] or ['No action is supported by this evidence.']
    lines += ['', INTERPRETATION, '', 'None added. A reader may replace this line with interpretation that names no number; '
              'every figure belongs in the generated sections above.']
    return '\n'.join(lines) + '\n'


# Report checks -----------------------------------------------------------

MONEY = re.compile(r'[$€£]\s?\d|\b\d[\d,.]*\s?(?:USD|EUR|GBP|dollars)\b|\b(?:cost|price|bill)\b[^|\n]{0,20}?[:=]\s*\d', re.I)
SAVINGS = re.compile(r'\b(?:saved|saves|saving)\s+(?:about\s+|~)?\d|\b\d+(?:\.\d+)?\s*(?:h|hours?|min|minutes?)\s+saved\b', re.I)
FLAKE = re.compile(r'\bflak\w*[^|\n]{0,30}?\d+(?:\.\d+)?\s*%|\d+(?:\.\d+)?\s*%[^|\n]{0,30}?\bflak|\bflake[- ]rate\b\s*[:=]', re.I)
PROVIDER = r'(?:claude(?: code)?|codex|opus|sonnet|haiku|fable|gpt\S*|sol|luna|astra|grok)'
RANKING = re.compile(
    rf'\b{PROVIDER}\b[^|\n.]{{0,30}}\b(?:better|faster|superior|outperform\w*|beats?|wins?|more reliable)\b'
    rf'|\b(?:better|faster|superior|more reliable)\b[^|\n.]{{0,30}}\bthan\b[^|\n.]{{0,10}}\b{PROVIDER}\b'
    rf'|\b(?:because of|caused by|due to|thanks to)\s+{PROVIDER}\b|\bprovider ranking\s*:|\bwinner\b', re.I)
# Added interpretation may name no number and no comparison, cause, saving or price at all.
NUMBER_WORDS = re.compile(r'\d|\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|'
                          r'forty|fifty|hundred|thousand|dozen|half|twice|double|triple|percent|majority|minority)\b', re.I)
INTERPRETIVE_CLAIM = re.compile(r'\b(?:better|worse|best|worst|faster|slower|superior|inferior|outperform\w*|beats?|'
                                r'wins?|winner|reliab\w*|rank\w*|saved|saves?|saving|cheaper|costl?\w*|price\w*|'
                                r'caused?|causes|because|due to|thanks to|flak\w*|rate)\b|[$€£%|`]', re.I)
UNKNOWN_COVER = re.compile(r'^(?:incomplete|unknown|unavailable|no source|0 of )', re.I)
NUMERIC = re.compile(r'^(?:at least )?\d')


def split_interpretation(text):
    """Return the generated body and the interpretation section, which must come last."""
    parts = re.split(r'^## Interpretation[ \t]*$', text, flags=re.M)
    if len(parts) != 2 or re.search(r'^#{1,6} ', parts[1], flags=re.M):
        return None, None
    return parts[0], parts[1]


def body_digest(text):
    body, _ = split_interpretation(text)
    return hashlib.sha256((body or text).encode('utf-8')).hexdigest()


def check_report(text, markers=()):
    """Return every way a report breaks the trust rules. Empty means it may be kept."""
    problems = []
    if any(form in text for form in marker_forms(markers)):
        problems.append('a supplied secret marker appears in the report')
    body, interpretation = split_interpretation(text)
    if body is None:
        problems.append('the interpretation section is missing, repeated or not last')
    else:
        if NUMBER_WORDS.search(interpretation):
            problems.append('the interpretation names a number; figures belong in the generated sections')
        if INTERPRETIVE_CLAIM.search(interpretation):
            problems.append('the interpretation makes a comparison, cause, saving, price or rate claim')
    if any(pattern.search(text) for pattern in SECRET_PATTERNS):
        problems.append('a credential-shaped value appears in the report')
    if PRIVATE_PATH.search(text):
        problems.append('a private path appears in the report')
    prose = re.sub(r'`[^`\n]*`', '`quoted`', text)
    for pattern, label in ((MONEY, 'unsupported monetary total'), (SAVINGS, 'unsupported time-saving claim'),
                           (FLAKE, 'unsupported flake rate'), (RANKING, 'causal or provider-ranking claim')):
        if pattern.search(prose):
            problems.append(label)
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        if not (lines[index].startswith('|') and index + 1 < len(lines) and set(lines[index + 1]) <= set('|- :')):
            index += 1
            continue
        headers = [cell.strip() for cell in lines[index].strip().strip('|').split('|')]
        index += 2
        rows = []
        while index < len(lines) and lines[index].startswith('|'):
            rows.append([cell.strip() for cell in lines[index].strip().strip('|').split('|')])
            index += 1
        for row in rows:
            numeric = [cell for cell in row if NUMERIC.match(cell)]
            if headers[:2] == ['Repository', 'State'] or not numeric:
                continue
            if 'Denominator' not in headers or 'Coverage' not in headers or len(row) != len(headers):
                problems.append(f'a numeric row lacks a denominator or coverage: {row[0]}')
                continue
            denominator, cover = row[headers.index('Denominator')], row[headers.index('Coverage')]
            if not denominator or not cover:
                problems.append(f'a numeric row has an empty denominator or coverage: {row[0]}')
            values = [c for h, c in zip(headers, row) if h not in ('Denominator', 'Coverage', 'Repository', 'Measure', 'Setting')]
            if UNKNOWN_COVER.match(cover) and any(re.match(r'^0(?:\s|$)', cell) for cell in values):
                problems.append(f'unknown coverage shown as zero: {row[0]}')
    section = re.split(r'^## Proposed actions\s*$', body or text, flags=re.M)
    if len(section) != 2:
        problems.append('the proposed-actions section is missing')
    else:
        actions = re.findall(r'^\d+\. .*$', section[1], flags=re.M)
        if len(actions) > MAX_ACTIONS:
            problems.append(f'more than {MAX_ACTIONS} proposed actions')
        if any('Owner:' not in action for action in actions):
            problems.append('a proposed action has no linked owner')
    if '## Scope' not in text or 'Window, UTC' not in text or 'Display timezone' not in text:
        problems.append('the window or display timezone is missing')
    if '## Missing evidence and limits' not in text:
        problems.append('the limits section is missing')
    return problems


def check_file(path, markers=()):
    """Check a saved report, and that only its interpretation changed since it was generated."""
    text = path.read_text(encoding='utf-8')
    problems = check_report(text, markers)
    try:
        summary = json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
        recorded = summary.get('report_digest') if isinstance(summary, dict) else None
    except (OSError, UnicodeError, ValueError):
        recorded = None
    if recorded is None:
        problems.append('the counts-only summary beside the report is missing or unreadable')
    elif recorded != body_digest(text):
        problems.append('the generated sections changed after generation; only the interpretation may be edited')
    return problems


# Command line ------------------------------------------------------------

def select_repositories(names):
    chosen = list(dict.fromkeys(names or SELECTED_REPOSITORIES))
    outside = [name for name in chosen if name not in SELECTED_REPOSITORIES]
    if outside:
        raise ValueError('a repository is outside the selected allowlist')
    if len(chosen) == len(SELECTED_REPOSITORIES):
        return chosen, f'the full selected allowlist of {len(chosen)}: ' + ', '.join(short(n) for n in chosen)
    omitted = [short(n) for n in SELECTED_REPOSITORIES if n not in chosen]
    return chosen, (f'a named subset, {len(chosen)} of {len(SELECTED_REPOSITORIES)}: '
                    + ', '.join(short(n) for n in chosen) + '; omitted: ' + ', '.join(omitted))


def write_private(path, text):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w', encoding='utf-8') as handle:
        handle.write(text)


def generate(args, client, now):
    directory = require_private_dir(args.output_dir)
    markers = read_markers(args.secret_markers_file)
    repositories, selection = select_repositories(args.repo)
    window = resolve_window(args.start, args.end, args.timezone, now)
    loaded = [load_snapshot(raw, index) for index, raw in enumerate(args.snapshot or [], 1)]
    evidence = [collect_repository(client, repo, window) for repo in repositories]
    analyses = [analyze_repository(item, window) for item in evidence]
    known = known_revisions(evidence)
    snapshots = [attribute_snapshot(snapshot, known) for snapshot in loaded]
    summary = dict(schema='private-insights-summary/1', generated_at=iso(now),
                   window=dict(start=iso(window['start']), end=iso(window['end']), timezone=window['zone']),
                   repositories=repositories, complete=not any(item['gaps'] for item in evidence),
                   policy={item['repository']: item['policy'] for item in evidence},
                   totals={item['repository']: summary_totals(item, analysis)
                           for item, analysis in zip(evidence, analyses)},
                   gaps={item['repository']: item['gaps'] for item in evidence})
    comparison = compare_previous(load_previous(directory, window), summary, window)
    text = render(evidence, analyses, window, now, selection, snapshots, comparison, markers)
    problems = check_report(text, markers)
    if problems:
        print('report-check-failed: ' + '; '.join(sorted(set(problems))), file=sys.stderr)
        return EXIT_CHECK, None
    stem = f"insights-{window['start']:%Y%m%dT%H%M%SZ}-{window['end']:%Y%m%dT%H%M%SZ}-{now:%Y%m%dT%H%M%SZ}"
    report = directory / f'{stem}.md'
    summary['report_digest'] = body_digest(text)
    write_private(report, text)
    write_private(directory / f'{stem}.json', json.dumps(summary, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(status='written', report=str(report), complete=summary['complete'],
                          repositories=[short(r) for r in repositories],
                          window=summary['window'], gaps=summary['gaps']), indent=2))
    return 0, report


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest='command', required=True)
    make = commands.add_parser('generate', help='write one private report')
    make.add_argument('--output-dir', help='existing owner-only directory outside any Git checkout')
    make.add_argument('--repo', action='append', help='owner/name inside the selected allowlist; repeatable')
    make.add_argument('--start', help='ISO 8601 with offset; defaults to seven days before the end')
    make.add_argument('--end', help='ISO 8601 with offset; defaults to now')
    make.add_argument('--timezone', default='UTC', help='IANA display timezone')
    make.add_argument('--snapshot', action='append', help='explicit private-insights-snapshot/1 JSON file; repeatable')
    make.add_argument('--secret-markers-file', help='file of literal strings that must not be published')
    verify = commands.add_parser('check', help='check a report file against the trust rules')
    verify.add_argument('report')
    verify.add_argument('--secret-markers-file')
    return parser


def main(argv=None, client=None, now=None):
    args = build_parser().parse_args(argv)
    try:
        if args.command == 'check':
            problems = check_file(Path(args.report), read_markers(args.secret_markers_file))
            for problem in sorted(set(problems)):
                print(problem, file=sys.stderr)
            return EXIT_CHECK if problems else 0
        return generate(args, client or GhClient(), now or datetime.now(timezone.utc))[0]
    except (SetupGap, GitHubUnavailable) as exc:
        print(f'setup-gap: {exc}', file=sys.stderr)
        return EXIT_SETUP_GAP
    except (ValueError, OSError) as exc:
        print(f'stopped: {exc}', file=sys.stderr)
        return EXIT_USAGE


if __name__ == '__main__':
    raise SystemExit(main())
