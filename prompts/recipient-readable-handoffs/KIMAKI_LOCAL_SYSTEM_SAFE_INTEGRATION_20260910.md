# KIMAKI LOCAL-FIRST SYSTEM INTEGRATION, HARDENING, AND ROLLBACK

```text
TASK=KIMAKI_LOCAL_SYSTEM_SAFE_INTEGRATION
REVISION=20260910_R1
EXECUTION_SURFACE=EXISTING_AUTHORIZED_LOCAL_WORK
MODE=IMPLEMENT_VERIFY_AND_HANDOFF
USER_FACING_LANGUAGE=Korean
UPSTREAM_REPOSITORY=https://github.com/remorses/kimaki
PINNED_KIMAKI_VERSION=0.27.0
PINNED_KIMAKI_TAG_COMMIT=75cab301896e76053526b147f58d6a797ab8ecd6
PUBLIC_SAFE_HANDOFF=true
PRODUCTION_PROJECT_DIRECT_MAPPING=false
GATEWAY_MODE=false
AUTO_UPGRADE=false
SUBROUTER=false
```

## 0. Mission

Integrate Kimaki deeply into the user's local system as a private mobile control surface, while preserving the existing local authority hierarchy, model routing, GitHub-canonical state, unified local memory, project gates, and production workspaces.

The finished architecture must be:

```text
User on private Discord
  -> self-hosted Kimaki instance dedicated to one Mac
    -> hardened local intake and session surface
      -> existing Local Work master control plane
        -> existing deterministic tools and verified evidence
        -> existing bounded worker routes
          -> candidate output
        -> independent verification, publication, and final status
  -> verified result returned to the originating Discord thread
```

Kimaki is a transport and session interface. It is not a new master controller, model authority, approval authority, canonical memory, GitHub publisher, production scheduler, or unrestricted shell gateway.

Implement the complete safe path now. Do not merely write a plan. Do not ask routine questions. Continue through reversible steps automatically. Pause only at an unavoidable user-only authentication, Discord authorization, or two-factor step. Never request that the user paste a bot token, password, cookie, OAuth code, or private key into chat, GitHub, logs, or a task artifact.

## 1. Binding authority and precedence

Use this order:

1. The user's latest explicit instruction.
2. The existing authorized Local Work master policy and active local project registry.
3. The current exact model-router decision and project-specific authority files loaded from their verified local source revisions.
4. Verified GitHub canonical state at exact commits.
5. Verified local working-tree evidence.
6. This deployment packet.
7. Kimaki or OpenCode defaults.

If this packet conflicts with a stricter current local policy, keep the stricter policy and report the exact conflict. Do not weaken an existing gate to make Kimaki work.

Before modifying anything, discover the actual authorized configuration checkout, Local Work intake/gate, active project registry, model-router decision, unified local-memory interface, and any current Kimaki/OpenCode installation. Resolve them by verified Git remote, registry record, exact file hash, or existing executable path. Do not infer authority from folder names alone. Do not invent missing paths.

## 2. Non-negotiable boundaries

The following are prohibited:

- Do not use Kimaki gateway mode.
- Do not register a production project root as a Kimaki project.
- Do not let Kimaki write directly into a production checkout.
- Do not replace or modify the user's existing global OpenCode installation, OAuth store, shell profile, model router, Antigravity wrapper, Blender bridge, GitHub credentials, or unified memory database.
- Do not silently change provider, model, account, reasoning level, repository, branch, source asset, approval state, or execution surface.
- Do not enable Subrouter or cross-provider fallback.
- Do not expose OpenCode, Local Work, Blender, a development server, or any local port on a non-loopback interface.
- Do not use Kimaki public tunnels, public session sharing, public diff sharing, or automatic critique upload.
- Do not enable Kimaki automatic worktrees for production.
- Do not let Kimaki merge, rebase, push, force-push, publish, approve, or promote canon.
- Do not create a second project-memory database or copy the full existing local memory into Kimaki `MEMORY.md`.
- Do not commit tokens, cookies, credentials, raw session databases, raw chat history, private file paths, private attachment URLs, or environment dumps.
- Do not delete an existing state directory, project checkout, worktree, database, or process merely because it looks stale.
- Do not kill an OpenCode, Node, Blender, Python, or browser process unless ownership by this Kimaki instance is proven from its runtime manifest, parent-child lineage, executable path, and start time.
- Do not report completion from configuration text alone. Require live canaries.

Any production enrollment attempted before the canary and hardening gates pass must stop with:

```text
BLOCKED_KIMAKI_PRODUCTION_ENROLLMENT_BEFORE_HARDENING
```

## 3. Upstream facts that must shape the deployment

Treat the pinned upstream version as potentially unsafe outside the exact bounded profile in this packet.

Known risk anchors as of 2026-09-10:

