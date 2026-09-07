# BBK Local Task-Aware Multi-Model Router Setup

**Recipient:** the existing authorized local Work/Codex session that is already continuing the BBK from-scratch 3D character project.

Run this once in that existing local project session. Do not open a replacement coordinator, do not stop the current modeling work, and do not restart the already-running remote chats. This instruction changes the BBK project's model-routing policy from a likely Gemini-only implementation route to a verified task-aware hybrid route while preserving the existing control plane, single-writer lease, current session, model assets, and in-flight jobs.

This is a public-safe operational successor. It contains no private asset, credential, local absolute path, API key, chat transcript, or hidden router state. Resolve the actual project root, authenticated private remote, active router files, session IDs, and provider access on the receiving host.

## 0. User authorization and hard objective lock

The user explicitly authorizes this BBK-scoped routing change:

- Stop treating Gemini 3.7 Flash High as the only model allowed for every BBK worker.
- Keep Gemini available where it is genuinely the best throughput choice.
- Use GPT-6 Astra and other actually available Codex models for the tasks they fit better.
- Allow different subagents or explicit CLI workers to use different models and reasoning levels.
- Keep the existing local continuation and modeling work running; apply routing changes at a safe task boundary rather than interrupting an owned active job.
- Do not change routing for unrelated projects.

Lock these fields before mutation:

```text
USER_GOAL = finish the actual editable BBK 3D character with the best practical modeling quality
PRIMARY_DELIVERABLE = task-aware model routing actively used by the existing local continuation runner, followed by continued real Blender work
DEFINITION_OF_DONE = verified route files + actual model/effort receipts + one real routed implementation/verification cycle + rollback path
USER_VISIBLE_EVIDENCE = route matrix, actual runtime identities, canary outputs, and continued native/model artifact progress
NON_GOALS = replacing Hermes, a second scheduler, a second coordinator, global provider churn, new API keys, paid API provisioning, or a report-only router
ALLOWED_SUPPORTING_WORK = version/access checks, backups, project-scoped Codex agent profiles, deterministic routing code, focused canaries, narrow supervisor integration
HARD_BLOCKERS = managed policy that cannot be project-scoped, unavailable authenticated model route, unresolved active-writer ownership, or failed rollback integrity
```

A configuration file alone is not completion. The setup must route at least one real current BBK task and preserve the current modeling process.

## 1. Recover the actual current routing authority without guessing

Begin inside the existing BBK project workspace. Read the applicable local `AGENTS.md`, project SSOT/continuity, active supervisor state, global write lease, current continuation-runner state, current Codex configuration, custom agents, profiles, and the active model-router decision file or successor.

The prior likely architecture is only a discovery hypothesis:

```text
Codex / Work frontend
  -> Hermes orchestration and project memory
  -> Antigravity CLI
  -> Gemini 3.7 Flash High
  -> one repository-writing implementation worker
```

Do not assume this is still current. Find and record the exact active files, loaded revision, route evidence, writer lease, current local session, and any newer policy. Search only the project and the explicit configured control paths, not the user's entire home directory.

Check, when present:

```text
MODEL_ROUTER_DECISION_V5.json
newer MODEL_ROUTER_DECISION_* successors
Hermes supervisor/router state
Antigravity/Gemini launch wrapper and observed model slug
$CODEX_HOME/config.toml
$CODEX_HOME/*.config.toml
$CODEX_HOME/agents/*.toml
<PROJECT>/.codex/config.toml
<PROJECT>/.codex/agents/*.toml
existing continuation runner, queue, lock, ledger, and scheduler identity
```

Before changing any authority or launcher file:

1. Reconcile the current owned job and global write lease.
2. Wait for a safe boundary if a writer is active; do not kill, cancel, or inject a second writer.
3. Save a timestamped byte-for-byte backup and SHA-256 manifest of every file to be changed.
4. Record this user instruction as the BBK-scoped authority that supersedes the old Gemini-only restriction for this project only.
5. Preserve the old router as a tested rollback target.

If two active authority files conflict, do not choose by filename or timestamp alone. Resolve the actually loaded supervisor/router and produce `BLOCKED_ROUTER_AUTHORITY_CONFLICT` only after completing safe read-only discovery.

## 2. Verify actual model access and CLI capability

Use the currently authenticated ChatGPT/Codex account and the existing Gemini/Antigravity account route. Do not create or request API keys, purchase credits, rotate accounts, copy cookies, or change providers globally.

Inspect the actual installed CLI and help before writing config:

```text
codex --version
codex --help
codex exec --help
codex resume --help
```

