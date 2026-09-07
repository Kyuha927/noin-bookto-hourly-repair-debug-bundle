# BBK 실제 3D 모델: 로컬 자동 이어가기·완성 실행

**전달 대상: 이미 사용 중인 해당 프로젝트의 로컬 Work/Codex 세션 하나.**

이 링크를 **그 로컬 세션에 한 번만 전달**합니다. 16개 채팅에 다시 나눠 보낼 문서가 아닙니다. 이미 “이어서 해야 할 거 해”라고 보낸 채팅은 그대로 진행합니다. 로컬은 그 결과를 수집하고 실제 Blender 실행·조립·수정·렌더·파일 전달을 맡습니다.

**현재 이 문서의 상태는 실행 지침 게시입니다. 발신 채팅에서 사용자 Mac의 서비스 설치·자동 실행 시작·실제 모델 완성을 확인한 것은 아닙니다.** 아래 지침을 받은 로컬 실행자는 설정만 작성하고 끝내지 말고, 설치 또는 기존 실행기 연결과 실제 첫 작업까지 수행해야 합니다.

This is a complete, public-safe operational handoff, not a verbatim copy of private project files. It publishes no character asset, private source, credentials, local folder identifiers, or private commit inventory. Resolve production inputs through the receiving workspace's existing authenticated project remote. This public transport repository is NOT the working project. Do not run its unrelated maintenance workflows or place private model assets here.

## 1. Execute the user's current request

The user has already started multiple independent modeling chats and told some completed chats to continue. Now they explicitly request local automatic continuation until the real 3D result is finished. Preserve their in-flight work. Do not ask them to restart chats, collect results manually, provide an existing model, repeat a plugin mention, or press “continue” between ordinary authorized stages.

USER_GOAL: a reference-faithful, genuinely editable 3D character with inspected native renders, not more infrastructure reports.

PRIMARY_DELIVERABLE: first, one useful whole-character candidate that can be inspected from front/three-quarter/side and reopened; then the remaining accepted model work, assembled rig/expressions/materials, and verified delivery files. Automating that actual workflow is the assignment. Creating a watcher that never executes a model job is incomplete.

USER_VISIBLE_EVIDENCE: actual character PNGs, editable `.blend`, a real material-change/restore comparison, saved-file reopen proof, and a concise Korean status with concrete defects remaining. A turn sequence is additional evidence, not a substitute for the editable asset.

NON_GOALS: a new 2D editor, a reference image on a plane, another GUI or installer product, generic benchmark spheres presented as a character, unlimited external AI calls, paid services, broadcast/camera/microphone capture, or automatic artistic approval.

The latest request authorizes project-scoped LOCAL continuation and deterministic Blender execution; it removes the obsolete assumption that local work may only install tools. It does NOT waive OS approvals, current model-routing restrictions, protection of originals, cost controls, or final user approval. It does not authorize remote arbitrary-code exposure through the existing bridge.

## 2. Recover the actual current workspace, once

Work in the existing local character project, not this public transport repository. Inspect the current workspace, its remote and worktrees, applicable AGENTS instructions, current model router, project continuity, latest modeling handoff, open jobs and any existing continuation service. Use the existing local memory only for relevant supplemental history after resolving project authority.

Use the real current home/workspace discovered on the host. Do not assume an old `/Users/...` or `/home/...` example is the current machine. Start with the active workspace and its explicit project records; do not recursively scan the user's entire home or cloud backups.

Preserve current `.blend` files, generation scripts, settings, asset hashes and in-flight request IDs. A filename such as `final_portrait.png` is not artistic approval. A PNG without its source does not prove the source can be recovered. When no editable master exists locally, create the character FROM SCRATCH under the project-owned integration area. Do not ask the user to supply one: creation was explicitly requested.

Use the actual designated `00_PRIMARY_USER_REFERENCE.png` through the existing private project/asset route and verify its identity against that route's manifest. The selected reference, not rejected concept sheets or a recolored preview, is the visual target. Preserve the designated reference identity, proportions, hairstyle, costume and accessories; do not redesign them. Inspect actual pixels. Missing source meshes are not a blocker to from-scratch modeling. If the reference itself is inaccessible, keep already authorized unambiguous technical work moving but do not invent character identity or approve a replacement.

## 3. Keep remote chats and local execution separate

Do not send more messages to the 16 chats, terminate them, rewrite their branches, or infer that a chat stopped because it has not published recently. A “continue” request in another chat is not permission for this local process to control that chat.

