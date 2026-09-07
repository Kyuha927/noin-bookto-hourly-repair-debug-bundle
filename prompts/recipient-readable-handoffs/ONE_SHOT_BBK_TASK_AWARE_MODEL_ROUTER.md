# BBK Local Task-Aware Multi-Model Router Setup

**Recipient:** the existing authorized local Work/Codex session that is already continuing the BBK from-scratch 3D character project.

Run this once in that existing local project session. Do not open a replacement coordinator. Do not stop the current modeling work. Do not restart the already-running remote chats. Apply the routing change at the next safe task boundary, then continue the real Blender/modeling pipeline automatically.

This is a public-safe operational successor. It contains no private asset, credential, local absolute path, API key, chat transcript, or hidden router state. Resolve the actual project root, authenticated project remote, active router files, session IDs, provider access, and exact model slugs on the receiving host.

## 0. Current user authority and objective lock

The user explicitly authorizes a **BBK-project-scoped** routing change:

- Stop treating Gemini 3.7 Flash High as the only permissible model for every BBK worker.
- Use each already authorized local model for the work it performs best.
- Prefer Gemini 3.8 Flash for high-throughput agentic implementation, validation, and mechanical Blender work when its actual local route is available.
- Use GPT-5.6 Sol High for difficult engineering, Blender state recovery, rigging/skinning, and cross-module debugging.
- Use GPT-6 Astra High for M00 coordination, major integration decisions, visual reasoning, and reference-faithful modeling direction.
- Use Astra xhigh only at discrete high-value visual/final-review boundaries, not continuously.
- Allow different subagents or explicit CLI workers to use different models and reasoning efforts.
- Keep current jobs alive and preserve their outputs. A worker already executing may finish on its original route; the new router governs subsequent tasks.
- Keep unrelated projects on their existing routing policies.

This current instruction supersedes the older **Gemini-only BBK implementation restriction** for this project. It does not globally revoke safeguards, the single-writer lease, provider authentication boundaries, quota controls, or user artistic approval.

Lock these fields before mutation:

```text
USER_GOAL = finish the actual editable BBK 3D character with the best practical modeling quality
PRIMARY_DELIVERABLE = task-aware multi-model routing actively used by the existing local continuation runner, followed immediately by continued real Blender work
DEFINITION_OF_DONE = verified route inventory + project-scoped router + actual model/effort receipts + one real routed BBK cycle + rollback proof
USER_VISIBLE_EVIDENCE = actual routed task results, native/model artifacts, route receipts, and continued progress toward the first meaningful 3D candidate
NON_GOALS = replacing Hermes, a second scheduler, a second coordinator, global provider churn, new API keys, paid API provisioning, or a report-only router
ALLOWED_SUPPORTING_WORK = version/access checks, backups, project-scoped profiles, deterministic routing code, focused canaries, and narrow supervisor integration
HARD_BLOCKERS = managed policy that cannot be project-scoped, unavailable authenticated model route, unresolved active-writer ownership, or failed rollback integrity
```

A configuration file alone is not completion. The setup must route and complete at least one real current BBK task, then select the next eligible task without another user “continue”.

## 1. Verified model facts to use, and what they do not prove

The following facts were checked against official primary sources on 2026-09-08:

### Gemini 3.8 Flash

Google lists Gemini 3.8 Flash as generally available and intended for agentic coding, software engineering, long-horizon workflows, advanced reasoning, multimodal understanding, and knowledge work. Its official model information lists a 1M-token input window, 64K output, function calling, search as a tool, computer use, and customizable effort levels. Google also publishes strong vendor-reported long-horizon software-engineering results.

Use those facts as support for assigning it substantial implementation and automation work. Do **not** treat vendor benchmarks as proof it wins every BBK task. Local canaries and actual Blender outcomes remain authoritative.

Official sources:

- https://deepmind.google/models/gemini/flash/
- https://deepmind.google/models/model-cards/gemini-3-8-flash/
- https://deepmind.google/models/gemini/

### GPT-6 Astra

