#!/usr/bin/env python3
"""Evaluate supplied setting evidence; collect no telemetry and switch no models."""
import argparse
import json
import sys


class InvalidEvidence(ValueError):
    """Input cannot support a setting decision."""


def fields(value, required):
    if not isinstance(value, dict) or set(value) != set(required):
        raise InvalidEvidence('missing or unexpected fields')


def nonempty(value):
    if not isinstance(value, str) or not value.strip():
        raise InvalidEvidence('expected nonempty text')
    return value


def records(value):
    if not isinstance(value, list):
        raise InvalidEvidence('evidence must be a list')
    for item in value:
        fields(item, ('value', 'source'))
        nonempty(item['value'])
        nonempty(item['source'])
    return value


def evaluate(document):
    """Return continue/ask/stop. Input provenance is asserted, never verified here."""
    try:
        fields(document, ('role', 'phase', 'settings', 'aliases'))
        nonempty(document['role'])
        if document['phase'] not in ('pickup', 'resume', 'setting-change', 'pre-launch'):
            raise InvalidEvidence('unknown phase')
        if not isinstance(document['aliases'], list):
            raise InvalidEvidence('aliases must be a list')
        aliases = {}
        for item in document['aliases']:
            fields(item, ('name', 'alias', 'canonical', 'source'))
            if item['name'] not in ('model', 'reasoning'):
                raise InvalidEvidence('unknown alias setting')
            key = (item['name'], nonempty(item['alias']))
            nonempty(item['source'])
            if key in aliases:
                raise InvalidEvidence('duplicate alias')
            aliases[key] = nonempty(item['canonical'])
        # One documented mapping only; chains and cycles obscure equivalence.
        if any((name, target) in aliases for (name, _), target in aliases.items()):
            raise InvalidEvidence('alias chains are unsupported')
        settings = document['settings']
        if not isinstance(settings, list) or not settings:
            raise InvalidEvidence('settings must be a nonempty list')
        outcomes, names = [], set()
        for setting in settings:
            fields(setting, ('name', 'value', 'required', 'verified',
                             'observed', 'declared', 'requested'))
            name = setting['name']
            if name not in ('model', 'reasoning') or name in names:
                raise InvalidEvidence('unknown or duplicate setting')
            names.add(name)
            expected = nonempty(setting['value'])
            if type(setting['required']) is not bool or type(setting['verified']) is not bool:
                raise InvalidEvidence('required and verified must be booleans')
            if setting['verified'] and not setting['required']:
                raise InvalidEvidence('verified identity requires a required setting')
            observed = records(setting['observed'])
            declared = records(setting['declared'])
            requested = records(setting['requested'])  # Never runtime evidence.
            normalize = lambda value: aliases.get((name, value), value)
            values = (requested if document['phase'] == 'pre-launch' else
                      observed or declared)
            mismatch = any(normalize(item['value']) != normalize(expected) for item in values)
            if mismatch:
                status, reason = ('stop' if setting['required'] else 'continue'), 'mismatch'
            elif setting['required'] and not values:
                status, reason = 'ask', 'missing declaration or observation'
            elif document['phase'] == 'pre-launch':
                status, reason = 'bootstrap-only', 'launch controls only; assignment work blocked'
            elif setting['verified'] and not observed:
                status, reason = 'stop', 'verified identity unavailable'
            else:
                status, reason = 'continue', ('observed match' if observed else
                                             'declaration only' if declared else 'advisory unknown')
            outcomes.append(dict(name=name, decision=status, reason=reason,
                                 runtime_verification=('observed' if observed and document['phase'] != 'pre-launch' else 'unknown'),
                                 evidence=setting))
        decision = ('stop' if any(x['decision'] == 'stop' for x in outcomes) else
                    'ask' if any(x['decision'] == 'ask' for x in outcomes) else
                    'bootstrap-only' if document['phase'] == 'pre-launch' else 'continue')
        return dict(decision=decision, role=document['role'], phase=document['phase'],
                    settings=outcomes, aliases=document['aliases'])
    except (InvalidEvidence, TypeError) as error:
        return dict(decision='stop', reason=f'invalid evidence: {error}')


def run_if_allowed(document, action):
    """Call the supplied dependent action once, only after a continuing decision."""
    result = evaluate(document)
    if result['decision'] == 'continue':
        action()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='JSON evidence file; - reads stdin')
    args = parser.parse_args()
    try:
        if args.input == '-':
            document = json.load(sys.stdin)
        else:
            with open(args.input, encoding='utf-8') as stream:
                document = json.load(stream)
        result = evaluate(document)
    except (OSError, ValueError) as error:
        result = dict(decision='stop', reason=f'unreadable evidence: {error}')
    print(json.dumps(result, sort_keys=True))
    return {'continue': 0, 'ask': 2, 'stop': 1, 'bootstrap-only': 3}[result['decision']]


if __name__ == '__main__':
    sys.exit(main())
