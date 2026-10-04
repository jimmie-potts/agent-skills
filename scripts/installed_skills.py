#!/usr/bin/env python3
"""Update existing managed skills; no discovery, link creation or service claims."""
import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
REPOSITORY = 'jimmie-potts/agent-skills'
REMOTE_URLS = {'https://github.com/jimmie-potts/agent-skills.git', 'git@github.com:jimmie-potts/agent-skills.git'}
TOOLS = ['bash', 'python3', 'git', 'dirname', 'readlink', 'realpath', 'find', 'sort', 'basename',
         'sha256sum', 'stat', 'cut', 'mkdir', 'ln', 'unlink']
FIELDS = {'schemaVersion', 'repository', 'owner', 'checkout', 'stateDirectory', 'evidenceRoot',
          'git', 'path', 'allowedPaths', 'protectedPaths', 'requiredSkills', 'links', 'files'}
REQUEST = {'schemaVersion', 'operation', 'repository', 'issue', 'merge', 'owner', 'deadline', 'evidenceDirectory'}
ACTIVE = ['skills/'+name for name in ['deliver-work', 'review-work', 'code-review', 'plan-work',
                                     'tdd', 'writing-for-agents', 'unslop']]
LIMIT = 8 * 1024 * 1024


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(value):
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate-json-key')
        result[key] = value
    return result


def owned(path, *, directory=False, private=False, system=False):
    path = Path(path)
    require(path.is_absolute() and path.resolve() == path, 'noncanonical-path')
    info = path.lstat()
    require(info.st_uid in ({0, os.getuid()} if system else {os.getuid()}) and
            not info.st_mode & (0o077 if private else 0o022) and
            (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode) and
             (info.st_nlink == 1 or system and info.st_uid == 0)), 'unsafe-path')
    return path


def read(path):
    path = Path(path)
    if not path.exists():
        return None
    owned(path, private=True)
    require(path.stat().st_size <= LIMIT, 'private-record-too-large')
    return json.loads(path.read_text(), object_pairs_hook=unique)


