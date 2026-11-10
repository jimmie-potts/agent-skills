# Reviewer case inputs

These changes are synthetic. Review each one as an independent reviewer covering
correctness, security, tests and the stated requirement. Treat every diff as the
complete change under review and the context as unchanged code you could read.
For each case, return your findings with severity, location and the failure
condition, or say that you found none. Do not read `graders.md` or any other
file in this directory, and make no file, tracker or publication changes.

## RV01: Settings save

**Requirement.** A settings save writes the value and bumps the configuration
revision in one transaction. A failed save leaves both unchanged and throws the
storage error that ended it, so the caller can classify it. A full disk must be
reported as `SQLITE_FULL`.

**Context.** The store uses `node:sqlite` `DatabaseSync`. The database is
opened in WAL mode with exclusive locking.

**Diff.**

```diff
--- a/src/settings-store.ts
+++ b/src/settings-store.ts
@@ -40,3 +40,16 @@ export class SettingsStore {
   get revision(): number {return Number(this.#get('revision') ?? '0');}
+
+  saveSetting(key: string, value: string): void {
+    this.#db.exec('BEGIN IMMEDIATE');
+    try {
+      this.#set(key, value);
+      this.#set('revision', String(this.revision + 1));
+      this.#db.exec('COMMIT');
+    } catch (error) {
+      this.#db.exec('ROLLBACK');
+      throw error;
+    }
+  }
 }
```

## RV02: Private lock files

**Requirement.** Each device worker takes a lock file as an exclusive SQLite
transaction. A second take of a held lock, from this process or another, is
refused, and the first holder keeps its lock. Lock files and their journals are
owner-only (mode 600). A symbolic link in a lock file's place is refused.

**Context.** The service runs on Linux. `workerLock` is exported and may be
called by any in-process caller.

**Diff.**

```diff
--- a/src/sqlite.ts
+++ b/src/sqlite.ts
@@ -1,3 +1,25 @@
+import {chmodSync, closeSync, constants, openSync} from 'node:fs';
+import {DatabaseSync} from 'node:sqlite';
+
+/** Opens a SQLite file only the owner can read or write; its journals inherit the mode. */
+export function privateDatabase(path: string, options: {timeout: number}): DatabaseSync {
+  const descriptor = openSync(path, constants.O_CREAT | constants.O_RDWR | constants.O_NOFOLLOW, 0o600);
+  try {
+    chmodSync(path, 0o600);
+  } finally {
+    closeSync(descriptor);
+  }
+  return new DatabaseSync(path, options);
+}
+
+export function workerLock(path: string): DatabaseSync {
+  const db = privateDatabase(path, {timeout: 0});
+  try {
+    db.exec('BEGIN EXCLUSIVE');
+    return db;
+  } catch (error) {
+    db.close();
+    throw error;
+  }
+}
```

## RV03: Two-step gesture timing

**Requirement.** A gesture sends an outbound move, holds, then sends the return
move. The return must be sent no earlier than 800 ms and no later than 900 ms
after the outbound move, measured on the transport's nanosecond clock;
`sendReturn` refuses an early return and the gesture then ends `uncertain`.
This change stops spending the 100 ms return window on a state commit: the
return phase is now recorded by the return's own transmission commit.

**Context.** `this.#sleep(ms, signal)` wraps `setTimeout`. `transport.nowNs()`
reads a monotonic nanosecond clock. `HOLD_NS` is `800_000_000n`.

**Diff.**

```diff
--- a/src/gesture.ts
+++ b/src/gesture.ts
@@ -88,8 +88,7 @@ class Owner {
     const sentAt = await this.#send(outbound);
-    await this.#transmitted(row);
+    await this.#transmitted(row, false);
     await this.#confirmMotion(sentAt, signal);
     const remaining = Math.ceil(Number(sentAt + HOLD_NS - this.#transport.nowNs()) / 1_000_000);
     if (remaining > 0) await this.#sleep(remaining, signal);
-    await this.#commit(() => {this.#state.phase = 'return';});
     await this.#sendReturn(sentAt);
-    await this.#transmitted(row);
+    await this.#transmitted(row, true);
@@ -120,3 +119,6 @@ class Owner {
-  async #transmitted(row: Row): Promise<void> {
-    await this.#commit(() => {this.#state.last = {requestId: row.requestId};});
+  async #transmitted(row: Row, returned: boolean): Promise<void> {
+    await this.#commit(() => {
+      this.#state.last = {requestId: row.requestId};
+      if (returned) this.#state.phase = 'return';
+    });
   }
```