GPT-6 Astra requires Codex CLI 0.153.0 or newer. If the installed version is older, use only the existing approved official update mechanism with backup and rollback, and only if the active local policy permits it. Do not use `curl | sh`, sudo, a global package-manager migration, or an unreviewed installer. If an update is not authorized, record `ASTRA_BLOCKED_CLI_VERSION` and continue configuring the routes that are actually available.

Verify model availability with bounded read-only canaries, using the syntax supported by the observed CLI. The intended model IDs are:

```text
gpt-6-astra
gpt-5.6
gpt-5.6-terra
gpt-5.6-luna
```

Verify the existing Antigravity Gemini slug/profile from the local wrapper rather than assuming its spelling. The expected semantic route is Gemini 3.7 Flash High, but the runtime-reported exact slug and account/profile are authoritative.

For each candidate route, capture:

```text
provider
actual model ID or observed external slug
reasoning effort
CLI/app version
account/auth source without secrets
surface (Work, Codex CLI, Antigravity CLI)
exit status
runtime-reported route evidence
quota/rate-limit state when exposed
```

A model's prose self-description is not route evidence. Use runtime status, command metadata, or the existing verified route receipt. A failed model-access canary must not silently substitute another model.

## 3. Preserve the existing control plane

Keep these architectural invariants:

- Codex/Work remains the user-facing coordinator.
- Hermes remains the orchestrator, durable queue, memory/checkpoint and handoff owner.
- The current continuation runner remains the only automation owner; extend it rather than adding a second watcher or scheduler.
- The existing Antigravity Gemini route remains available for explicitly assigned work.
- Exactly one repository/model integration writer may hold the global write lease.
- Parallel read-only exploration, review, and test analysis may use multiple agent threads, but they cannot independently merge or mutate the master.
- One heavy Blender/GPU job per shared host unless the current host controller proves a stricter or safer limit.
- No background AI polling merely to burn tokens. Deterministic intake may poll with backoff; agent work starts on queued events or explicit continuation.

Do not replace Hermes, create another memory store, start another master branch, enable competing auto-merge, change the user's installed Blender, widen sandbox permissions, or use `--yolo` / `--dangerously-bypass-approvals-and-sandbox`.

## 4. Install the BBK task-aware route matrix

Create a project-scoped successor router, using the existing router's schema and active location where possible. Prefer a name equivalent to `BBK_MODEL_ROUTER_V1.json` or a properly versioned successor of the current router. Preserve the old Gemini-only router for rollback.

The router must classify explicit task metadata, not guess from a vague free-form prompt. At minimum support:

```text
COORDINATION_INTEGRATION
VISUAL_MODELING_JUDGMENT
BLENDER_COMPLEX_DEBUG
IMPLEMENTATION_CODE
READ_HEAVY_EXPLORATION
DETERMINISTIC_VERIFICATION
BULK_ISOLATED_DRAFT
FINAL_ACCEPTANCE_REVIEW
```

Apply this primary matrix only after the route is actually observed as available:

| Route role | Primary model / effort | Permissions | Intended work |
|---|---|---|---|
| `bbk_coordinator` | `gpt-6-astra`, `high` | existing coordinator permissions; single-writer admission only | M00 planning, cross-lane integration, conflict resolution, next-task choice, end-to-end follow-through |
| `bbk_visual_director` | `gpt-6-astra`, `xhigh` | read-only by default | face/eye/hair/hood likeness, silhouette, render comparison, major artistic defect diagnosis, milestone acceptance recommendation |
| `bbk_blender_architect` | `gpt-6-astra`, `high` | read-only or leased writer for a narrowly declared patch | hard Blender API failures, geometry/shader interactions, multi-part integration, native execution diagnosis |
| `bbk_implementer` | `gpt-5.6`, `high` | the sole leased implementation writer | Blender Python builders, rig/skin/expression code, shader/material code, focused repairs and integration tests |
| `bbk_explorer` | `gpt-5.6-terra`, `medium` | read-only | branch/result discovery, codebase exploration, official-source research, large-file review, dependency mapping |
| `bbk_verifier` | `gpt-5.6-luna`, `medium` | read-only | hashes, manifests, deterministic log parsing, test triage, result normalization, deduplication and receipt checks |
| `bbk_gemini_batch` | observed Gemini 3.7 Flash High route | isolated worktree; no master merge or final approval | high-volume repetitive scaffolding, bounded component variants, mechanical refactors, fixture generation, parallel drafts |
| `bbk_final_reviewer` | `gpt-6-astra`, `xhigh` | read-only | final candidate review after native renders/reopen evidence; never self-grants user artistic approval |