OpenAI describes GPT-6 Astra as its most capable model for hard end-to-end work, complex reasoning, coding, computer use, research, and multistep professional workflows. Official model documentation lists low, medium, high, xhigh, and max reasoning efforts. OpenAI’s model guidance specifically notes that Astra can delegate to subagents when the harness supports it, while advising explicit delegation instructions.

Use Astra High for the root coordinator and high-impact integration/visual judgment. Reserve xhigh for milestone reviews or genuinely unresolved high-impact decisions. Do not run max by default.

Official sources:

- https://developers.openai.com/api/docs/models/gpt-6-astra
- https://developers.openai.com/api/docs/guides/latest-model
- https://help.openai.com/en/articles/20001275

### GPT-5.6 Sol

OpenAI describes GPT-5.6 Sol as a flagship model for complex professional work. Official documentation lists none, low, medium, high, xhigh, and max reasoning efforts. Use Sol High as the engineering specialist between Flash and Astra: difficult code, rig/skin/deformation logic, dependency conflicts, and state recovery.

Official sources:

- https://developers.openai.com/api/docs/models/gpt-5.6-sol
- https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt

### Availability caveat

API documentation and public product pages do not prove the exact local Work, Codex CLI, or Antigravity entitlement. The receiving host must verify its actual authenticated route and exact slug/profile. OpenAI currently states that Astra in Codex requires CLI 0.153.0 or newer, and GPT-5.6 in Codex requires CLI 0.144.0 or newer. Availability can differ between Chat, Work, and Codex.

Do not create an API key, buy credits, switch accounts, or migrate providers to satisfy this setup. Use existing subscription-backed and locally authorized routes only.

## 2. Recover the actual current routing authority without guessing

Begin inside the existing BBK project workspace. Read the applicable local `AGENTS.md`, project SSOT/continuity, active supervisor state, global write lease, continuation-runner state, current Codex configuration, custom agents/profiles, Antigravity wrapper, and the active model-router decision file or successor.

The prior likely architecture is only a discovery hypothesis:

```text
Codex / Work frontend
  -> Hermes orchestration and project memory
  -> Antigravity CLI
  -> Gemini 3.7 Flash High
  -> one repository-writing implementation worker
```

Do not assume it is still current. Resolve the actually loaded router and exact revision. Search only the project and explicit configured control paths, not the user’s entire home directory.

Check, when present:

```text
MODEL_ROUTER_DECISION_V5.json
newer MODEL_ROUTER_DECISION_* successors
Hermes supervisor/router state
Antigravity/Gemini launch wrapper and observed model profile
$CODEX_HOME/config.toml
$CODEX_HOME/*.config.toml
$CODEX_HOME/agents/*.toml
<PROJECT>/.codex/config.toml
<PROJECT>/.codex/agents/*.toml
existing continuation runner, queue, lock, ledger, and scheduler identity
```

Before changing any authority or launcher file:

1. Reconcile the current owned job and global write lease.
2. If a writer is active, let it finish or reach its documented safe boundary. Do not kill, cancel, or inject a second writer.
3. Save a timestamped byte-for-byte backup and SHA-256 manifest of every file to be changed.
4. Record this instruction as the BBK-scoped authority for the task-aware successor.
5. Preserve the old Gemini-only route as a tested rollback target.

If active authority files conflict, do not choose by filename or timestamp alone. Resolve what the current supervisor actually loads. Use `BLOCKED_ROUTER_AUTHORITY_CONFLICT` only after safe read-only discovery is exhausted; continue independent deterministic/model work that does not require the conflicting write path.

## 3. Verify the actual model inventory and execution surfaces

Use the currently authenticated ChatGPT/Codex account and the existing Gemini/Antigravity route. Do not create or request API keys, purchase credits, rotate accounts, copy cookies, or alter providers globally.

Inspect actual installed CLI help before writing configuration:

```text
codex --version
codex --help
codex exec --help
codex resume --help
agy --help or the actual existing Antigravity wrapper help
```

If Codex is below an officially required minimum, use only the existing approved update mechanism with backup and rollback and only when local policy already permits it. No `curl | sh`, sudo, global package-manager migration, or unreviewed installer. Otherwise keep the route blocked and continue with models that are actually available.

