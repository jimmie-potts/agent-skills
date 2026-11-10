# Reviewer case format

A reviewer case records a defect that independent review missed and that a
later pull request fixed after merge. Cases let a later change to the review
skills be judged against real misses. They authorize no trial: the owner
decided on 2026-11-09 to collect cases and run none until a separate
authorization
([agent-device-hub#1602](https://github.com/jimmie-potts/agent-device-hub/issues/1602)).
They are not preparation for the postponed workflow benchmark
([#44](https://github.com/jimmie-potts/agent-skills/issues/44)).

Each case has two parts, kept in separate files so the answer can be withheld
from the reviewer by access
([#82](https://github.com/jimmie-potts/agent-skills/issues/82)):

- **Input**, in `cases.md` under `## RVnn: <neutral title>`:
  - the requirement the change was meant to meet, written as the original
    author could have stated it, without naming the defect;
  - any unchanged code the original reviewer could have read and needed;
  - a synthetic or sanitized diff that reproduces the defect in as few lines
    as possible.
- **Grader**, in `graders.md` under the same `## RVnn` heading:
  - the defect a reviewer should find, as a failure condition;
  - what a finding must name to count, the expected severity, and near misses
    that do not count;
  - links to where the real miss was recorded: the pull request that
    introduced the defect, the pull request that fixed it, and the issue that
    reported or owns it.

Inputs carry no links, issue numbers or answers. The source pull requests
describe the defect, so a link in the input would give it away.

Write every case as a synthetic reduction: rename product identifiers, keep only
the code needed to show the defect, and include no private session content,
credentials, device or network addresses, locations or personal data.

To run a case, once a trial is authorized, give the evaluated reviewer
`cases.md` and the review skill under test only. Withhold `graders.md` and this
fixture's other files. Until #82 establishes access-based withholding, record
the withholding as instruction-only. Score each returned finding against the
grader after the reviewer returns.

To add a case, start from a merged pull request that fixes a defect introduced
by an earlier reviewed and merged pull request. Add its input and grader under
the next free `RVnn`; `tests/workflow-evaluation-test.py` checks that the two
files stay paired and that inputs stay link-free.