Do not run `xhigh` continuously. Use it at discrete high-value visual or final review boundaries. The coordinator and hard integration default to Astra High. Routine scans and receipts must not consume Astra unless the cheaper route fails on a materially complex case.

### Explicit fallback rules

Fallback is allowed only when recorded and only after actual route unavailability, not as a silent optimization:

```text
bbk_coordinator:
  gpt-6-astra high
  -> gpt-5.6 high with ASTRA_UNAVAILABLE marker
  -> BLOCKED_COORDINATOR_MODEL if neither is available

bbk_visual_director / bbk_final_reviewer:
  gpt-6-astra xhigh
  -> gpt-6-astra high
  -> gpt-5.6 high marked PROVISIONAL_VISUAL_REVIEW
  Final artistic/model-quality acceptance remains pending until the designated high-end review route or the user reviews it.

bbk_implementer:
  gpt-5.6 high
  -> gpt-6-astra medium/high
  -> observed Gemini 3.7 Flash High for isolated implementation only, followed by Astra/gpt-5.6 review before integration

bbk_explorer:
  gpt-5.6-terra medium
  -> observed Gemini 3.7 Flash High
  -> gpt-5.6-luna medium

bbk_verifier:
  gpt-5.6-luna medium
  -> gpt-5.6-terra low/medium
  -> observed Gemini 3.7 Flash High
```

Never rotate accounts, switch to an unapproved provider, lower the delivered Blender/render quality, or hide the fallback. Store `requested_route`, `actual_route`, `fallback_reason`, and `review_required` in every task receipt.

## 5. Map the current BBK work to routes

Use these defaults for the existing M00–M16 modeling program. A lane may use multiple roles, but one model owns each concrete task step.

| Work | Primary execution | Required review |
|---|---|---|
| M00 master integration and prioritization | `bbk_coordinator` | `bbk_final_reviewer` at meaningful visual milestones |
| M01 face/head, M02 eyes, M03/M04 hair, M06 hood | `bbk_blender_architect` or `bbk_implementer` depending on whether the step is visual/structural or code-heavy | `bbk_visual_director` |
| M05 body/hands, M07 jacket, M08 inner/shorts, M09 footwear, M10 tail/accessories | `bbk_implementer`; `bbk_gemini_batch` may produce isolated repetitive drafts/fixtures | `bbk_visual_director` before adoption |
| M11 UV/textures | `bbk_implementer` | `bbk_blender_architect`; visual result checked by `bbk_visual_director` |
| M12 expressions | `bbk_blender_architect` for deformation design, `bbk_implementer` for code/shape-key tooling | `bbk_visual_director` |
| M13 rig/skin | `bbk_implementer` | `bbk_blender_architect` |
| M14 face/eye shading, M15 hair/cloth shading | `bbk_blender_architect` for material behavior, `bbk_implementer` for node/build code | `bbk_visual_director` under matched native conditions |
| M16 native delivery, save/reopen/export | `bbk_implementer` | `bbk_coordinator` plus `bbk_verifier` |
| Branch discovery, result intake, documentation research | `bbk_explorer` | coordinator spot-check |
| Test logs, hashes, manifests, receipt normalization | `bbk_verifier` | coordinator only on exceptions |
| Final whole-character before/after and readiness judgment | `bbk_final_reviewer` | user approval remains separate |

Gemini is no longer the universal worker. It is a high-throughput specialist. It must not be the sole judge for face likeness, final model quality, integration conflicts, or release readiness.

## 6. Configure Codex custom agents and CLI profiles safely

Use the official Codex configuration mechanism supported by the observed version. Project-scoped Codex configuration loads only for a trusted project. Merge with existing files rather than overwriting them.

The project `.codex/config.toml` should be equivalent to the following, adjusted only for the actual supported schema and current limits:

```toml
model = "gpt-6-astra"
model_reasoning_effort = "high"

[agents]
enabled = true
max_concurrent_threads_per_session = 4
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
```

`4` is a ceiling for open read-heavy agent threads, not four writers and not four Blender renders. Reduce it when the observed account, client, host, or managed policy requires a lower number. Keep write admission at one.

Create project-scoped custom agent files under `.codex/agents/` using the actual current format. Each file must define `name`, `description`, and `developer_instructions`; set `model` and `model_reasoning_effort` explicitly for the roles above. Configure `sandbox_mode = "read-only"` for explorer, verifier, visual director, and final reviewer. The implementer may receive workspace-write only after Hermes grants the existing global lease and declares its exact write set.