- Kimaki 0.27.0 still targets the OpenCode v1 interface while the v2 port remains open: https://github.com/remorses/kimaki/issues/220
- Direct Discord messages beginning with `!` execute shell commands in the mapped project directory without an OpenCode approval turn.
- Kimaki normally allows every external directory unless `--restrict-directories` is used.
- Project-local `.opencode/plugins` and plugin declarations can execute during workspace initialization without a workspace-trust gate: https://github.com/remorses/kimaki/issues/189
- Kimaki-created worktrees still have an open branch-reset, collision, cleanup, and lockfile-mutation report: https://github.com/remorses/kimaki/issues/202
- A running process can remain alive while new Discord ingress stops working, and upstream has no complete active liveness watchdog: https://github.com/remorses/kimaki/issues/206
- Restart can discard pending interactions or interrupt accepted work: https://github.com/remorses/kimaki/issues/200 and https://github.com/remorses/kimaki/issues/218
- Persisted session events can grow without bounded retention: https://github.com/remorses/kimaki/issues/193
- The npm OpenCode wrapper can leave an orphaned native child: https://github.com/remorses/kimaki/issues/144
- Stable Discord thread attribution is not yet exported to every tool subprocess: https://github.com/remorses/kimaki/issues/137

Do not treat an open issue as proof that every installation reproduces the bug. Treat it as a gate requiring a discriminating canary or a compensating control.

## 4. Required target layout

Create a separate tree per Mac. Derive `MACHINE_ID` from a user-approved human-readable alias or a one-way hash of stable local identifiers. Never publish a hardware serial number.

Use this logical layout, adapting only when the existing local policy requires another non-cloud location:

```text
$HOME/Library/Application Support/KimakiLocal/$MACHINE_ID/
  runtime/
    0.27.0-upstream/
    0.27.0-hardened/
    current -> 0.27.0-hardened
  state/
  xdg/
    config/
    data/
    cache/
  control-adapter/
    AGENTS.md
    MEMORY.md
    REQUEST_SCHEMA.json
    inbox/pending/
    inbox/accepted/
    inbox/quarantine/
    outbox/pending/
    outbox/delivered/
    receipts/
  canary-project/
  workspaces/
  backups/
  manifests/
  sentinels/

$HOME/Library/Logs/KimakiLocal/$MACHINE_ID/
```

Requirements:

- Every directory above must be local, non-networked, and outside iCloud Drive, Dropbox, Google Drive, OneDrive, Syncthing, rclone roots, and other automatic sync trees.
- `state`, `xdg`, `backups`, `manifests`, and all credential-bearing files must be owner-only.
- Directories default to mode `0700`; regular secret-bearing files default to `0600`; immutable policy and schema files in the adapter default to `0400` after installation.
- Confirm FileVault status. If FileVault is off, do not claim at-rest protection and report `WARN_FILEVAULT_DISABLED`.
- Do not reuse `~/.kimaki` unless an existing verified deployment already owns it and migration is explicitly justified. Prefer the isolated data directory.
- Do not place production source code in `control-adapter` or `canary-project`.
- Keep a machine-local `OWNERSHIP_MANIFEST.json` listing every path this deployment is allowed to remove during rollback.

## 5. Phase 0: read-only preflight

Run a read-only inventory before installation.

Record, without secret values:

- macOS version and architecture.
- Node, npm, pnpm/Corepack, Git, SQLite, and launchd availability.
- Exact absolute paths and hashes of any existing `kimaki`, `opencode`, `node`, and Local Work executables.
- Existing Kimaki processes, child OpenCode processes, lock ports, launch agents, data directories, and project mappings.
- Free disk space, total disk capacity, and whether the proposed directories are on local APFS storage.
- Whether the active shell environment contains proxy variables, nonstandard certificates, or global XDG overrides that could alter Kimaki behavior. Record only variable names and classifications, never secret values.
- The current exact Local Work authority files, project registry, model-router file, GitHub-canonical memory policy, and unified-memory adapter path.
- Whether a second Mac will run Kimaki. If so, assign a distinct `MACHINE_ID`, bot application, token, state directory, log directory, category, and lock identity.
- Whether any candidate directory contains `.opencode/plugins`, an `opencode.json` plugin declaration, executable MCP declarations, symlinked executable configuration, or unreviewed lifecycle scripts.

Create a sanitized local receipt containing hashes and classifications, not contents of secrets.

Stop before mutation on any of these:

```text
BLOCKED_EXISTING_KIMAKI_INSTANCE_OWNERSHIP_UNKNOWN
BLOCKED_LOCAL_WORK_AUTHORITY_NOT_DISCOVERED
BLOCKED_ACTIVE_ROUTER_NOT_DISCOVERED
BLOCKED_PROPOSED_STATE_PATH_IS_CLOUD_SYNCED
BLOCKED_INSUFFICIENT_DISK_HEADROOM
BLOCKED_CONFLICTING_PORT_OR_LAUNCH_AGENT
```

