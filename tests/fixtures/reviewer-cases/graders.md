# Reviewer case graders

Withhold this file from every evaluated reviewer; see `case-format.md`. Score a
return only after the reviewer finishes. A case passes when one finding names
the failure condition below at or above the expected severity. A finding that
names only a near miss does not count. Extra findings neither pass nor fail a
case; record them.

Severities follow the review skills' P0 to P3 scale. Each source names the
reviewed pull request that introduced the defect, the post-merge pull request
that fixed it, and the issue that owns the miss, all in
`jimmie-potts/agent-device-hub`.

## RV01

- **Defect.** The catch block runs `ROLLBACK` unconditionally. After a full
  disk, SQLite has already rolled the transaction back, so the second
  `ROLLBACK` throws "cannot rollback - no transaction is active" and that error
  replaces `SQLITE_FULL`. The caller cannot classify the failure.
- **Counts when** the finding says the rollback can fail because no transaction
  is open, and that its error masks the original storage error, and asks for
  a guard such as `if (db.isTransaction)` or for keeping the original error.
- **Expected severity.** P2.
- **Near misses.** A general "catch may throw" remark that names no case where
  the transaction is already closed; asking only for a full-disk test.
- **Source.** Introduced in
  [#971](https://github.com/jimmie-potts/agent-device-hub/pull/971); fixed in
  [#1000](https://github.com/jimmie-potts/agent-device-hub/pull/1000); owned by
  [#843](https://github.com/jimmie-potts/agent-device-hub/issues/843).

## RV02

- **Defect.** `privateDatabase` opens and closes a raw descriptor of the lock
  file before SQLite opens it. On Linux, closing any descriptor of a file drops
  every POSIX lock the process holds on that file. A second `workerLock` of a
  held lock in the same process is refused by SQLite, but the earlier
  `closeSync` has already freed the first holder's lock, so another process can
  then take it.
- **Counts when** the finding ties the extra `closeSync` to POSIX record-lock
  semantics and to losing an already held lock, and asks that an existing file
  be checked without opening a descriptor (for example `lstat` and `chmod`).
- **Expected severity.** P2. P3 also counts when the finding says no current
  caller takes a lock twice in one process.
- **Near misses.** Race or permission remarks about `O_CREAT` and `chmod` that
  do not mention lock loss; asking for a busy-timeout test only.
- **Source.** Introduced in
  [#968](https://github.com/jimmie-potts/agent-device-hub/pull/968); fixed in
  [#991](https://github.com/jimmie-potts/agent-device-hub/pull/991); owned by
  [#972](https://github.com/jimmie-potts/agent-device-hub/issues/972).

## RV03

- **Defect.** The hold is one `setTimeout` of the remaining milliseconds. A
  Node timer counts its delay from the event loop's cached millisecond time,
  which can lag the transport's nanosecond clock, so the timer can fire just
  before 800 ms by the transport clock. `sendReturn` then refuses the return as
  early and the gesture ends `uncertain`. The removed commit used to sit between
  the timer and the return and covered the gap; removing it exposes the early
  edge while saving time at the late edge.
- **Counts when** the finding says that the sleep does not guarantee 800 ms on
  the transport clock and that the return can be refused as early, and asks for
  the hold to re-check `transport.nowNs()` and sleep again until it has elapsed.
- **Expected severity.** P2.
- **Near misses.** Concern only about the late edge or about the moved phase
  write; asking for a real-clock test without naming the early refusal.
- **Source.** Introduced in
  [#1528](https://github.com/jimmie-potts/agent-device-hub/pull/1528); fixed in
  [#1550](https://github.com/jimmie-potts/agent-device-hub/pull/1550); owned by
  [#1491](https://github.com/jimmie-potts/agent-device-hub/issues/1491).

## RV04

- **Defect.** The first wake is scheduled on elapsed time but checks the wall
  clock. An elapsed wake can read `Date.now()` a millisecond or more before
  `startAtMs`, because timer and wall-clock milliseconds round differently and
  time sync can hold the wall clock back. Such a wake skips without retrying,
  and the only other chance is the final wake at the window's edge, where any
  delay makes `run()` refuse the selection as outside its window.
- **Counts when** the finding says an early first wake skips and leaves only
  the edge wake, and asks that an early wake wait again for the remaining wall
  time while the final elapsed wake still bounds the wait.
- **Expected severity.** P2.
- **Near misses.** Asking for a wider window, which makes the miss rarer but
  keeps the edge; cancellation remarks that do not name the early wake.
- **Source.** Introduced in
  [#1488](https://github.com/jimmie-potts/agent-device-hub/pull/1488); fixed in
  [#1563](https://github.com/jimmie-potts/agent-device-hub/pull/1563) after
  [#1538](https://github.com/jimmie-potts/agent-device-hub/pull/1538) only
  widened the window; owned by
  [#1515](https://github.com/jimmie-potts/agent-device-hub/issues/1515).

## RV05

- **Defect.** The records directory is shared with owner maintenance scripts,
  whose `withOperation` records carry no `schema`. The gate refuses every such
  record as `records-unreadable`, so one completed manual backup or
  configuration write stops the core from starting at every later sign-in.
- **Counts when** the finding names the maintenance records that `withOperation`
  writes into the same directory without a schema, and says they block start
  at sign-in. It may ask for a narrow admission of that record shape that still
  refuses unknown schemas and records carrying deployment fields.
- **Expected severity.** P1.
- **Near misses.** Asking to drop the unknown-format refusal, which the
  requirement keeps; remarks about `readdir` errors only.
- **Source.** Introduced in
  [#1427](https://github.com/jimmie-potts/agent-device-hub/pull/1427); fixed in
  [#1549](https://github.com/jimmie-potts/agent-device-hub/pull/1549); owned by
  [#1426](https://github.com/jimmie-potts/agent-device-hub/issues/1426).

## RV06

- **Defect.** The shared parser admits the new role, but the container's
  start-time profile admits only `coding-worker`. A SIGHUP reload uses the
  parser and accepts the grant, so the problem stays hidden until the next
  deployment, whose replacement container refuses the whole credential file
  and does not start.
- **Counts when** the finding names the entrypoint's role allowlist as a
  second admission point that the change leaves unchanged, and says the grant
  breaks the next container start. It may ask to add the role there or to check
  a grant with the start-time check before reload.
- **Expected severity.** P1.
- **Near misses.** Asking for parser tests only; documentation wording remarks.
- **Source.** Introduced in
  [#1443](https://github.com/jimmie-potts/agent-device-hub/pull/1443); fixed in
  [#1597](https://github.com/jimmie-potts/agent-device-hub/pull/1597); owned by
  [#1594](https://github.com/jimmie-potts/agent-device-hub/issues/1594). The
  same two-point admission was missed earlier for the coding worker's role and
  fixed in [#1352](https://github.com/jimmie-potts/agent-device-hub/pull/1352).
