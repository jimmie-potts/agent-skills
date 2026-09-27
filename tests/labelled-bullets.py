"""Check that a Markdown section keeps its labelled bullets and their anchors.

A labelled bullet starts `- Label: ` at column 0 and indented lines continue
it. Anchors match case-insensitively with whitespace normalized, so every
other word may change. Each gap names the label it concerns.
"""
import re

BULLET = re.compile(r'^- ([A-Z][^:\n`]{0,40}): (.*\n(?:  .*\n)*)', re.MULTILINE)


def flat(text):
    return ' '.join(text.split()).lower()


def section_span(text, heading):
    """Return the (start, end) offsets of a section's body, or None."""
    match = re.search(rf'^{re.escape(heading)}\n', text, re.MULTILINE)
    if not match:
        return None
    level = len(heading) - len(heading.lstrip('#'))
    end = re.compile(rf'^#{{1,{level}}} ', re.MULTILINE).search(text, match.end())
    return match.end(), end.start() if end else len(text)


def bullets(text, heading):
    """Return [(label, match)] for the section's labelled bullets, or None."""
    span = section_span(text, heading)
    if span is None:
        return None
    return [(match.group(1), match)
            for match in BULLET.finditer(text, *span)]


def gaps(text, heading, required):
    """Name each required label or anchor that the section is missing."""
    found = bullets(text, heading)
    if found is None:
        return [f'{heading}: missing section']
    result = []
    for label, anchors in required.items():
        bodies = [flat(match.group(2)) for name, match in found if name == label]
        if not bodies:
            result.append(f'{label}: missing from {heading}')
            continue
        if len(bodies) > 1:
            result.append(f'{label}: repeated in {heading}')
        result += [f'{label}: missing anchor "{anchor}"' for anchor in anchors
                   if flat(anchor) not in bodies[0]]
    return result


def controls(text, heading, required):
    """Yield (label, mutation, text) negative controls for each requirement:
    delete its bullet, rename its label and drop each anchor from it."""
    for label, anchors in required.items():
        match = next(match for name, match in bullets(text, heading)
                     if name == label)
        start, body, end = match.start(), match.start(2), match.end()
        yield label, 'delete bullet', text[:start] + text[end:]
        yield label, 'rename label', (
            f'{text[:start]}- Renamed {label}: {text[body:]}')
        for anchor in anchors:
            phrase = r'\s+'.join(map(re.escape, anchor.split()))
            yield label, f'drop anchor "{anchor}"', (
                text[:body] + re.sub(phrase, 'X', text[body:end],
                                     flags=re.IGNORECASE) + text[end:])


def assert_guarded(case, text, heading, required):
    """Fail `case` on any gap, then show that each control produces a gap
    naming the label it mutated."""
    case.assertEqual(gaps(text, heading, required), [])
    for label, mutation, mutated in controls(text, heading, required):
        with case.subTest(label=label, mutation=mutation):
            case.assertNotEqual(mutated, text)
            found = gaps(mutated, heading, required)
            case.assertTrue(any(gap.startswith(f'{label}: ') for gap in found),
                            found)