Do not place provider credentials, base URLs, authentication keys, or unrelated machine settings in project-scoped config. Codex project config cannot override machine-local provider/auth keys. If the current base config is tied to the Gemini external provider, keep that route in its existing Antigravity wrapper and use the authenticated OpenAI Codex route through named user-level profiles or explicit CLI model selection, without replacing the user's base profile.

Create named user-level profile files only when needed and permitted, for example equivalent to:

```text
bbk-astra-high
bbk-astra-xhigh
bbk-gpt56-high
bbk-terra-medium
bbk-luna-medium
```

Do not change the default profile for unrelated projects. The continuation runner must select the profile explicitly by role.

When native Codex subagents are permitted after this user-scoped override, use custom agents. If a managed configuration still prevents subagents, do not bypass it: use separate explicit `codex exec` jobs with exact `--model`/`--profile` and reasoning config, the same durable queue, and the same one-writer lease. Record `EXECUTION_MODE=CODEX_SUBAGENT` or `EXECUTION_MODE=EXPLICIT_CLI_WORKER`.

## 7. Add a deterministic router to the existing Hermes continuation path

Extend the existing continuation runner and Hermes task graph. Do not create a second scheduler.

Add a small deterministic route selector, using the project's existing language and conventions, that accepts a structured task record such as:

```json
{
  "task_id": "...",
  "task_class": "IMPLEMENTATION_CODE",
  "lane": "M14",
  "needs_visual_judgment": false,
  "needs_repo_write": true,
  "needs_blender_gpu": false,
  "input_revision": "...",
  "write_set": ["..."],
  "expected_context": "medium"
}
```

The selector must return:

```json
{
  "role": "bbk_implementer",
  "requested_model": "gpt-5.6",
  "requested_effort": "high",
  "provider_route": "codex_chatgpt",
  "permissions": "workspace-write-after-lease",
  "review_role": "bbk_blender_architect",
  "fallbacks": [],
  "decision_rule": "explicit rule ID"
}
```

Reject ambiguous write tasks instead of allowing a free-form model choice. Read-only tasks can be conservatively routed to explorer/verifier. A change in the active router revision must invalidate cached route decisions for unstarted tasks.

Every execution receipt must include:

```text
router revision/hash
rule ID
task class/lane
requested and actual model
reasoning effort
provider/profile
execution mode
sandbox/permission mode
writer lease ID when applicable
input commit and source hashes
output hashes
fallback reason
reviewer and review result
usage data if exposed
```

The actual runtime route must be checked again at launch. A router JSON saying `gpt-6-astra` is not proof that Astra ran.

## 8. Keep one writer while using multiple models

Different models may work in parallel only when their effects are isolated:

- Explorer/verifier/visual-review roles remain read-only and can run concurrently within the observed thread limit.
- Gemini batch work uses a disposable worktree/output and cannot write the master, router, shared ledger, or another lane.
- Only `bbk_implementer`, `bbk_blender_architect`, or M00 may receive the single writer lease for one declared write set.
- A read-only model can return a patch proposal. The leased writer rechecks current hashes and applies it semantically.
- Do not let multiple agents write different files in the same Blender master concurrently merely because their paths differ.
- One heavy native Blender/GPU job at a time. CPU-only source checks may use at most the observed safe capacity.

If an agent finishes late, compare its pinned input against the current master. Rebase the idea, not the whole old file. A newer timestamp does not automatically win.

## 9. Run route canaries before promotion

Do not activate the successor router globally for the BBK runner until these canaries pass with actual runtime evidence:

1. **Astra coordinator canary:** `bbk_coordinator` reads the current checkpoint, identifies the highest-impact eligible task, and returns a structured plan without writing.
2. **Terra explorer canary:** `bbk_explorer` scans the authenticated project for current modeling result heads and returns pinned candidates without mutation.
3. **Luna verifier canary:** `bbk_verifier` validates one real manifest/hash/test receipt and catches a deliberately malformed fixture.
4. **GPT-5.6 implementer canary:** under a temporary worktree and the single lease, `bbk_implementer` performs one small real current-project repair or integration, runs affected tests, and produces a reviewable commit or patch.
5. **Gemini specialist canary:** the existing Antigravity route executes one bounded isolated batch/scaffolding task and records the exact Gemini route. It does not merge or self-approve.
6. **Astra visual-review canary:** `bbk_visual_director` reviews an actual current native render or modeling result, identifies concrete visible defects, and does not confuse a method fixture or 2D image with the final character.
7. **Single-writer canary:** a second write request is denied or queued while the first lease is active; no file is touched by the denied worker.
8. **Rollback canary:** restore the old routing state in a disposable copy and prove the previous Gemini-only path still resolves without changing the live project.