Use conservative disk headroom. The installation must not proceed when free space is below both 20 GiB and 10 percent of the volume, unless a stricter existing threshold applies.

## 6. Phase 1: reproducible isolated installation

### 6.1 Pin and verify Kimaki

Install only the pinned version `kimaki@0.27.0` for the first accepted deployment.

Before installation:

1. Resolve npm metadata for exactly `kimaki@0.27.0`.
2. Record `version`, `dist.integrity`, tarball URL, tarball SHA-256, package byte count, and observation time.
3. Compare the package version and source metadata with upstream tag commit `75cab301896e76053526b147f58d6a797ab8ecd6`.
4. Inspect package scripts before allowing them to run.
5. Install into a staging directory under `runtime`, never globally.
6. Use absolute executable paths in every wrapper and launch agent.
7. Preserve a read-only upstream package copy for rollback and diffing.

Do not use `kimaki@latest`, an unpinned `npx`, or an automatic updater in the permanent runtime.

### 6.2 Keep OpenCode isolated and on the compatible major line

Kimaki 0.27.0 must not attach to or replace the user's existing OpenCode installation.

- Create an isolated OpenCode v1 runtime inside the Kimaki tree.
- Verify the exact installed OpenCode package, native binary, version, package integrity, executable format, and SHA-256.
- Use a known v1-compatible candidate such as `opencode-ai@1.18.18` only after package integrity and a live compatibility canary are verified.
- Do not install or attach OpenCode v2 for this deployment while upstream issue 220 remains unresolved.
- Set `OPENCODE_PATH` to the verified native binary when available, not merely the npm wrapper.
- If only an npm wrapper is available, prove parent-child cleanup and orphan detection before activation.
- Keep Kimaki/OpenCode OAuth, configuration, data, and cache separate from the user's existing OpenCode state using dedicated `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, and `XDG_CACHE_HOME`.
- Do not import existing OAuth credentials automatically. Reauthentication, if later approved, occurs inside the isolated XDG tree.

Stop on:

```text
BLOCKED_OPENCODE_V1_COMPATIBILITY_NOT_PROVEN
BLOCKED_OPENCODE_NATIVE_PROCESS_OWNERSHIP_NOT_PROVEN
BLOCKED_EXISTING_OPENCODE_STATE_WOULD_BE_MUTATED
```

## 7. Phase 2: mandatory local hardening overlay

Do not expose the pinned upstream build to a production channel unchanged.

Create a minimal, version-bound local overlay. Keep it in a dedicated local Git repository or task-owned branch, with the upstream tag commit as provenance. Do not push secrets or private state. Every patch must have:

- exact upstream preimage hashes;
- exact patched output hashes;
- a narrow patch file;
- focused tests;
- a build receipt;
- a rollback target;
- a refusal path when any upstream preimage differs.

The overlay must implement a local profile controlled by an explicit environment variable such as:

```text
KIMAKI_LOCAL_PROFILE=local-work-transport-v1
```

### 7.1 Disable direct shell escape hatches

Under the local profile:

- A Discord message beginning with `!` must never call `runShellCommand`.
- `/run-shell-command` must be unavailable or return a deterministic blocked response.
- The block must apply in channels and threads, including worktree threads.
- Mention mode must not bypass this block.
- The denial path must not echo secrets or the full attempted command into public logs.

Required canary:

1. Send a command that would create a unique marker file.
2. Verify the bot reports the command blocked.
3. Verify the marker file does not exist anywhere in the control adapter or canary tree.
4. Verify no shell child process was created.

Failure code:

```text
BLOCKED_KIMAKI_DIRECT_SHELL_NOT_DISABLED
```

### 7.2 Disable remote and public surfaces

Under the local profile, block or hide:

- public `/share` session links;
- public `/diff` upload links;
- automatic critique upload;
- `kimaki tunnel` from the managed wrapper;
- `/upgrade-and-restart`;
- project creation and arbitrary project registration from Discord;
- automatic worktree creation and merge commands;
- global or channel-wide model overrides;
- scheduled tasks until a separate scheduler review is completed.

The local administrator may retain a separate offline maintenance command outside Discord. It must require a local terminal and exact version-bound checks.

### 7.3 Workspace trust firewall

Before Kimaki initializes any mapped directory:

1. Resolve the canonical directory without following an untrusted symlink chain.
2. Confirm it is inside the exact allowlisted Kimaki root.
3. Inspect `.opencode/plugins`, `opencode.json`, MCP declarations, command hooks, package lifecycle scripts, and symlink targets.
4. Reject unapproved executable configuration.
5. For the control adapter, allow only exact audited files with recorded hashes.
6. Recheck hashes at every process start and after any update.