Verify bounded read-only or isolated canaries for these semantic routes:

```text
OPENAI_ASTRA_HIGH
OPENAI_ASTRA_XHIGH
OPENAI_GPT56_SOL_HIGH
GEMINI_38_FLASH_LOW
GEMINI_38_FLASH_MEDIUM
GEMINI_38_FLASH_HIGH
```

Resolve exact local slugs rather than guessing them. The Gemini wrapper may encode model and effort in a profile name. Record the actual command/profile identity without exposing credentials.

For every route capture:

```text
provider
actual model ID or external profile slug
requested and observed reasoning effort
CLI/app/wrapper version
surface: Work, Codex CLI, or Antigravity CLI
exit status
runtime route evidence
quota/rate-limit state when exposed
subscription-backed versus API-key-backed route
```

Reject API-key-backed routes unless they were already explicitly authorized for this project. A model’s prose self-description is not route evidence. A failed canary must not silently substitute another model.

## 4. Preserve the existing control plane

Keep these invariants:

- Codex/Work remains the user-facing coordinator.
- Hermes remains the orchestrator, durable queue, memory/checkpoint, retry, and handoff owner.
- The existing continuation runner remains the only automation owner; extend it rather than adding another watcher or scheduler.
- Antigravity remains the execution route for authorized Gemini calls.
- Exactly one repository/master integration writer may hold the global write lease.
- Parallel read-only exploration, visual review, or isolated worktree implementation may use distinct model workers, but they cannot independently merge or mutate the master.
- One heavy Blender/GPU job per shared host unless current host evidence proves a stricter safe limit.
- Default maximum two CPU-heavy test/build jobs, counting existing work.
- No background AI polling merely to consume tokens. Deterministic intake may poll with backoff; model work begins on queued events or explicit continuation.

Do not replace Hermes, create another memory store, create another master branch, enable competing auto-merge, alter the installed Blender, widen sandbox permissions, or use approval-bypass flags.

Native Codex `spawn_agent` remains disabled if the active managed policy forbids it. Different-model “subagents” may instead be separate explicit CLI worker processes managed by the existing durable queue. This still satisfies the task-aware worker design without bypassing the local policy.

## 5. Deterministic-first task classification

Do not waste any model on work that a deterministic tool can perform exactly. Add these task classes to the existing router or its project-scoped successor:

```text
DETERMINISTIC_EXACT
GEMINI_ROUTINE_LOW
GEMINI_ENGINEERING_MEDIUM
GEMINI_ENGINEERING_HIGH
SOL_COMPLEX_ENGINEERING
ASTRA_COORDINATION_HIGH
ASTRA_VISUAL_HIGH
ASTRA_FINAL_XHIGH
```

Routing must be based on structured task metadata, not a vague free-form request. A task record should include at least:

```json
{
  "task_id": "...",
  "lane": "M00-M16 or shared",
  "operation": "...",
  "needs_visual_judgment": false,
  "needs_complex_state_reasoning": false,
  "needs_repo_write": false,
  "needs_blender_gpu": false,
  "input_revision": "...",
  "write_set": [],
  "estimated_context": "small|medium|large",
  "failure_history": []
}
```

The selector must return and persist:

```json
{
  "task_class": "...",
  "requested_route": "...",
  "actual_route": "...",
  "requested_effort": "...",
  "actual_effort": "...",
  "selection_reason": "...",
  "fallback_reason": null,
  "write_lease_required": false,
  "review_route": "..."
}
```

### No-model work

Use `DETERMINISTIC_EXACT` for:

- `git fetch`, branch/ref discovery, exact SHA comparison, changed-path lists;
- checksums, manifests, file existence/size, JSON schema validation;
- launching already reviewed tests and recording exit codes;
- Blender subprocess execution from already reviewed source;
- artifact decode/reopen checks that are deterministic;
- queue, lock, deduplication, heartbeat, and receipt bookkeeping.

A model may interpret a failure only after the deterministic command produces evidence.

## 6. Install this task-aware route matrix

Use actual observed local slugs and profile syntax. The table defines semantic roles, not permission to invent a model route.