Discover modeling result branches from the authenticated project remote using the existing `model/bbk-mp1-mNN-` naming family. Read its current modeling handoff for exact output prefixes. Pin a discovered head before reading its files. Record branch/head/result-path, but distinguish a baseline-only branch, a missing report, implemented source, genuine native artifacts, and an accepted master part.

The roles to preserve are:

| Role | Actual work |
|---|---|
| M01 | Face, skull, ears and neck join |
| M02 | Eyes, iris, lashes, brows and eye fitting |
| M03 | Scalp, front hair, fringe and ahoge |
| M04 | Side/back hair, single braid and ribbon |
| M05 | Body, hands, visible limbs and joins |
| M06 | Hood, lining, horns and hood spikes |
| M07 | Jacket, sleeves, pockets, cuffs and seams |
| M08 | Inner garment, shorts, belts and related hardware |
| M09 | Shoes and leg warmers |
| M10 | Tail, small sleeve wings and charm |
| M11 | Topology-bound UV and texture work |
| M12 | Expressions, blink and mouth shapes |
| M13 | Skeleton, skinning and pose checks |
| M14 | Face/eye shading |
| M15 | Hair/cloth/accessory shading |
| M16 | Native inspection, rendering, save/reopen and export |

No all-lane barrier. Keep making the actual M00 character when a lane is missing; put any needed baseline implementation under M00 ownership, not in the absent lane's output directory. Keep that lane's pending result eligible for later comparison. Never fill the missing role with a flat image or label a fitting proxy as accepted geometry.

## 4. Use the installed native Blender, not the bridge's missing feature

Find the already installed official Blender executable from the existing project setup. Inspect its version, architecture and supported arguments. Run it as a project-owned subprocess on new private outputs. The shared bridge lacking a “run builder” tool is NOT a reason to leave local Python builders unexecuted.

Do not reinstall a healthy Blender, patch the shared bridge to expose arbitrary Python, replace its service, grant it new permissions, or change the live shared scene. Use its read-only health/schema only where useful. Current permission state must be observed, never copied from an old report.

For reviewed Blender scripts, construct an argv list, not a shell string. On a verified compatible Blender, use the supported equivalents of:

```text
<observed Blender binary> --background --factory-startup --disable-autoexec --offline-mode --python-exit-code 1 --python <reviewed absolute entry script> -- <its inspected arguments>
```

Inspect the actual script's CLI before invoking it. These flags do not sandbox arbitrary Python or block Python networking: source review, a restricted working area and the existing local execution policy are still required. `--disable-autoexec` protects against implicit file/startup scripts; explicit `--python` is intentional execution. Do not add `--enable-autoexec`, bypass flags or renderer fallback. EEVEE material work must actually run on the supported EEVEE backend.

Use an isolated process rather than an open user scene. Read existing source before calling functions: not all lanes implemented exactly the same builder signature. Preserve `build_component(context)` when actually present. Otherwise write a thin M00 adapter around the inspected entry point, not a second material/model implementation.

## 5. Make the first real pilot happen during setup

After bounded workspace recovery, run useful native work before expanding scheduling infrastructure. Prefer an existing component builder with both inspectable source and a native entry point.

M14 is a known starting candidate: locate its current `materials.py`, `native_probe.py`, source tests and M00 review corrections in the private project. Inspect the newest source and apply only corrections still relevant. Check stale material-slot identity, iris parameter/socket bounds and duplicate-group/version reopen preflight. Do not apply an older full patch over a newer corrected source.

Run its pure checks once for changed source, then its actual native material creation and create-only export. The existing probe exposes reference/output/render and verify operations; read the current CLI, run the genuine native build/render path and reopen in another fresh process. Fix actual API or shader errors without weakening assertions. Its ellipsoid is a METHOD FIXTURE and must not be shown as the finished character.

Immediately continue to actual geometry: select the best available face/eye/hair/hood/body builders; adapt their coordinates and joins to the current master; build them in new component files; assemble into a new master candidate. Keep the full-body draft while refining the face. Deliver the first real character render as soon as it is meaningful, without waiting for shoes, every expression, automated updates or all 16 reports to be perfect. Explicitly list missing or rough parts.

Setup is not ACTIVE_END_TO_END until an actual native job finishes, its output exists and is reopened, and the continuation mechanism demonstrates that it can select the next eligible job without another user “continue”. A text-only canary, heartbeat or mock success cannot satisfy this pilot.