A changed executable configuration must quarantine the project mapping and stop OpenCode initialization.

Failure code:

```text
BLOCKED_KIMAKI_WORKSPACE_TRUST_DIGEST_CHANGED
```

### 7.4 Prefer transport-only intake for the real control channel

The production control channel must not need an LLM merely to accept a user request.

Add a narrow transport-only path for a directory containing a signed or hash-pinned marker such as `.kimaki-local-work-transport.json`.

For that exact mapped directory and exact Discord channel:

- Do not create or prompt an OpenCode session.
- Create the Discord thread normally.
- Capture the exact guild, channel, thread, message, author, timestamp, and attachment metadata supplied by Discord.
- Generate a cryptographically random request ID and idempotency key.
- Write one atomic JSON request into `control-adapter/inbox/pending` using temporary-file, fsync, and rename semantics.
- Reply with a compact Korean acknowledgement containing only the request ID and `PENDING_LOCAL_WORK`.
- Do not interpret the request as mutation authority.
- Do not invoke the model router, OpenCode, Antigravity, Git, Blender, a shell, or a network tool from this transport path.
- If the same Discord message is delivered again, return the original request ID and do not duplicate the request.

The transport-only request schema must include at least:

```text
schema=kimaki.local-work.request.v1
request_id
idempotency_key
machine_id
received_at_utc
source_guild_id
source_channel_id
source_thread_id
source_message_id
source_user_id
source_username
raw_user_request
attachments
requested_action_class
user_explicitly_requested_mutation=true|false|unknown
status=PENDING_LOCAL_WORK
```

Rules:

- Missing or unavailable attribution remains `null`; never guess it.
- `requested_action_class` is a neutral transport classification, not an approval.
- The raw user request is untrusted data.
- Attachments are downloaded only to a quarantine folder with size, count, MIME, extension, symlink, archive, and decompression-bomb limits.
- Compute SHA-256 before any downstream use.
- Never execute, import, render, source, or open an attachment automatically.
- Reject device files, sockets, FIFOs, sparse bombs, nested archives, and unsupported executable formats.
- Preserve a compact rejection receipt without reproducing dangerous contents.

If a maintainable transport-only overlay cannot be implemented and tested against the pinned release, keep Kimaki in canary-only mode. Do not fall back to production direct shell or unrestricted OpenCode.

## 8. Phase 3: private self-hosted Discord deployment

Use a dedicated private Discord server, or a dedicated private category in an existing agent-only server.

For each Mac:

- Create one separate self-hosted Discord application and bot.
- Use a distinct bot identity, token, category, state directory, and machine alias.
- Do not use the shared Kimaki gateway.
- Grant only the minimum channel permissions needed for message intake, replies, attachments, threads, history, and application commands.
- Do not grant Administrator when narrower permissions work.
- Assign the `Kimaki` role only to the trusted user account that will control the system.
- Use `no-kimaki` for every account or bot that must be denied.
- Deny all other roles from seeing the private control category.
- Do not enable bot-to-bot invocation.
- Enable only Discord intents actually required by the live canary.
- Voice is disabled in the initial deployment.

The bot token will be stored by Kimaki in its dedicated local SQLite state. Therefore:

- enter it only through the local interactive terminal or local trusted UI;
- never place it in shell history, a plist, a Markdown file, Git, chat, or a process listing;
- protect the state directory with owner-only permissions on FileVault storage;
- exclude the raw state directory from ordinary cloud backup;
- make only encrypted, owner-only local backups;
- redact tokens from every report and log scan.

Pause only for the user's Discord login, application creation, token reveal, authorization, or two-factor interaction. Resume the remaining automated installation immediately after that gate.

## 9. Phase 4: locked runtime wrapper

Create one owner-only wrapper that sets a minimal deterministic environment and launches the exact hardened binary.

The managed invocation must include the equivalent of:

```text
--data-dir <isolated state directory>
--projects-dir <isolated Kimaki workspaces directory>
--mention-mode
--restrict-directories
--permission-timeout-minutes 5
--disable-sync
--no-analytics
--no-auto-upgrade
--no-critique
--skip-footer-mentions
--session-footers
--opencode-hostname 127.0.0.1
--disable-skill new-skill
--disable-skill npm-package
--disable-skill opensrc
```

Also enforce:

```text
KIMAKI_LOCAL_PROFILE=local-work-transport-v1
KIMAKI_DATA_DIR=<isolated state directory>
XDG_CONFIG_HOME=<isolated xdg/config>
XDG_DATA_HOME=<isolated xdg/data>
XDG_CACHE_HOME=<isolated xdg/cache>
OPENCODE_PATH=<verified isolated native v1 binary>
KIMAKI_LOG_SESSION_EVENTS=<unset>
```