| Semantic role | Primary model / effort | Intended work |
|---|---|---|
| `bbk_root` | GPT-6 Astra High | M00 coordination, cross-lane integration, next-task selection, conflict resolution, end-to-end follow-through |
| `bbk_visual` | GPT-6 Astra High | face/eye/hair/hood likeness, silhouette, render comparison, major artistic defect diagnosis |
| `bbk_final` | GPT-6 Astra xhigh | one milestone/final candidate review after native renders and reopen evidence; never grants user approval |
| `bbk_complex_engineer` | GPT-5.6 Sol High | hard Blender bugs, dependency conflicts, rig/skin/expression logic, state recovery, multi-module repairs |
| `bbk_flash_high` | Gemini 3.8 Flash High | `bpy` implementation, UV, modifiers/constraints, rig/shader scaffolding, long repetitive coding, bounded component iteration |
| `bbk_flash_medium` | Gemini 3.8 Flash Medium | validation, test repair, file-structure checks, routine debugging, result normalization, documentation implementation |
| `bbk_flash_low` | Gemini 3.8 Flash Low | branch/log/result triage, summaries, simple classifications after deterministic evidence |
| `bbk_exact` | no model | hashes, tests, Git operations, process execution, queue/lock/receipt mechanics |

### Why this differs from the older router

Gemini remains the main throughput worker rather than being removed. The verified 3.8 Flash release is suited to agentic coding and long workflows, so use it for much of the implementation load. Astra is preserved for work where logs cannot determine correctness: identity, silhouette, visual coherence, complex orchestration, and final comparison. Sol is the engineering bridge for genuinely hard code/state problems.

Expected long-run share among **model calls**, not a quota target:

```text
Gemini 3.8 Flash: roughly 50-60%
GPT-5.6 Sol: roughly 15-25%
GPT-6 Astra: roughly 20-30%
```

Do not force these percentages. Exact deterministic work should reduce all model usage. A task’s evidence and complexity decide its route.

## 7. Effort selection and escalation rules

### Gemini 3.8 Flash

- **Low:** branch/result/log interpretation, lightweight classification, concise summaries.
- **Medium:** validation, test diagnosis, file-structure work, ordinary repairs, manifest/provenance work.
- **High:** `bpy`, UV, modifiers, constraints, rig structures, shader-node code, long automatic implementation, or large code context.

Do not send final face likeness or whole-character aesthetic approval to Flash alone.

### GPT-5.6 Sol

Default to **High** for complex engineering. Use it when one or more of these apply:

- cross-module state or ownership is difficult;
- Blender execution fails after a plausible Flash repair;
- rig/skin/deformation logic requires deep structural reasoning;
- persistence, process recovery, or revision reconciliation is involved;
- a shared-file semantic merge has nontrivial regression risk.

Do not use Sol merely because a routine test failed once.

### GPT-6 Astra

- **High:** M00 root work, complex integration, reference-based visual diagnosis, facial/hair/hood direction, deciding between competing component candidates.
- **xhigh:** a discrete milestone review, unresolved high-impact visual defect, or final integrated candidate. One review task at a time.
- **max:** disabled by default. It requires a recorded current need and explicit project authorization beyond this setup.

### Escalation ladder

```text
exact deterministic operation
  -> Gemini 3.8 Low/Medium/High according to complexity
  -> GPT-5.6 Sol High for verified complex engineering
  -> GPT-6 Astra High for cross-system or visual/integration judgment
  -> GPT-6 Astra xhigh for one high-value review boundary
```

Escalation is not “retry with a bigger model until something says PASS.” Preserve the exact failure, change the hypothesis, and run the appropriate route. After two identical failures with no new evidence, park the fingerprint and continue another eligible task.

## 8. Explicit fallback policy

Fallback must be recorded, never silent.