## 6. Install one small continuation mechanism, or reuse the existing one

First check for an existing project-specific runner/scheduler and its lock/state. Extend it in place when compatible; do not create a duplicate owner or restart an active job. Otherwise implement a small project-local Python runner and one user-scoped schedule. This request authorizes a scoped continuation mechanism, not a machine-wide agent platform.

Keep all state, logs, adapters and outputs in a discovered project-owned directory. The only outside write, when actually necessary and locally permitted, is this project's own user scheduler registration. Do not use sudo, create system daemons, change power settings, disable Gatekeeper, turn off permission prompts globally or replace existing login jobs.

The implementation must expose equivalent commands for one cycle, status, pause-after-current-job, resume and uninstall-this-schedule. Those commands must be real and tested, not labels in a README. Prefer the existing scheduler. For a standalone macOS helper use the locally supported user LaunchAgent path; for a bundled application follow its existing Service Management integration. Inspect current host support rather than copying obsolete `launchctl` commands blindly.

Use a five-minute idle intake interval as the default proposed setting, backing off to fifteen minutes when no new work is available. Do not leave a sleeping AI worker burning tokens just to poll. A completed model step should immediately advance to the next eligible step while the active local worker owns the cycle. On reboot or login resume from durable state; do not promise execution while the Mac is powered off, logged out from a user-agent session or asleep. Do not modify those conditions without separate authorization.

## 7. Two loops are required; a file watcher is not an AI worker

Loop A is deterministic: discover new pinned submissions, queue approved source, execute approved native jobs, validate files, reconcile status, and expose results.

Loop B performs review, integration and repairs through the already authorized LOCAL agent route. Resolve its actual model/provider/reasoning profile and keep it unchanged. If local policy permits only a specified worker, use that route exactly. Do not hard-code an old model from this conversation, spawn Codex subagents, open more app threads, buy credits, create API keys or substitute a provider.

Prefer the existing local continuation mechanism with its explicit project/session ID. If the installed and authorized Codex CLI is that mechanism, inspect `codex exec resume --help` and its supported settings, then use the explicit saved SESSION_ID. Never use `--last` or `--all`, which can select an unrelated task. Verify the runtime-reported session and route, not a model's self-description. Do not add `--yolo`, `--dangerously-bypass-approvals-and-sandbox`, `--ignore-rules` or `--ignore-user-config`.

Do not invoke a second turn into a currently active owner. Register a deferred handoff for the existing turn's completion, using the real host/agent idle signal and the project's lock. If that signal or resume API is unavailable, do not guess from a timestamp. Use the authorized alternative already installed for this project, or report AGENT_RESUME_UNAVAILABLE while deterministic admitted jobs continue. A watcher-only installation must say WATCH_ONLY, not “automatic completion enabled”.

For a long-running or rate-limited agent, preserve its explicit session/cursor and next action. Retry only at the observed reset/retry time, with bounded backoff and the same route. Authentication, OS approval, route denial and quota blocks are separate states. Do not fake credentials or advance budgets. These genuine external gates may require user action; the automation must not turn them into DONE.

## 8. Durable jobs, incremental updates and safe ownership

Implement the following transaction in the existing ledger or a small project-local SQLite ledger. Do not create a second canonical memory system.

```text
discover named refs -> pin exact source -> inspect changed code/resources
-> bind review/admission to exact hashes -> run in new private output
-> reopen and inspect actual artifact -> compare with prior candidate
-> integrate only useful changes -> publish private result -> choose next task
```

Persist each job before execution: role, input commit, full source/dependency identity, operation, parameter hash, output directory, owning process/session, attempts, completion evidence and next action. Key deduplication by the exact inputs and operation, not by a branch name or a “done” sentence. Imports and metadata discovery must not execute incoming code.

Use a real single-writer integration lock. A second scheduler tick must return BUSY without touching active work. Failed or timed-out lock checks do not authorize stealing a lock. Native rendering on a shared host defaults to one GPU job; independent lightweight source tests may use up to two slots only with observed spare capacity. The limits include existing jobs, not merely this runner's children.

New branch heads may arrive while rendering. Put them in the inbox, let the current pinned job finish, then inspect and rebase the new delta semantically. Never hot-swap an imported script during rendering, move the master back to an older checkpoint, rewrite another lane's branch, or merge an entire historical app branch just to retrieve one component. Source review is required again when executed bytes or imported dependencies change.