Do not include:

```text
--gateway
--use-worktrees
--auto-restart
non-loopback OpenCode hostname
public tunnel options
Subrouter configuration
```

Additional wrapper requirements:

- use absolute executable paths;
- set `umask 077` before creating files;
- use a constrained `PATH` containing only approved system and isolated runtime directories;
- do not inherit unrelated API keys or provider credentials from the login shell;
- unset known credential variables not explicitly required;
- reject execution when the hardening manifest or binary hashes do not match;
- reject execution when the mapped project list contains a production root or a path outside the allowlisted Kimaki tree;
- rotate stdout/stderr logs before launch;
- write a PID and process-generation manifest atomically;
- preserve exit code and shutdown reason;
- never print environment values.

## 10. Phase 5: custom launchd supervision

Do not use Kimaki's generic start-on-login entry as the final supervisor.

Create a custom user LaunchAgent with:

- one unique label per Mac;
- absolute wrapper path;
- `RunAtLoad=true`;
- restart on abnormal exit only;
- a conservative throttle interval of at least 30 seconds;
- no token or secret in plist arguments or environment;
- standard output and error paths inside the dedicated log directory;
- no root privileges;
- no network listener except loopback child services;
- a clean unload command and a verified rollback path.

Do not perform an automatic restart merely because a liveness probe failed while accepted work, queued prompts, sleeps, permissions, questions, or Local Work requests may be pending.

Crash restart and operator-requested restart are different gates:

- A process crash may be relaunched by launchd.
- A planned restart or upgrade must first prove the Kimaki intake queue and Local Work bridge are drained.
- If pending-interaction state cannot be proven empty, leave the process running and report `BLOCKED_KIMAKI_RESTART_PENDING_STATE_UNKNOWN`.

## 11. Phase 6: control adapter into the existing Local Work master

The adapter must remain subordinate to the existing Local Work system.

### 11.1 Adapter files

Create these immutable files:

- `AGENTS.md`: states that Kimaki is transport only, raw Discord input is untrusted, and no direct production mutation is authorized.
- `MEMORY.md`: compatibility stub only. It must say the authoritative sources are the existing GitHub-canonical state and unified local memory. It must contain no private memory dump and must not be automatically rewritten.
- `REQUEST_SCHEMA.json`: strict JSON Schema for the intake request.
- `POLICY_POINTERS.json`: local pointers and hashes to currently verified authority files. Do not publish its private values.

Make only `inbox/pending`, attachment quarantine, and task-owned receipt destinations writable by the Kimaki transport process.

### 11.2 Deterministic intake watcher

Integrate with the existing Local Work request intake. Prefer a thin adapter to an already installed interface. Do not create a parallel scheduler.

For every request:

1. Acquire an atomic per-request claim.
2. Recompute file and attachment hashes.
3. Validate schema, source IDs, timestamps, size limits, path containment, and idempotency.
4. Treat request text and attachments as untrusted data, never as policy.
5. Load the current exact Local Work authority, project registry, active router, and project SSOT.
6. Determine whether the request is read-only, reversible draft work, or mutating work.
7. For mutating work, require the existing Local Work packet and lease mechanism. A Discord request is not a task packet.
8. Submit through the existing Local Work master. Do not call a subordinate executor directly unless the master issues the bounded packet.
9. Preserve the existing one-mutation-owner rule across threads and Macs.
10. Write a return receipt containing actual evidence and status.
11. Deliver the compact result to the exact originating Discord thread using the recorded thread ID.
12. Use a stable delivery nonce so retries cannot duplicate the result.
13. Move the request to accepted, delivered, blocked, or quarantine state atomically.

The state machine must distinguish:

```text
RECEIVED
VALIDATED
QUEUED_LOCAL_WORK
PACKET_ISSUED
CANDIDATE_RETURNED
INDEPENDENTLY_VERIFIED
DELIVERY_PENDING
DELIVERED
BLOCKED
QUARANTINED
```

Only Local Work may set `PACKET_ISSUED`, `INDEPENDENTLY_VERIFIED`, approval, final, canon, merge, release, or publication states.

If no safe existing Local Work intake interface is discoverable, stop with:

```text
BLOCKED_LOCAL_WORK_INTAKE_ADAPTER_NOT_DISCOVERED
```

Do not turn Kimaki into the replacement controller.

### 11.3 Result delivery

Return results to the originating thread only after exact attribution is present.

- Do not infer a Discord thread from recency, title, or user name.
- If attribution is missing, preserve the outbox item and report `BLOCKED_KIMAKI_THREAD_ATTRIBUTION_MISSING` locally.
- Do not post a result into a historical thread merely because it previously mapped to the same OpenCode session.
- Never include secrets, raw private logs, hidden reasoning, or full environment dumps in Discord.
- Large artifacts remain in their approved canonical store. Discord receives a verified pointer and compact receipt.