## RV04: Scheduled selection start

**Requirement.** A scheduled browser selection runs once, within its start
window: no earlier than `startAtMs` and no later than `startAtMs + 5000` on the
wall clock. `run()` re-checks the wall clock and refuses outside the window.
Restart and stop cancel a waiting selection.

**Context.** `options.clock()` returns `Date.now()`. `options.scheduler.after`
schedules on elapsed time and returns a cancellable timer. `latest` is
`startAtMs + 5000`.

**Diff.**

```diff
--- a/src/core/schedule.ts
+++ b/src/core/schedule.ts
@@ -110,0 +111,9 @@ export function createPlans(options: Options) {
+  const arm = (plan: Plan, run: () => void, active: () => boolean): void => {
+    const armedAtMs = options.clock();
+    if (plan.startAtMs <= armedAtMs) {run(); return;}
+    const latest = plan.startAtMs + 5000;
+    const delay = plan.startAtMs - armedAtMs, budget = latest - armedAtMs;
+    // The first wake can be early on the wall clock. Only the final wake may try again.
+    timers.push(options.scheduler.after(delay, () => {if (!active() || options.clock() >= plan.startAtMs) run();}));
+    timers.push(options.scheduler.after(budget, run));
+  };
```

## RV05: Start at sign-in

**Requirement.** At sign-in, a starter starts the installed core unless a start
hold file exists or the operations records show a failed deployment whose
replacement is this container. A record format the starter does not know must
refuse rather than read as "no failed deployment".

**Context.** Unchanged `scripts/operations.mjs` is the shared operation
recorder. Deployments and owner maintenance scripts (backups, configuration
writes) both call it:

```js
export async function withOperation(project, operations, fields, body) {
  const id = randomUUID();
  const path = join(operations, `${project}.records`, `${id}.json`);
  const record = {id, ...fields, ownerProcess: {pid: process.pid}, writerReleasedAt: null};
  await writeFile(path, JSON.stringify(record));
  // runs body, then stamps completedAt or failedAt
}
```

Deployment batches pass `{schema: 'batch-record/1.0', ...}` in `fields`.

**Diff.**

```diff
--- a/scripts/signin.mjs
+++ b/scripts/signin.mjs
@@ -60,0 +61,15 @@
+export async function startGate({project, operations}, info) {
+  if (await exists(join(operations, `${project}.start-hold`))) refuse('held');
+  const records = join(operations, `${project}.records`);
+  const names = await readdir(records).catch(error => (error.code === 'ENOENT' ? [] : refuse('records-unreadable')));
+  for (const name of names.filter(file => file.endsWith('.json'))) {
+    const record = await readFile(join(records, name), 'utf8').then(JSON.parse).catch(() => refuse('records-unreadable'));
+    // An installed copy can lag a release: a record format it does not know must not read as "no failed deployment".
+    if (record.schema !== 'batch-record/1.0') refuse('records-unreadable');
+    if (record.reconciledFrom === undefined || record.completedAt !== undefined) continue;
+    if (record.replacementContainer === info.Id) refuse('failed-deployment');
+  }
+}
```

## RV06: Producer credential role

**Requirement.** A new producer connects to the production core with a
credential whose role is `music-producer`, bound to its fixed source with no
scopes. The owner grants it in `edge.json` and reloads the running core with
SIGHUP. The grant must keep working across later deployments, which replace the
container.

**Context.** Unchanged `deploy/container/entrypoint.mjs` runs only when a
container starts, after the shared parser:

```js
// Input has already passed the shared credential parser. This profile narrows its grants further.
export function checkPrivateCredentials(credentials) {
  // The coding worker's own role is admitted with no scopes. Every other role, and any robot ID, stays refused here.
  if (credentials.some(credential => (credential.role !== undefined
      && (credential.role !== 'coding-worker' || credential.scopes.length !== 0)) || credential.robotId !== undefined))
    throw new Error('container-config-refused');
}
```

A refusal stops the container before any state effect.

**Diff.**

```diff
--- a/src/credentials.ts
+++ b/src/credentials.ts
@@ -18,4 +18,5 @@ const roleSources: Record<string, string> = {
   'coding-worker': 'parts/coding-worker',
+  'music-producer': 'apps/music-producer',
 };
--- a/docs/music-producer.md
+++ b/docs/music-producer.md
@@ -0,0 +1,4 @@
+## Grant the producer's credential
+
+Add a `music-producer` credential with no scopes to `edge.json`, then send
+SIGHUP to the core. The producer connects once the core reloads.
```