```text
Gemini 3.8 Flash unavailable:
  -> existing verified Gemini 3.7 Flash High route for Gemini-assigned work
  -> mark DEGRADED_GEMINI_37
  -> continue checking 3.8 only at a later explicit maintenance boundary, not every task

GPT-5.6 Sol unavailable:
  -> Astra High for complex engineering when quota and route are available
  -> mark FALLBACK_ASTRA_FROM_SOL
  -> otherwise park only the affected complex task

Astra unavailable:
  -> Sol High may continue engineering and provisional integration
  -> visual/final acceptance remains PROVISIONAL_VISUAL_REVIEW
  -> do not let Sol or Gemini self-grant final artistic acceptance

All model routes unavailable:
  -> deterministic queue and Blender/test execution may continue
  -> agent-required tasks become BLOCKED_MODEL_ROUTE
```

Never rotate accounts, use an unapproved provider, lower Blender/render quality, or consume paid API billing as an invisible fallback.

## 9. Map M00-M16 to the appropriate routes

A lane may use more than one route, but each concrete step has one owner and one receipt.

| Work | Implementation route | Review / decision route |
|---|---|---|
| M00 master integration and prioritization | Astra High | Astra xhigh only at meaningful milestone |
| M01 face/head | Gemini 3.8 High for builders; Sol High for topology/deformation bugs | Astra High, xhigh only for milestone likeness review |
| M02 eyes/lids/lashes | Gemini 3.8 High for assets/material code; Sol High for fitting/deformation bugs | Astra High |
| M03/M04 hair and braid | Gemini 3.8 High for geometry builders and iteration | Astra High for silhouette/flow |
| M05 body/hands | Gemini 3.8 High for base builder; Sol High for joint/deformation complexity | Astra High at whole-body silhouette checkpoints |
| M06 hood/horns | Gemini 3.8 High for construction; Sol High for intersections/attachments | Astra High |
| M07 jacket | Gemini 3.8 High for pattern/mesh/tooling; Sol High for deformation/fit failures | Astra High for silhouette and fold hierarchy |
| M08 inner/shorts, M09 footwear, M10 tail/accessories | Gemini 3.8 High | Astra High only when the component materially affects silhouette; Sol High for structural bugs |
| M11 UV/textures | Gemini 3.8 High | Sol High on topology-bound conflicts; Astra High for visible seam/color decisions |
| M12 expressions | Sol High for shape/deformation design and tooling | Astra High for identity/expression quality |
| M13 rig/skin | Sol High primary; Gemini 3.8 High for diagnostics and repetitive weight tooling | Astra High only for visible deformation quality |
| M14 face/eye shading | Gemini 3.8 High for node/build code; Sol High for Blender API/shader bugs | Astra High/xhigh under matched native conditions |
| M15 hair/cloth shading | Gemini 3.8 High for material implementation | Astra High for coherent look; Sol High for technical shader conflicts |
| M16 delivery/reopen/export | deterministic tools + Gemini 3.8 Medium | Astra High for actual visible result; Sol High for failed native pipeline |
| branch/result discovery, SHA/log/status | deterministic first, Gemini 3.8 Low only for interpretation | M00 spot-check on anomalies |
| repeated tests/validation/file inspection | deterministic first, Gemini 3.8 Medium | Sol High only for unresolved complex failure |
| final integrated `.blend` visual QA | deterministic native render | Astra xhigh once, then user review |

Do not use a model ratio to override this mapping. Do not let the same worker implement and independently approve a high-impact visual result.

## 10. Configure per-role CLI workers or subagents safely

Use the official configuration mechanism supported by the observed local versions. Merge with current files rather than overwriting them. Exact TOML/JSON keys must come from installed help/schema, not this document.

Preferred execution order:

1. **If the current harness supports per-agent model/effort profiles under policy:** create project-scoped roles for Astra High, Astra xhigh, Sol High, Gemini Flash Low/Medium/High, and deterministic exact work.
2. **If native Codex subagents are prohibited or cannot mix external Gemini profiles:** keep `spawn_agent` disabled and have Hermes launch separate explicit CLI worker processes with exact role/profile, durable task ID, and bounded output.
3. **If only the root Work session can use Astra:** keep M00 in that existing Astra High session and route subwork through the existing CLI workers; return evidence to M00 for integration.

Do not use `--last` or `--all` for continuation. Bind explicit session IDs. Do not use `--yolo`, approval bypasses, ignore-rules flags, or provider credentials in project config.

