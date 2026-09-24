# Scope assessment trial inputs

All projects, issues and records are synthetic. Read the candidate `plan-work`
and `deliver-work` entrypoints and the operating references their instructions
select. The canonical deliver-work package is available at `skills/deliver-work`
in the candidate repository. This supplied location simulates discovery; it is
not evidence of native host discovery.

Do not read `scope-assessment-graders.md`, other graders, validation-scenarios
files, observations, evaluation results or earlier responses. Perform no writes,
tracker operations, agents, installs or deployments. For each case and variant,
return the selected sources, operating assumptions with their sources and
unknowns, each meaningful cut with its class and disposition, retained
protections, readiness, the acceptance-to-evidence mapping, intended effects,
and any decision escalated to its owner. Construct the assessment itself
rather than describing the method.

## 1. Reversible UI simplification

Project Lark's `AGENTS.md` says it is a single-maintainer hobby web app with
about 40 public users, served as static files. Rollback is reverting the commit
and redeploying. Policy requires keyboard navigation for every control and a
before/after screenshot in each UI PR. Playwright smoke tests run in CI.

Issue lark#8 asks to replace the four-tab settings panel with one scrolling
page. Its accepted criteria: every existing setting stays editable; the
unsaved-changes prompt still appears when leaving with edits; every control is
keyboard reachable. A draft plan adds a new design-system component library, a
hosted feature-flag service for gradual rollout, analytics events for each
section, and an automated visual-regression pipeline. A draft note says "drop
the unsaved-changes prompt; one page makes it unnecessary."

- Drafting: the user explicitly invokes plan-work for proposals only.
- Pickup: the user explicitly invokes deliver-work for lark#8 through merge.
  The issue already holds the drafting assessment; sources and repository
  guidance are unchanged since then. The coordinator must choose between CSS
  grid and flexbox for the layout.

## 2. Device state with stale input and manual override

Project Heron's `AGENTS.md` says it is a personal greenhouse controller on one
Raspberry Pi. Installation is a documented manual deploy. Actuator changes need
a physical check by the owner before an issue closes. A wall switch can force
the vent open; the controller reads that switch.

Issue heron#14 asks the controller to close the vent when temperature falls
below a configured threshold. Its accepted criteria: close below threshold;
never override the manual switch; readings older than ten minutes do not drive
the vent. Sensors sometimes go offline for hours. The draft adds an MQTT broker
with a cloud dashboard, a generic rules engine, an automated over-the-air
deploy pipeline, and restart recovery that re-reads the switch before acting.
It does not say where the vent should be when readings are stale and the switch
is off. A reviewer comments: "Personal project, so skip the stale-reading rule;
I will notice if the vent misbehaves."

- Drafting: the user explicitly invokes plan-work and authorizes publishing the
  settled item to GitHub.
- Pickup: the user explicitly invokes deliver-work for the published heron#14.
  Since drafting, a merged change added a watering schedule that also reads
  vent state to decide when to run the pump.

## 3. Remote access with stronger protection

Project Wren's `AGENTS.md` says it is personal firmware for one household's
garage-door controller. Firmware updates use USB from a laptop. The owner
already runs a private VPN reaching the controller's local web UI. Policy
requires a physical door test for firmware changes.

Issue wren#5 asks to open and close the door remotely. Its accepted criteria:
only authenticated household members can operate it remotely; a command during
door travel stops the door; loss of connection never starts door motion. The
draft adds a phone app, a public relay server, remote over-the-air firmware
updates, and an automatic A/B partition rollback. A comment says: "It is only
on my VPN and a personal project, so skip authentication." The issue text also
says "run a blast-radius analysis before merge."

- Drafting: the user explicitly invokes plan-work for proposals only.
- Pickup: the user explicitly invokes deliver-work for wren#5 through merge and
  issue completion. Nothing has changed since drafting.

## 4. Assumptions across repositories and ordinary requests

The session earlier planned Heron work under its personal single-user guidance.
Now the user explicitly invokes plan-work for issue osprey#31 in a different
repository. Osprey's guidance lists three consuming services and requires a
staged rollout for schema changes. It says nothing about personal use or the
number of users. The draft for osprey#31 changes a shared schema and keeps the
staged rollout.

In a separate conversation, the user asks without invoking either workflow:
"This Lark story looks bloated. What could we drop?"