Before adopting geometry, bind UV/shape/weight edits to the actual current topology. Material-only changes must preserve protected geometry and other material roles. Join dimensions in old prompts are fitting seeds, not approved anatomy. Resolve scale/head/neck/eye/hair/hood joins explicitly; do not deform the whole current master merely to fit an incoming component.

Unknown RUNNING outcomes after a crash are RECONCILE_REQUIRED, not automatically retried. Check the original process and durable output first. Retain partial outputs and logs. Confirm any old process is terminal before an idempotent fresh-output retry. Timeout cleanup may signal only the process group created and still owned by this job; no killall, cross-project cleanup or cancellation of web-chat jobs.

## 9. Bounded failure handling without stopping the whole project

Separate native-code failure, source integrity mismatch, missing peer, resource contention, disk pressure, renderer unavailability, permission, authentication, route policy, rate limit and subjective quality defects.

A source or geometry failure should create a concrete local repair task with the actual error and pinned inputs. Have the approved local worker make a narrow correction and rerun affected checks. Do not reset the entire model or add a new delivery framework.

After two identical failures for the same input/operation/error fingerprint, park that fingerprint until inputs, environment or the proposed diagnosis materially change. The local worker must switch to another eligible task, not repeat the failed command or claim the whole project finished. A low-quality render is not a crash: inspect it, identify the largest visible defect, make one coherent correction and rerender under comparable conditions.

Use finite per-job resource limits chosen from the host and measured pilot. Preserve native quality; do not change renderer or silently reduce delivered resolution to get PASS. Disk headroom should include expected outputs plus staging and a reserve. Under storage pressure, pause new heavy allocation without deleting the user's files. Keep last-good artifacts and cap/rotate only this runner's own logs under its declared policy.

## 10. The resumed worker's instruction, stored locally

Store this exact operating intent in the existing project's continuation context; it is not permission to change the global prompt/router:

> Continue the current BBK from-scratch 3D master. First reconcile owned running jobs and read the exact latest checkpoint. Inspect new pinned modeling submissions; never execute unreviewed branch code or reset another lane. Select the highest-impact eligible native build, component integration or visible quality correction. Actually run it in a new private output, inspect the result, save/reopen and update the private ledger. Continue to the next eligible stage during this active session. Do not end at source tests, reports, a fixture, a 2D proxy or another prompt. Preserve the reference identity and existing master. Use only the current approved local model route and actual permissions. If externally blocked, park only the affected task, work on independent tasks, and record the exact unblock condition. Advance the real-character milestone only with the corresponding file and image evidence. Never self-approve final artistic quality. At a real session boundary save the exact next action so the authorized resume mechanism can continue without asking the user to reassemble context.

Bind this instruction to the explicit existing session ID and project path. Do not copy private chat archives or auth files to a public repository. A new turn must read current durable job state before doing anything, rather than blindly repeating the last command.

## 11. Visual priorities and done conditions

Refine the largest visible problems first: reference likeness and head/face contour; eye depth/lid contact and expression; layered hair and braid silhouette; hood thickness and horn attachment; jacket proportions and meaningful cloth construction; then finer textures, footwear, accessories and deformation.

Check both neutral clay and final shading from front and at least one three-quarter and one side view. Do not hide shape errors with beauty lighting. Preserve the full-body deliverable while giving extra attention to the face, hair and hood. Do not interpret a high polygon count, source-test total or render completion as high modeling quality.

Keep three separate milestones:

1. FIRST_VISIBLE_3D: an actual recognizable whole-character candidate, editable source, native front/three-quarter/side renders, one genuine material change/restore and a separately reopened saved file. Visible defects are listed. Technical fixtures alone do not qualify.
2. TECHNICAL_DELIVERY_READY: accepted modeled parts assembled without known blocking intersections, required UV/material setup, tested requested expressions and rig behavior, native file reopening, and any explicitly promised export verified through reimport. Do not claim unsupported renderer/VRM/Warudo equivalence.
3. USER_APPROVED: the user has actually approved the exact candidate's artistic result. Until then report READY_FOR_USER_REVIEW, not FINAL_LOCKED. Continue objective defect repairs within scope, but do not run infinite subjective redesign while waiting for taste approval.

Preserve the original software completion rubric separately. Its prior reported baseline was 37.5%, not a modeling-quality score or a current remeasurement. Read the current private ledger and calculate any change from actual newly passed criteria. Also report model readiness plainly: editable master exists, native renders exist, geometry assembled, expressions tested, save/reopen passed, user review pending. Never fabricate a percent for beauty.