## 12. Model and subscription routing

The production control channel should use the transport-only path and therefore consume no model tokens for intake.

For any optional Kimaki/OpenCode canary or bounded assistant channel:

1. Load the current exact active model-router decision from its verified local source.
2. Select only a route explicitly allowed for that task class and execution surface.
3. Record exact provider, model ID, variant, authentication class, and observed runtime response.
4. Do not use a model name remembered from chat or hardcoded in this packet.
5. Do not use Subrouter.
6. Do not rotate accounts or cross providers silently.
7. Do not fall back from a subscription route to paid API credits.
8. If the exact route is unavailable, stop with the active router's failure code.
9. Keep Gemini or other specialized execution on its existing authorized local route. Do not reroute it through OpenCode merely because Kimaki supports Google models.
10. Keep final integration and approval with the existing Local Work authority.

OAuth or API login inside Kimaki is optional and disabled until the transport-only round trip passes. When later enabled, use the isolated XDG tree and one explicit provider/model route at a time.

## 13. Production project enrollment, only after all prior gates pass

Never map an original production checkout.

For each approved production task:

1. Local Work resolves the exact repository and base commit.
2. Local Work creates a unique task-owned worktree or isolated copy outside the original checkout.
3. Use an explicit unique branch name with a random or task-ID suffix.
4. Verify the branch does not already exist. Do not use `git worktree add -B`.
5. Record worktree ownership, common Git directory, base commit, lease, allowed write set, and expiry.
6. Run dependency preparation with frozen lockfiles and verify it did not mutate tracked files.
7. Map only the isolated task directory if Kimaki access is actually needed.
8. Disable Kimaki automatic worktree creation and `/merge-worktree`.
9. Kimaki output remains a candidate.
10. Local Work independently inspects files, reruns checks, commits task-owned paths, pushes, and publishes when authorized.
11. Unmap the task directory before cleanup.
12. Remove it only when ownership, clean state, branch preservation, artifact preservation, and lease release are all proven.

Enroll one project at a time. Require a successful project-specific canary before the next project.

## 14. Blender, GUI automation, and local bridges

Kimaki must not connect directly to an active production Blender bridge, production `.blend`, GUI automation service, or unrestricted desktop-control process.

Any Blender or GUI task must flow through Local Work and an exact bounded task packet specifying:

- allowed process and port;
- source file hashes;
- task-owned copy or isolated scene;
- allowed objects and write paths;
- save/reopen evidence;
- screenshots or renders required;
- rollback target;
- user approval boundary.

Keep current production Blender and other long-running creative processes untouched. A canary must use a disposable file and a separate port/process.

## 15. Health, liveness, and orphan control

Create a separate owner-only health checker. It may observe but must not become a scheduler.

Passive checks, at a bounded interval, must verify:

- launchd job state;
- Kimaki parent and worker process lineage;
- exact executable and runtime hashes;
- OpenCode child ownership;
- loopback listeners only;
- Discord gateway connectivity evidence from recent logs;
- SQLite `PRAGMA quick_check` through a safe read-only or quiesced path;
- WAL/SHM growth;
- free disk headroom;
- log freshness and repeated error signatures;
- no unexpected mapped directories;
- no orphaned native OpenCode process owned by this Kimaki generation.

An active end-to-end canary may run only when no active session, queue item, Local Work request, scheduled item, sleep, question, permission, or pending delivery exists. If pending-interaction emptiness cannot be proven, skip the active canary.

Because upstream liveness can wedge while the process remains alive:

- require two consecutive active-canary failures before declaring `DEGRADED_INGRESS`;
- alert through an independent narrow channel, such as a local notification plus an optional dedicated Discord webhook stored in macOS Keychain;
- do not place the webhook URL in files, plist, Git, or logs;
- do not automatically restart when pending state is unknown;
- provide an exact operator recovery command and preserve evidence first.

A restart may occur automatically only when process ownership is proven, the instance is idle, no pending state exists, a state backup succeeded, and the restart generation nonce prevents loops.

## 16. Storage, logs, and retention

Storage protection is mandatory.

Track separately:

- Kimaki SQLite database;
- WAL and SHM files;
- isolated OpenCode database and cache;
- attachments and quarantine;
- task workspaces;
- logs;
- local backups;
- package/runtime copies.

At installation, record a byte baseline. At least daily, record current bytes and delta without uploading private filenames or contents.

Default safety thresholds, unless a stricter local policy exists:

```text
WARN_FREE_SPACE=<20 GiB or <10 percent>
HARD_PAUSE_FREE_SPACE=<10 GiB or <5 percent>
WARN_SINGLE_DAY_GROWTH=>128 MiB
WARN_KIMAKI_DB_PLUS_WAL=>512 MiB
HARD_PAUSE_KIMAKI_DB_PLUS_WAL=>1536 MiB
LOG_ROTATE_AT=20 MiB
LOG_GENERATIONS=5
```