Use the cheapest route for malformed-fixture and deterministic tests. Do not use a fake model label or a prose claim as a canary.

If Astra or another route is unavailable, activate only the verified subset and mark exact routes blocked. Do not call the setup fully task-aware when every task still goes to Gemini.

## 10. Promote at a safe boundary and continue real work

After the canaries pass:

1. Commit the successor router, custom-agent files, selector, focused tests, backup manifest, rollback tool, and updated continuation configuration on the existing authorized local project branch/worktree.
2. Read back the exact files and hashes.
3. Atomically update the existing active-router pointer or supervisor configuration at a safe idle boundary.
4. Restart only the specific continuation component if its documented reload mechanism requires it and no owned job is active. Never reboot the machine or restart Blender/other services as a shortcut.
5. Run a status cycle and confirm the loaded router hash.
6. Resume the existing BBK local-finish queue from its current cursor.
7. Route the next highest-impact actual modeling task, not another configuration audit.

The first post-activation task should advance visible 3D quality or native integration, preferably current face/eyes/hair/hood or an actual Blender builder that already has reviewed source. It must create or improve a real editable component/master and produce native evidence where the environment allows it.

Do not stop at `ROUTER_INSTALLED`. Continue until the active turn/session reaches a real boundary, then checkpoint the exact next task and route.

## 11. Required tests

Add focused tests for:

- every task class mapping to the expected role/model/effort;
- the 16 modeling lanes mapping to the intended primary/reviewer pair;
- unknown or malformed tasks failing closed;
- no silent fallback;
- Astra unavailable behavior;
- Gemini route retained but no longer universal;
- xhigh limited to visual/final boundaries;
- one-writer lease enforcement across different models;
- read-only roles unable to mutate;
- route cache invalidated by router revision changes;
- late result requiring semantic rebase;
- actual CLI/profile invocation matching the receipt;
- rollback restoring the previous loaded router;
- unrelated project configuration remaining byte-identical.

Do not count repeated tests or model self-reports as new product progress. Keep route tests separate from native Blender/model-quality evidence.

## 12. Activation states and truthful reporting

Use these states exactly or map them to equivalent existing states:

```text
DISCOVERED_GEMINI_ONLY
ROUTER_CANDIDATE_BUILT
CANARIES_PARTIAL
ACTIVE_TASK_AWARE_ROUTING
ACTIVE_WITH_BLOCKED_ROUTES
ROLLBACK_VERIFIED
BLOCKED_ROUTER_AUTHORITY_CONFLICT
BLOCKED_MANAGED_MODEL_POLICY
BLOCKED_WRITER_OWNERSHIP
```

`ACTIVE_TASK_AWARE_ROUTING` requires:

- Astra coordinator route actually observed;
- at least two different subagent/CLI model routes actually observed;
- Gemini route observed and constrained to its specialist role;
- one real implementation task completed through the selected route;
- one real review completed by a different appropriate route;
- single-writer behavior verified;
- active router hash read back;
- rollback verified.

A config edit, `codex --version`, or successful no-op prompt alone cannot satisfy it.

Return a concise Korean report in this order:

1. actual active route matrix and loaded router revision;
2. actual task completed after activation and its visible/native output;
3. exact model/effort/provider receipts for each canary;
4. blocked/unavailable routes and explicit fallbacks;
5. unchanged controls: Hermes, one writer, existing scheduler/session, models/assets, unrelated projects;
6. exact next real modeling task already queued or running.

Do not claim that local autonomous continuation is active unless the existing continuation runner has loaded this router and executed the real post-activation task.

## 13. Official current references

Use installed help as the source of truth for the actual client. These current official references establish the intended supported mechanisms:

- GPT-6 Astra model and supported reasoning efforts: https://developers.openai.com/api/docs/models/gpt-6-astra
- ChatGPT Work/Codex Astra availability and Codex CLI 0.153.0 minimum: https://help.openai.com/en/articles/20001275/
- Codex configuration reference, project config, profiles, and `[agents]` settings: https://developers.openai.com/codex/config-reference
- Codex subagents and custom per-agent model/reasoning files: https://developers.openai.com/codex/multi-agent
- Codex CLI model/profile/config flags: https://developers.openai.com/codex/cli/reference

The docs confirm capability, not local availability. Verify the receiving account and loaded configuration.

**Begin now in the existing local BBK session: reconcile the current writer, audit the actual Gemini-only restriction, build and test the BBK-scoped successor router, promote it only after real canaries, then continue the actual 3D modeling queue with the task-appropriate model.**