## 12. Deliver privately without making the user hunt

Use the existing private project output/continuity paths. Put the latest meaningful native portrait and full views at stable reviewed pointers, with immutable versioned originals behind them. Supply an editable `.blend`; include a genuine geometry export only when actually produced and reopened. A still image is not that file.

Publish redacted status and artifacts through the already authorized private project route, not this public transport. Preserve the existing GitHub-only delivery preference. Check file sizes and configured LFS/release mechanisms before uploading binaries. A failed upload must not stop local modeling or delete the local result; mark PUBLISH_PENDING and retry safely. Do not commit private source assets or logs to the public bootstrap repository.

Status order: actual native result first, visible improvement/remaining defects, software rubric if relevant, running/next task, then technical evidence. Notify through the already configured local app/project mechanism when a meaningful candidate is ready. Do not enable email, messaging or other accounts for this purpose.

## 13. Required activation canary and recovery checks

Before reporting automatic continuation active, demonstrate all of the following with real local state:

- Existing remote access works and a real published modeling unit is inspected at an exact revision.
- A reviewed local Blender job creates actual native data and a file; a second process reopens that file.
- The runner completes that job and selects/executes a distinct eligible next stage without a fresh user prompt.
- A second tick cannot execute the same owned job concurrently; unchanged input is deduplicated.
- Pause-after-current-job preserves output, then resume continues from the recorded cursor.
- A delayed/new submission is detected and queued, not applied to an in-flight render.
- The actual approved agent-resume route works on the correct idle project/session. A no-op self-report is not enough; verify a bounded intended project change or repair and its artifact.
- Status, scoped scheduler registration and a recent heartbeat are read back on the host. No claim of installation based solely on writing a plist.

Use controlled temporary jobs for the interruption/dedup tests, never interrupt the user's active render. Keep synthetic tests explicitly separate from the real native canary. If one gate fails, report exactly which continuation capability is active and repair the failed gate where authorized. Do not label WATCH_ONLY or NATIVE_QUEUE_ONLY as end-to-end autonomous modeling.

## 14. Required private checkpoint and final local report

Reuse the project's single source-of-truth ledger. At a meaningful boundary record these fields or their existing equivalents:

```json
{
  "setup_state": "NOT_ACTIVATED",
  "collection_state": "NOT_RUN",
  "native_queue_state": "NOT_RUN",
  "agent_resume_state": "NOT_RUN",
  "actual_session_id": null,
  "actual_route_identity": null,
  "scheduler_identity": null,
  "heartbeat_at": null,
  "master_candidate_sha256": null,
  "native_pilot": "NOT_RUN",
  "next_stage_automatic": "NOT_RUN",
  "first_visible_3d": "NOT_RUN",
  "technical_delivery": "NOT_RUN",
  "artistic_approval": "NOT_GRANTED",
  "running_jobs": [],
  "pending_submission_heads": [],
  "blocked_fingerprints": [],
  "next_action": null
}
```

This is a schema example with truthful initial values, not an activation receipt. Fill it from actual observations and keep private identifiers private. A setup-only delivery cannot claim all these fields passed.

When returning from the local setup session, report either ACTIVE_END_TO_END with the real pilot and next-stage proof, or the exact partial mode and the one externally necessary action. Keep other eligible local work moving. Do not return only a plan or “send continue”. Successful setup should already have begun an actual modeling/material operation. The first useful character candidate is the next delivery target, not completion of an installer or a test-count milestone.

## 15. Current primary documentation, not an excuse for more research

Inspect installed help and current project code first. These official references support the execution mechanisms; they do not prove anything is installed on the user's host:

- Blender 4.5 command-line arguments: https://docs.blender.org/manual/en/4.5/advanced/command_line/arguments.html
- Codex non-interactive mode and explicit session resume: https://developers.openai.com/codex/noninteractive/
- Codex CLI argument reference: https://developers.openai.com/codex/cli/reference/
- Apple user agents and launchd: https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html
- Apple app-bundled helper registration: https://developer.apple.com/documentation/servicemanagement/smappservice

Do not install a new tool merely because it is mentioned here. No public CI is authorized to execute private modeling code or invoke an AI model. The public entry only solves instruction delivery; actual processing remains in the existing authorized local project.

**Begin now in the receiving LOCAL session: recover current state, run the first reviewed native unit, wire the actual continuation owner, verify one automatic next step, and continue toward the real 3D deliverable.**