At a hard-pause threshold:

- stop admitting new AI work;
- keep transport acknowledgements and existing safe completion delivery available when possible;
- preserve current work;
- alert the user;
- do not delete data automatically.

Do not perform unsupported direct SQL deletion from `session_events`. Do not claim retention is solved merely by running `VACUUM`. Safe WAL checkpointing or database optimization may run only from a backup-aware, tested maintenance path.

Cleanup rules:

- rotate only manifest-owned logs;
- remove only manifest-owned caches whose producer is stopped and whose recreation is proven;
- quarantine stale workspaces before deletion;
- never auto-delete a worktree, branch, database, or attachment referenced by a pending request, receipt, session, or approval ledger;
- preserve at least one verified rollback snapshot before maintenance;
- keep raw credential-bearing backups local, encrypted, owner-only, and outside cloud sync.

## 17. Updates and rollback

### 17.1 Updates

Automatic upgrade is prohibited.

For every future update:

1. Check upstream releases and open issues without modifying the active runtime.
2. Download the exact candidate package into a new staging directory.
3. Record package integrity and source revision.
4. Reapply the hardening overlay only when all preimage checks pass.
5. Rerun focused unit tests and the full canary matrix.
6. Use a copied non-production state database for migration tests.
7. Verify OpenCode major-version compatibility.
8. Switch the `current` symlink atomically only after acceptance.
9. Keep the previous runtime and a database backup.
10. Roll back immediately on a failed canary.

Do not adopt OpenCode v2 until the relevant Kimaki migration is released and independently verified.

### 17.2 Rollback

The rollback procedure must:

1. stop new intake;
2. preserve pending requests and outbox deliveries;
3. unload the exact LaunchAgent;
4. terminate only the verified Kimaki process generation and its verified children;
5. confirm no owned loopback listener remains;
6. confirm no orphaned native OpenCode child remains;
7. preserve an encrypted state backup and hashes;
8. restore the previous runtime symlink when rolling back an update;
9. remove only paths listed in `OWNERSHIP_MANIFEST.json` when uninstalling;
10. leave existing global OpenCode, Local Work, model router, project repos, GitHub credentials, unified memory, Blender, and unrelated launch agents unchanged;
11. optionally revoke the Discord bot token through the user's authenticated Discord account;
12. write a sanitized rollback receipt.

A rollback test with the disposable canary instance is required before production activation.

## 18. Dual-Mac contract

When deploying on two Macs:

- use one self-hosted bot application per Mac;
- use separate state, XDG, logs, runtime, workspaces, tokens, category, and machine ID;
- never share or sync SQLite databases;
- never share a Kimaki lock port or runtime PID file;
- route a request to one explicit machine or to Local Work for deterministic assignment;
- use the existing global lease or mutation-owner mechanism before either machine mutates shared project state;
- reject simultaneous ownership of the same task, branch, file set, Blender scene, or publication action;
- prove duplicate Discord delivery is idempotent across machines;
- keep one machine's outage from causing the other to assume mutation ownership without a verified lease transfer.

## 19. Mandatory canary matrix

Use a disposable local repository and disposable files. Preserve raw evidence locally and a sanitized receipt.

### Installation and isolation

- exact Kimaki version, npm integrity, upstream commit, binary hash, and OpenCode v1 hash match the manifest;
- no global package, shell profile, existing OpenCode config, or production file changed;
- Kimaki state exists only in the isolated tree;
- all listeners are loopback except the outbound Discord connection;
- analytics, sync, auto-upgrade, critique upload, public share, public diff, and tunnels are disabled;
- only the canary and transport adapter are mapped.

### Security

- `!` command canary is blocked and creates no process or file;
- `/run-shell-command` is blocked;
- an external-directory read attempt is denied or fails closed;
- an unapproved project-local plugin marker does not execute;
- changed plugin/config digest quarantines the mapping;
- `/share`, `/diff`, `/upgrade-and-restart`, project creation, automatic worktree, and merge commands are unavailable in the production profile;
- no token appears in plist, Git, logs, process arguments, receipts, or environment reports;
- an unauthorized Discord user cannot trigger intake.

### Transport and Local Work

- one Discord message creates one thread and one atomic request;
- duplicate delivery returns the original request ID;
- malformed JSON, oversize input, unsupported attachment, path traversal, archive bomb, and symlink attacks are quarantined;
- Local Work validates and accepts a harmless read-only request;
- a harmless reversible mutation request is not executed until the existing packet and lease are issued;
- the result is independently verified and delivered to the exact source thread once;
- missing attribution leaves delivery pending rather than posting to the wrong thread;
- Kimaki never marks the result final or approved.