def write(path, value):
    descriptor, temporary = tempfile.mkstemp(prefix='.write-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'w') as output:
            json.dump(value, output, sort_keys=True)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
        parent = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(parent)
        finally:
            os.close(parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def locked(root, create):
    if create:
        root.mkdir(mode=0o700, parents=True, exist_ok=True)
    owned(root, directory=True, private=True)
    descriptor = os.open(root/'install.lock', os.O_RDWR | os.O_NOFOLLOW | (os.O_CREAT if create else 0), 0o600)
    try:
        owned(root/'install.lock', private=True)
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        os.close(descriptor)


def relative(value):
    return isinstance(value, str) and bool(re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]*(?:/[A-Za-z0-9_-][A-Za-z0-9_.-]*)*', value))


def fingerprints(config):
    for name, expected in config['files'].items():
        path = owned(name, system=True)
        require(re.fullmatch(r'[0-9a-f]{64}', expected) and sha(path.read_bytes()) == expected, 'trusted-input-changed')


def configuration(path):
    config = read(path)
    require(isinstance(config, dict) and set(config) == FIELDS and config['schemaVersion'] == 1 and
            config['repository'] == REPOSITORY, 'configuration-invalid')
    require(isinstance(config['owner'], str) and re.fullmatch(r'[A-Za-z0-9_.-]{1,128}', config['owner']), 'owner-invalid')
    checkout = owned(config['checkout'], directory=True)
    require(not Path(path).is_relative_to(checkout), 'configuration-in-checkout')
    roots = [Path(config[key]) for key in ['stateDirectory', 'evidenceRoot']]
    require(all(p.is_absolute() and p.resolve() == p and not p.is_relative_to(checkout) for p in roots) and
            not roots[0].is_relative_to(roots[1]) and not roots[1].is_relative_to(roots[0]), 'private-roots-invalid')
    require(isinstance(config['files'], dict) and 1 <= len(config['files']) <= 1000, 'fingerprints-invalid')
    for key in ['allowedPaths', 'protectedPaths']:
        require(isinstance(config[key], list) and len(config[key]) <= 10000 and all(relative(p) for p in config[key]), 'path-policy-invalid')
    require(config['allowedPaths'] and isinstance(config['requiredSkills'], list) and config['requiredSkills'] and
            all(isinstance(s, str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', s) and len(s) < 64 for s in config['requiredSkills']), 'required-skills-invalid')
    require(isinstance(config['path'], str) and config['path'] and all(Path(p).is_absolute() for p in config['path'].split(os.pathsep)), 'tool-path-invalid')
    for directory in config['path'].split(os.pathsep):
        owned(Path(directory).resolve(), directory=True, system=True)
    needed = {str(checkout/'scripts'/name) for name in ['manage-skills.sh', 'validate-skills.py']}
    for tool in TOOLS:
        resolved = shutil.which(tool, path=config['path'])
        require(resolved is not None, 'required-tool-missing')
        needed.add(str(Path(resolved).resolve()))
    require(needed <= set(config['files']) and config['git'] == str(Path(shutil.which('git', path=config['path'])).resolve()), 'tools-not-pinned')
    fingerprints(config)
    require(isinstance(config['links'], list) and config['links'] and len(config['links']) <= 1000, 'links-invalid')
    keys = []
    for link in config['links']:
        require(isinstance(link, dict) and set(link) == {'agent', 'skill', 'path'} and link['agent'] in {'codex', 'claude'} and
                link['skill'] in config['requiredSkills'], 'link-policy-invalid')
        keys.append((link['agent'], link['skill']))
    require(len(keys) == len(set(keys)) and set(config['requiredSkills']) == {s for _, s in keys} and
            {a for a, _ in keys} == {'codex', 'claude'}, 'required-link-coverage-missing')
    return config, sha(Path(path).read_bytes())


def environment(config):
    # No caller-supplied source/target overrides, shell startup or Python imports.
    return {'PATH': config['path'], 'LANG': 'C.UTF-8', 'PYTHONNOUSERSITE': '1', 'PYTHONSAFEPATH': '1',
            'PYTHONDONTWRITEBYTECODE': '1', 'GIT_OPTIONAL_LOCKS': '0', 'GIT_ATTR_NOSYSTEM': '1', 'GIT_TERMINAL_PROMPT': '0'}


def git(config, arguments, deadline, *, mutation=False):
    require(time.time() < deadline, 'deadline-expired')
    result = subprocess.run([config['git'], '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false',
                             '-c', 'core.attributesFile=/dev/null', '-c', 'core.autocrlf=false', '-c', 'submodule.recurse=false',
                             '-c', 'merge.autostash=false', '-C', config['checkout'], *arguments],
                            env=environment(config), capture_output=True, timeout=None if mutation else min(30, deadline-time.time()))
    require(result.returncode == 0 and len(result.stdout)+len(result.stderr) <= LIMIT, 'git-operation-incomplete')
    return result.stdout


def identity(config, deadline):
    checkout = Path(config['checkout'])
    require((checkout/'.git').is_dir() and not (checkout/'.git').is_symlink(), 'canonical-checkout-required')
    for arguments, expected in [(['rev-parse', '--show-toplevel'], config['checkout']), (['symbolic-ref', 'HEAD'], 'refs/heads/main')]:
        require(git(config, arguments, deadline).decode().strip() == expected, 'canonical-main-required')
    require(git(config, ['remote', 'get-url', 'origin'], deadline).decode().strip() in REMOTE_URLS, 'origin-mismatch')
    return git(config, ['rev-parse', 'HEAD'], deadline).decode().strip()


def tree(config, revision, deadline):
    result = {}
    for row in git(config, ['ls-tree', '-r', '-z', revision], deadline).split(b'\0'):
        if row:
            fields, name = row.split(b'\t', 1)
            mode, kind, oid = fields.decode().split()
            result[name.decode()] = (mode, kind, oid)
    require(len(result) <= 10000 and not any(Path(p).name == '.gitattributes' for p in result), 'unsupported-tree-or-attributes')
    return result


def record(root, name):
    path = owned(Path(root, name))
    require(path.stat().st_size <= LIMIT, 'file-too-large')
    data = path.read_bytes()
    return {'path': name, 'sha256': sha(data), 'size': len(data), 'mode': '100755' if path.stat().st_mode & 0o111 else '100644'}


def dirty(config, deadline):
    root = Path(config['checkout'])
    require(not (root/'.git/info/attributes').exists() and not (root/'.git/info/attributes').is_symlink(), 'attribute-processing-unsupported')
    for name in git(config, ['ls-files', '--cached', '--others', '--exclude-standard', '-z'], deadline).split(b'\0'):
        if name:
            for parent in (root/name.decode()).parents:
                if parent.is_relative_to(root):
                    require(not (parent/'.gitattributes').exists() and not (parent/'.gitattributes').is_symlink(), 'attribute-processing-unsupported')
    rows = git(config, ['status', '--porcelain=v1', '-z', '--untracked-files=all'], deadline).split(b'\0')
    index = git(config, ['ls-files', '--stage', '-z'], deadline).split(b'\0')
    result, offset = [], 0
    while offset < len(rows) and rows[offset]:
        row = rows[offset]; state, name = row[:2].decode(), row[3:].decode()
        names = [name]
        if 'R' in state or 'C' in state:
            offset += 1; names.append(rows[offset].decode())
        for name in names:
            require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'dirty-path-invalid')
            path = root/name
            require(path.parent.resolve() == path.parent, 'dirty-parent-link')
            content = {'link': os.readlink(path)} if path.is_symlink() else record(root, name) if path.exists() else {'absent': True}
            result.append({'path': name, 'status': state, 'content': content,
                           'index': [v.decode() for v in index if v.endswith(b'\t'+name.encode())]})
        offset += 1
    require(len(result) <= 1000, 'dirty-inventory-too-large')
    return result


def links(config):
    result, roots = [], {}
    for selected in config['links']:
        path = Path(selected['path']); target = Path(config['checkout'], 'skills', selected['skill'])
        require(path.is_absolute() and path.name == selected['skill'] and not path.is_relative_to(config['checkout']), 'link-path-invalid')
        owned(path.parent, directory=True)
        info = path.lstat()
        require(stat.S_ISLNK(info.st_mode) and info.st_uid == os.getuid() and path.resolve(strict=True) == target and
                target.resolve() == target and target.is_dir(), 'existing-link-missing-or-foreign')
        require(selected['agent'] not in roots or roots[selected['agent']] == str(path.parent), 'multiple-host-roots')
        roots[selected['agent']] = str(path.parent)
        result.append(selected | {'target': os.readlink(path), 'device': info.st_dev, 'inode': info.st_ino})
    selected_keys = {(v['agent'], v['skill']) for v in result}
    for agent, root in roots.items():
        for skill in config['requiredSkills']:
            path = Path(root, skill)
            if path.is_symlink() and path.resolve() == Path(config['checkout'], 'skills', skill):
                require((agent, skill) in selected_keys, 'installed-target-not-declared')
    return result, roots


def manager(config, deadline, action, *, dry_run=False):
    inventory, roots = links(config)
    fingerprints(config)
    env = environment(config) | {'CODEX_SKILLS_DIR': roots['codex'], 'CLAUDE_SKILLS_DIR': roots['claude']}
    output = {}
    for agent in ['codex', 'claude']:
        arguments = ['status', '--agent', agent] if action == 'status' else ['install', '--agent', agent, '--existing-only', *(['--dry-run'] if dry_run else []), *[v['skill'] for v in inventory if v['agent'] == agent]]
        require(time.time() < deadline, 'deadline-expired')
        result = subprocess.run([shutil.which('bash', path=config['path']), str(Path(config['checkout'], 'scripts/manage-skills.sh')), *arguments],
                                cwd=config['checkout'], env=env, capture_output=True, timeout=min(60, deadline-time.time()))
        require(result.returncode == 0 and len(result.stdout)+len(result.stderr) <= LIMIT, 'manager-readback-incomplete')
        if action == 'status':
            rows = result.stdout.decode().splitlines()
            require(all(f"{agent} {v['skill']}: correctly installed ({v['path']})" in rows for v in inventory if v['agent'] == agent), 'manager-required-link-incomplete')
            output[agent] = {'status': 'correct', 'sha256': sha(result.stdout)}
    require(links(config)[0] == inventory, 'manager-link-identity-changed')
    return output


def protected(config, name):
    paths = ['AGENTS.md', 'README.md', 'scripts', *ACTIVE, *config['protectedPaths']]
    paths += [str(Path(p).relative_to(config['checkout'])) for p in config['files'] if Path(p).is_relative_to(config['checkout'])]
    return any(name == p or name.startswith(p+'/') for p in paths)


def baseline(config, plan, deadline):
    before = tree(config, plan['previousRevision'], deadline)
    for value in plan['files']:
        name = value['path']
        if name in before:
            mode, kind, oid = before[name]
            require(kind == 'blob' and mode in {'100644', '100755'}, 'baseline-kind-unsupported')
            current = record(config['checkout'], name)
            require(current['mode'] == mode and current['sha256'] == sha(git(config, ['cat-file', 'blob', oid], deadline)), 'affected-skill-dirty')
        else:
            path = Path(config['checkout'], name)
            require(not path.exists() and not path.is_symlink(), 'new-resource-occupied')


def prepare(config, request, config_sha):
    deadline = request['deadline']; previous = identity(config, deadline)
    require(previous != request['merge'], 'target-already-present-without-receipt')
    git(config, ['fetch', '--no-tags', '--no-recurse-submodules', 'origin', 'refs/heads/main'], deadline)
    remote = git(config, ['rev-parse', 'FETCH_HEAD'], deadline).decode().strip()
    for a, b in [(previous, request['merge']), (request['merge'], remote)]:
        git(config, ['merge-base', '--is-ancestor', a, b], deadline)
    before, target = tree(config, previous, deadline), tree(config, request['merge'], deadline)
    catalog = lambda t: {p.split('/')[1] for p in t if p.startswith('skills/') and p.endswith('/SKILL.md') and len(p.split('/')) == 3}
    require(catalog(before) == catalog(target), 'new-renamed-or-retired-skill-needs-discovery')
    require(set(config['requiredSkills']) <= catalog(target), 'required-skill-not-in-reviewed-catalog')
    changed = [p.decode() for p in git(config, ['diff', '--no-renames', '--name-only', '-z', previous, request['merge']], deadline).split(b'\0') if p]
    require(changed and len(changed) <= 1000 and all(relative(p) and p.split('/')[0] in {'skills', 'tests', 'docs'} and
            p in config['allowedPaths'] and not protected(config, p) for p in changed), 'unreviewed-or-protected-bundle')
    affected = {p.split('/')[1] for p in changed if p.startswith('skills/')}
    require(affected and affected <= set(config['requiredSkills']), 'changed-skill-not-selected-or-installed')
    selected = sorted(set(changed) | {p for p in target if p.startswith('skills/') and p.split('/')[1] in affected})
    require(set(selected) <= set(config['allowedPaths']) and all(p in target and target[p][0] in {'100644', '100755'} and target[p][1] == 'blob' for p in selected), 'uncovered-files-or-removal')
    saved_dirty = dirty(config, deadline)
    require(not any(v['path'] in changed or any(v['path'].startswith('skills/'+s+'/') for s in affected) for v in saved_dirty), 'affected-skill-dirty')
    files = []
    for name in selected:
        data = git(config, ['cat-file', 'blob', target[name][2]], deadline)
        files.append({'path': name, 'sha256': sha(data), 'size': len(data), 'mode': target[name][0]})
    inventory, _ = links(config)
    manager(config, deadline, 'status'); manager(config, deadline, 'install', dry_run=True)
    commits = git(config, ['rev-list', '--reverse', previous+'..'+request['merge']], deadline).decode().splitlines()
    require(len(commits) <= 1000, 'included-commit-bound')
    plan = {'schemaVersion': 1, 'repository': REPOSITORY, 'issue': request['issue'], 'owner': config['owner'], 'checkout': config['checkout'],
            'previousRevision': previous, 'targetRevision': request['merge'], 'remoteMain': remote, 'commits': commits,
            'files': files, 'links': inventory, 'requiredSkills': config['requiredSkills'], 'preservedDirty': saved_dirty,
            'configSha256': config_sha, 'deadline': deadline}
    baseline(config, plan, deadline)
    return plan


def verify(config, request, plan):
    require(identity(config, request['deadline']) == request['merge'] and links(config)[0] == plan['links'], 'installed-identity-changed')
    files = [record(config['checkout'], v['path']) for v in plan['files']]
    require(files == plan['files'], 'installed-files-incomplete')
    for link in plan['links']:
        prefix = 'skills/'+link['skill']+'/'
        for value in files:
            if value['path'].startswith(prefix):
                path = Path(link['path'], value['path'][len(prefix):])
                require(path.resolve(strict=True) == Path(config['checkout'], value['path']) and sha(path.read_bytes()) == value['sha256'], 'loading-readback-incomplete')
    require(dirty(config, request['deadline']) == plan['preservedDirty'], 'unrelated-state-changed')
    return {'kind': 'installed-files', 'revision': request['merge'], 'files': files, 'links': plan['links'],
            'preservedDirtySha256': digest(plan['preservedDirty']), 'managerStatus': manager(config, request['deadline'], 'status')}


def run(config_path, request):
    result = {'schemaVersion': 1, 'readbackKind': 'installed-files', 'repository': request.get('repository'),
              'merge': request.get('merge'), 'owner': request.get('owner')}
    uncertain = True
    try:
        config, config_sha = configuration(config_path)
        require(set(request) == REQUEST and request['schemaVersion'] == 1 and request['repository'] == REPOSITORY and
                request['owner'] == config['owner'] and request['operation'] in {'install', 'reconcile'} and
                type(request['issue']) is int and request['issue'] > 0 and re.fullmatch(r'[0-9a-f]{40}', request['merge']) and
                type(request['deadline']) in {int, float} and math.isfinite(request['deadline']) and time.time() < request['deadline'], 'request-invalid')
        evidence = owned(request['evidenceDirectory'], directory=True, private=True)
        parent = owned(config['evidenceRoot'], directory=True, private=True)
        require(evidence != parent and evidence.is_relative_to(parent) and not any(evidence.iterdir()), 'evidence-directory-invalid')
        root = Path(config['stateDirectory']); key = digest({'repository': REPOSITORY, 'issue': request['issue'], 'merge': request['merge']})
        with locked(root, request['operation'] == 'install'):
            active, saved = read(root/'active.json'), read(root/(key+'.json'))
            uncertain = bool(active and active['status'] != 'complete')
            require(not uncertain or active['key'] == key, 'another-installation-unreconciled')
            if saved:
                plan = saved['plan']
                require(saved['planSha256'] == digest(plan) and plan['configSha256'] == config_sha and
                        plan['repository'] == REPOSITORY and plan['issue'] == request['issue'] and plan['owner'] == request['owner'] and
                        plan['targetRevision'] == request['merge'], 'saved-plan-mismatch')
                require(saved['status'] == 'complete' or request['operation'] == 'reconcile', 'read-only-reconciliation-required')
            else:
                require(request['operation'] == 'install', 'no-owned-installation-to-reconcile')
                plan = prepare(config, request, config_sha); write(evidence/'plan.json', plan)
                require(configuration(config_path)[1] == config_sha and identity(config, request['deadline']) == plan['previousRevision'] and
                        links(config)[0] == plan['links'] and dirty(config, request['deadline']) == plan['preservedDirty'], 'prepared-input-changed')
                baseline(config, plan, request['deadline'])
                require(time.time() < request['deadline'], 'deadline-expired')
                saved = {'status': 'pending', 'plan': plan, 'planSha256': digest(plan)}
                write(root/(key+'.json'), saved); write(root/'active.json', {'key': key, 'status': 'pending'}); uncertain = True
                git(config, ['merge', '--ff-only', '--no-edit', '--no-stat', request['merge']], request['deadline'], mutation=True)
                manager(config, request['deadline'], 'install', dry_run=True)
                manager(config, request['deadline'], 'install')
            require(configuration(config_path)[1] == config_sha, 'configuration-changed')
            readback = verify(config, request, plan)
            receipt = {'schemaVersion': 'installed-files/1.0', 'repository': REPOSITORY, 'issue': request['issue'], 'owner': config['owner'],
                       'outcome': 'succeeded', 'targetRevision': request['merge'], 'plan': plan, 'planSha256': digest(plan),
                       'readback': readback, 'verifiedAt': time.time()}
            path = evidence/'installed-files.json'; write(path, receipt)
            proof = {'path': str(path), 'sha256': sha(path.read_bytes())}
            write(root/(key+'.json'), saved | {'status': 'complete', 'receipt': proof})
            write(root/'active.json', {'key': key, 'status': 'complete'})
            return result | {'status': 'installed', 'installedRevision': request['merge'], 'receipt': proof}
    except (OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as error:
        reason = str(error) if re.fullmatch(r'[a-z][a-z0-9-]{0,100}', str(error)) else 'installation-evidence-unavailable'
        return result | {'status': 'uncertain' if uncertain else 'blocked', 'effects': 'uncertain' if uncertain else 'none', 'reason': reason}


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--config', required=True)
    arguments = parser.parse_args()
    try:
        data = sys.stdin.read(65537); require(len(data) <= 65536, 'request-too-large')
        request = json.loads(data, object_pairs_hook=unique); require(isinstance(request, dict), 'request-invalid')
        print(json.dumps(run(arguments.config, request), sort_keys=True))
    except (OSError, ValueError):
        print(json.dumps({'schemaVersion': 1, 'status': 'blocked', 'effects': 'none', 'reason': 'request-invalid'}))


if __name__ == '__main__':
    main()
