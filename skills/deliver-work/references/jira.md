# Jira tracking

Use this reference only when Jira owns the work item. Jira tracking and code
hosting are independent choices; a Jira issue does not imply a GitHub repository.

Resolve the Jira site and project as well as the key. Read the authoritative
issue, acceptance fields, relevant scope decisions, current status, resolution,
dependencies and sprint. Verify ambiguous dependency directions from both
endpoints. Do not take ownership of outgoing dependents or linked issues.

Discover the workflow meaning of starting, reviewing, waiting and completing
work from project sources. Immediately before each authorized transition, fetch
available transitions from the current issue state and their required fields.
Use the live transition ID and valid field values. Do not guess from familiar
status names, hard-code IDs or treat a status category as acceptance evidence.

Read back the changed status and resolution when applicable. A resumed issue
need not traverse earlier statuses. If no intermediate checkpoint is defined,
retain current tracking state rather than inventing a transition. Missing
information required for completion blocks that transition, while independent
work can continue. Preserve sprint membership/lifecycle, assignment and unrelated
fields unless separately authorized.

For an uncertain transition, inspect fresh issue state and available change
history before recovery. Do not resend a transition to test whether it worked.
Use the entrypoint's recovery rules when authoritative evidence is unavailable.

API reference: [Jira issues and transitions](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/).