### Runtime and recovery

- normal login launch works;
- deliberate worker exit is restarted by launchd with bounded backoff;
- planned restart refuses while pending state exists;
- passive health checks detect a stopped process, wrong binary hash, unexpected listener, low disk, database failure, and orphaned owned child;
- active ingress canary detects a controlled wedge without blind restart;
- log rotation preserves recent evidence;
- database backup and quick check pass;
- rollback returns the machine to the exact pre-install state except for preserved receipts and user-approved backups.

### Production enrollment

- Kimaki cannot map a production root;
- Local Work-created unique worktree keeps the original checkout untouched;
- dependency preparation leaves lockfiles clean;
- no Kimaki merge or push occurs;
- Local Work remains the sole verifier and publisher.

Any failed mandatory canary blocks production activation.

## 20. Activation stages

Report each stage independently. Do not collapse them into one PASS.

```text
STAGE_0_READ_ONLY_PREFLIGHT
STAGE_1_ISOLATED_RUNTIME_INSTALLED
STAGE_2_LOCAL_HARDENING_VERIFIED
STAGE_3_DISCORD_SELF_HOSTED_CONNECTED
STAGE_4_TRANSPORT_ONLY_INTAKE_VERIFIED
STAGE_5_LOCAL_WORK_ROUND_TRIP_VERIFIED
STAGE_6_LAUNCHD_AND_HEALTH_VERIFIED
STAGE_7_STORAGE_AND_BACKUP_VERIFIED
STAGE_8_ROLLBACK_VERIFIED
STAGE_9_SECOND_MAC_VERIFIED_OR_NOT_REQUESTED
STAGE_10_FIRST_PRODUCTION_PROJECT_ENROLLED_OR_NOT_REQUESTED
```

Activation status may be:

```text
CANARY_ONLY
READY_FOR_LOCAL_WORK_TRANSPORT
READY_FOR_ONE_PROJECT_PILOT
ACTIVE_BOUNDED_PRODUCTION
BLOCKED_<EXACT_REASON>
```

Do not use `ACTIVE_BOUNDED_PRODUCTION` until every mandatory gate through rollback passes and at least one project-specific pilot is independently accepted.

## 21. Required local artifacts

Create these locally, with no secrets in sanitized versions:

```text
PREFLIGHT_RECEIPT.json
UPSTREAM_PROVENANCE.json
RUNTIME_MANIFEST.json
HARDENING_PATCH_MANIFEST.json
DISCORD_SELF_HOSTED_RECEIPT.json
WORKSPACE_TRUST_MANIFEST.json
TRANSPORT_ADAPTER_MANIFEST.json
LOCAL_WORK_ROUNDTRIP_RECEIPT.json
MODEL_ROUTE_ATTESTATION.json
LAUNCHD_MANIFEST.json
HEALTH_CANARY_RECEIPT.json
STORAGE_BASELINE.json
BACKUP_RESTORE_RECEIPT.json
ROLLBACK_RECEIPT.json
DUAL_MAC_LEASE_CANARY.json          # only when a second Mac is deployed
FINAL_INSTALL_REPORT.md
```

Raw secret-bearing state remains local and encrypted. GitHub may receive only sanitized policy, patch, tests, manifests, hashes, and receipts through the existing authorized publication path after Local Work verification.

## 22. Final report to the user

Write the final user-facing report in Korean and keep it factual. Include:

```text
STATUS
KIMAKI_VERSION_AND_COMMIT
SELF_HOSTED_DISCORD
MACHINE_ID
ISOLATED_RUNTIME
DIRECT_SHELL_BLOCK
PUBLIC_SURFACES_BLOCK
WORKSPACE_TRUST
TRANSPORT_ONLY_INTAKE
LOCAL_WORK_BRIDGE
MODEL_ROUTING
PRODUCTION_PROJECTS_MAPPED
LOOPBACK_NETWORK
LAUNCHD
HEALTH
STORAGE
BACKUP
ROLLBACK
SECOND_MAC
BLOCKER
NEXT_SAFE_ACTION
```

For every item, use `PASS`, `FAIL`, `BLOCKED`, `WARN`, `NOT_RUN`, or `NOT_REQUESTED` and cite the exact local receipt or verified Git commit. Never claim that creating a file, writing a patch, or loading a plist proves live activation.

The ideal finished state is:

```text
Kimaki is a private, self-hosted, per-Mac Discord transport.
Direct shell and public surfaces are disabled.
Only the hardened control adapter and disposable canary are mapped by default.
The user's existing Local Work master remains the sole controller.
Existing model routes remain unchanged.
Existing GitHub-canonical and unified-memory systems remain authoritative.
Production roots, Blender, and global OpenCode remain untouched.
Every change is version-pinned, monitored, backed up, and reversibly owned.
```