Create logical project-scoped profiles equivalent to:

```text
bbk-astra-high
bbk-astra-xhigh
bbk-sol-high
bbk-gemini38-low
bbk-gemini38-medium
bbk-gemini38-high
```

Actual filenames and fields follow the observed local runner. Do not change default profiles for unrelated projects.

Every worker invocation must include:

```text
project identity
task ID and lane
exact input revision
read/write scope
requested role/model/effort
actual route evidence
expected artifact
bounded timeout/output
review route
```

## 11. Concurrency and write ownership

The target is parallel thinking and isolated production, not concurrent corruption.

Initial safe ceiling, reduced when the actual host/account requires it:

```text
max_llm_workers = 3
max_shared_repo_writers = 1
max_master_integrators = 1
max_blender_gpu_jobs = 1
max_cpu_heavy_jobs = 2
max_astra_xhigh_jobs = 1
```

A practical initial mix is:

```text
1 Astra High M00 coordinator
1 Gemini 3.8 implementation/validation worker
1 Sol High complex-engineering worker when an eligible task exists
```

A second Gemini read-only/isolated worker may replace the idle Sol slot for routine backlog. Do not keep expensive workers alive without an eligible task. All write-capable workers must use isolated worktrees and the existing global write lease. Only M00 integrates the master.

A current in-flight Gemini 3.7 task is not canceled merely because 3.8 becomes available. Finish and review it, then route new tasks through 3.8.

## 12. Implement the project-scoped router

Extend the existing Hermes continuation path. Do not add a second scheduler or memory system.

Required behavior:

1. Deterministically classify each queued task.
2. Select the semantic route and exact observed profile.
3. Persist the routing receipt before launch.
4. Acquire the existing write lease only for a declared write set.
5. Launch the bounded worker in an isolated context.
6. Validate actual outputs and route identity.
7. Send the result to M00 for acceptance or rejection.
8. Release the lease and select the next eligible task.
9. Preserve failures and blocked routes without stopping unrelated work.

The router must not infer model success from a worker’s prose. Require actual command metadata, output files, Git changes, native artifacts, or test evidence appropriate to the task.

Project-scoped output should include equivalents of:

```text
router policy/config
role/profile definitions
route-selector implementation
route-selector tests
migration receipt
model-inventory receipt
canary receipts
rollback script or exact reversible procedure
updated continuation state
```

Do not edit unrelated global projects. If the current system has only a global router, add a BBK project predicate that preserves the existing default route elsewhere.

## 13. Rollout without stopping current work

Perform this transaction:

```text
observe current active job and router
-> back up exact router/profile/runner files
-> build project-scoped successor in an isolated copy
-> run deterministic route-selector tests
-> run read-only route canaries
-> wait for current writer safe boundary
-> activate BBK-scoped successor atomically
-> run one real current BBK task
-> verify its actual route/artifact
-> automatically select a distinct next eligible task
-> verify rollback to the old router in a controlled config test
-> keep the new router active if all gates pass
```

Do not pause the whole project while waiting for every model route. Missing one route blocks only its specialized tasks; explicit fallbacks handle the rest.

## 14. Required canaries

Do not declare the router active until these are demonstrated with actual local evidence:

1. **Current-work preservation:** the in-flight task was not killed, reset, or duplicated.
2. **Deterministic route:** a Git/hash/test/queue task completes without an LLM call.
3. **Gemini low/medium route:** branch/log/test evidence is interpreted with the observed Gemini 3.8 profile, or explicitly degraded to verified 3.7.
4. **Gemini high route:** one isolated real BBK implementation or repair task produces a concrete reviewed change.
5. **Sol route:** one genuinely complex engineering task is handled by GPT-5.6 Sol High, or the receipt records why no eligible Sol task existed. Do not manufacture a bug merely to exercise the model.
6. **Astra High route:** M00 reviews and integrates/rejects a real current result using actual evidence.
7. **Astra xhigh route:** run only when a meaningful native visual milestone exists. If none exists yet, keep this canary pending rather than wasting quota on fixtures.
8. **Single-writer:** a competing write attempt returns BUSY without mutating the master.
9. **No silent fallback:** intentionally unavailable test route records the requested/actual route and reason.
10. **Automatic next stage:** after the real task completes, the runner selects a distinct eligible next task without a new user message.
11. **Rollback:** the previous router can be restored from verified backup and then the new route reactivated, without touching model assets or task history.

