# Review skill evaluation scenarios

Use `tests/fixtures/workflow-evaluation/review-work-cases.md` for routing,
standalone and composed review, reviewer independence, result states, finding
continuity, resumption and adoption of this skill into an installed catalog.
Withhold `review-work-graders.md`, recorded observations, this evaluation-only
reference and the validation scenarios of deliver-work and plan-work from every
evaluated context, even when an entrypoint links them.

For finding identity, fix verification and explicit limits that deliver-work's
corrections share with this skill, also use
`tests/fixtures/workflow-evaluation/review-cycles-cases.md` and withhold
`review-cycles-graders.md` in the same way.

For retained reviewer returns and the states a result must not hide, also use
`tests/fixtures/workflow-evaluation/review-evidence-cases.md` and withhold
`review-evidence-graders.md` in the same way.

Read `review-work-observations.md` in that fixture directory only after
scoring.

Give each evaluated context the case inputs, the candidate entrypoints and the
operating references they select, never the expected answers. Record actual
decisions, proposed effects, sources read and limits. Require every case to pass
with no gate waiver or authority violation.

Keep these kinds of evidence apart:

- Static checks: `tests/review-work-test.py` parses the result contract and
  its retained returns, rejects known-bad records and checks the migration's
  reference closure.
- Simulated decisions: fresh read-only contexts decide the cases. Label the
  withholding as instruction-only unless available filesystem, Git and network
  tools were shown unable to reach the withheld files.
- Host discovery and live review: a fresh host session discovering this skill
  and running real reviewers. Static checks and simulations prove neither.
