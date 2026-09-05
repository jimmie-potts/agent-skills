#!/usr/bin/env bash
# Output-only human-in-the-loop reproduction template.
# Copy and tailor this file only in an authorized disposable location.
# This script has no input channel: it reads no standard input, arguments, or
# environment values and captures nothing. Complete authentication directly in
# the target application. Never paste a credential into a shell prompt.

set -euo pipefail

# Replace these placeholders with the minimum human steps needed to reach the
# symptom and the exact red-capable observation. Keep sign-in or credential
# entry in the target application.
printf '\n>>> <Perform the next reproduction action in the test environment.>\n'
printf '>>> Observe: <Did the exact expected symptom occur?>\n'
printf '>>> After this script exits, report only yes, no, or unclear through the authorized task conversation.\n'