A text-only no-op is not a real task canary. A synthetic route test is useful but does not replace the concrete BBK cycle.

## 15. Quality and cost policy

The user’s proposed allocation is broadly sound and should be used as a routing hypothesis:

- Gemini 3.8 Flash can handle most branch/result intake, validation, routine `bpy`, UV, modifier/constraint work, rig/shader scaffolding, and long repetitive automation.
- GPT-5.6 Sol High is retained for hard engineering rather than routine bookkeeping.
- Astra High/xhigh is protected for visual identity, facial/eye/hair/hood quality, cross-system integration, and final candidate review.

Apply these corrections:

- Exact hashes, tests, Git operations, and process management should usually use **no model**, not even Flash.
- Gemini 3.8 Flash’s published benchmark wins are vendor-reported; actual local Blender outcomes decide escalation.
- “Astra xhigh once at the end” is a good default, but a discrete earlier xhigh review is justified when a face/identity decision would otherwise contaminate many downstream parts.
- Do not hard-code a workload percentage or burn remaining quota to meet a ratio.

Track usage where the local clients expose it. Do not buy credits, invoke API billing, or downgrade native render/modeling quality. Prefer the smallest adequate reasoning effort, but never sacrifice the primary visible result for a cheaper PASS.

## 16. Completion states

Use these exact meanings:

```text
DISCOVERED_ONLY
  Router/model files inspected; nothing activated.

CONFIGURED_NOT_ACTIVE
  Project-scoped config exists and static tests pass; no real task routed.

ACTIVE_TASK_AWARE_ROUTER
  Current work preserved, actual model routes verified, one real BBK task completed through the router, and a distinct next task selected automatically.

ACTIVE_DEGRADED_GEMINI37
  Same as active, but Gemini 3.8 is unavailable and the verified 3.7 route is explicitly used for Gemini-assigned work.

PARTIAL_ROUTE_BLOCKED
  Some specialized routes are unavailable; independent tasks continue under explicit fallback.

ROLLBACK_REQUIRED
  Route identity, write ownership, output integrity, or rollback verification failed. Restore the prior router and preserve task outputs.
```

Do not report active based only on writing config/profile files.

## 17. Required final local receipt

Record at least:

```json
{
  "project": "BBK",
  "status": "CONFIGURED_NOT_ACTIVE",
  "previous_router": {
    "path": null,
    "sha256": null,
    "loaded_revision": null
  },
  "new_router": {
    "path": null,
    "sha256": null,
    "project_scoped": true
  },
  "current_job_preserved": null,
  "model_inventory": [],
  "role_profiles": [],
  "canaries": [],
  "actual_real_task": null,
  "actual_next_task": null,
  "single_writer_verified": false,
  "rollback_verified": false,
  "unrelated_projects_changed": false,
  "api_keys_or_paid_routes_added": false,
  "continuation_runner_reused": false,
  "next_action": null
}
```

Fill it from observed facts. Include requested and actual route, effort, execution surface, input revision, output identity, and evidence for every routed task. Keep secrets and private paths out of public reports.

## 18. Continue the real project after activation

Do not end after router setup. Resume the current BBK continuation queue immediately.

Prioritize:

1. actual editable whole-character candidate;
2. native front/three-quarter/side renders;
3. face, eye, hair, and hood quality;
4. component integration and intersection repairs;
5. material change/restore and saved-file reopen;
6. rig, expressions, UV/material completion;
7. final Astra xhigh review and user-ready delivery.

The first meaningful 3D result remains more important than a larger router report. Tests, receipts, and routing infrastructure support that result; they do not replace it.

**Begin now in the existing local session: preserve the current worker, inventory actual routes, install the BBK-scoped task-aware router, verify a real routed task, and continue the native modeling pipeline.**
