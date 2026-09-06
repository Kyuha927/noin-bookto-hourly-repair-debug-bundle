# Local Work one-shot: Muse Code + Muse Spark 1.3 Contributor XHigh performance-first setup

Date: 2026-09-07 (Asia/Seoul)
Target: the user's current macOS local Work/Codex environment
Primary goal: make `Muse Spark 1.3 Contributor` usable through the native Muse Code harness at `xhigh` reasoning with the most stable supported route, while preserving the user's existing Codex, Pi, OpenCode, Gemini routing, repositories, and credentials.

## User objective

The user wants a production-usable **Muse Code lane** for `Muse Spark 1.3 Contributor` at its highest generally exposed Contributor reasoning level, `xhigh`.

Performance and stability are the priorities. Contributor quota/cost is not the limiting factor. Do not lower reasoning to save tokens. Do not substitute Spark 1.2, Standard 1.3, another provider, or another model unless the user explicitly requests it later.

This is a real setup-and-verification task. Inspect the actual installed Muse Code and current provider capabilities, make the smallest maintainable supported configuration, run bounded real canaries, and leave a concise operational result.

## Current public facts to verify against the live installation

Treat these as starting evidence, not immutable truth:

- Current OpenCode Go catalog exposes model ID `muse-spark-1.3-contributor` through a Responses endpoint and advertises reasoning variants `minimal`, `low`, `medium`, `high`, `xhigh`; no Contributor `max` variant is currently exposed.
- Contributor is the same Spark 1.3 checkpoint/capability class under a different data-use/pricing contract, not a deliberately smaller model. Inputs and outputs sent through Contributor may be used to improve/train future Meta models and the tier is not ZDR.
- Muse Code is Meta's first-party agentic coding harness for Muse Spark and supports explicit model/reasoning selection in current CLI builds, but exact provider/model/config syntax must be discovered from the installed version rather than guessed.
- Some third-party integrations have recently misrouted Spark 1.3 Contributor to legacy `/chat/completions`; the working OpenCode Go route is Responses. Never introduce that regression.

Reference URLs for verification if network access is available:
- https://opencode.ai/docs/go/
- https://ai.meta.com/llama/
- https://github.com/meta-models/meta-model-cookbook
- https://github.com/meta-models/muse-code-sdk

Do not rely on unofficial examples when current CLI help or first-party docs contradict them.

## Non-negotiable constraints

1. Preserve the existing Codex Desktop/CLI, Pi/Astra setup, OpenCode, Gemini worker routing, model-router policy, repositories, project configuration, shell startup behavior, and active sessions.
2. Muse Code must remain a separate lane. Do not globally replace Codex, Pi, or OpenCode commands/configuration.
3. Target model is exactly `muse-spark-1.3-contributor` with `xhigh` reasoning when the live provider supports it.
4. Never silently fall back to Spark 1.2, Standard Spark 1.3, Medium/High reasoning, another model, another provider, or a compatibility endpoint. Fail visibly instead.
5. Prefer the **native Muse Code + Meta-supported provider path** when it can directly access Contributor. This gives the first-party harness the best chance to preserve Muse-specific agent behavior.
6. If native Muse Code cannot directly address Contributor in the installed release/account, inspect whether Muse Code officially supports a custom/provider base URL compatible with the current Responses transport. Use it only if supported by current Muse documentation/help. Do not monkeypatch the binary, intercept TLS, scrape credentials, or depend on an undocumented hack merely to force the model.
7. Do not copy OAuth tokens/API keys between Pi, OpenCode, Codex, browsers, or Muse Code. Use each product's supported authentication mechanism.
8. Never print, log, commit, upload, or expose API keys, OAuth tokens, cookies, auth JSON, refresh tokens, secret environment variables, or browser storage.
9. Contributor data-use terms are intentional for this lane. Still exclude secret-bearing files and unrelated private material from canaries. Do not silently send `.env`, SSH keys, cloud credentials, signing keys, browser data, chat archives, or unrelated personal data.
10. Preserve all existing sandbox, approvals, filesystem, network, destructive-action, privacy, storage, GitHub-authority, and project-specific safety rules.
11. Do not install a new daemon, proxy, provider gateway, credential forwarder, or background service unless Muse Code's supported architecture strictly requires it and the existing policy authorizes it.
12. No broad filesystem scans, no destructive cleanup, no mass package upgrades, and no unrelated refactoring.
13. Do not claim completion from config text alone. A real Muse Code canary must prove the requested model route and an actual coding/tool loop.

## Phase 1 — Inspect the actual Muse Code installation

Perform minimal read-only inspection first.

Resolve and record:

- macOS version and architecture;
- the exact `muse` executable on PATH;
- Muse Code version/build and install source;
- all relevant Muse Code config locations discovered from current help/docs;
- whether duplicate Muse installations or stale wrappers exist;
- current provider/auth status without displaying credential values;
- current default model and reasoning effort;
- available model list/catalog from the live provider;
- supported `muse exec` / TUI flags for provider, model, reasoning effort, JSON/event output, workspace, sandbox, context/compaction, and model selection;
- whether the current build exposes `muse-spark-1.3-contributor` directly;
- whether `xhigh` is accepted for that exact model;
- whether the current provider uses a Responses-style transport for Spark 1.3 Contributor;
- whether Muse Code's own subagents inherit the requested model/effort or silently use a different default.

Use `muse --help`, relevant subcommand help, live model listing, first-party docs, and sanitized runtime event metadata. A model saying its own name in prose is not route proof.

Do not dump full environment variables or auth files.

## Phase 2 — Normalize Muse Code only if necessary

If Muse Code is absent, install the latest stable official Muse Code release using Meta's current official installation path appropriate for macOS.

If it is already installed:

- keep the current install when it supports Spark 1.3 Contributor + XHigh correctly;
- upgrade only if required for the target capability or to fix a known routing defect;
- use the official supported update mechanism;
- preserve existing settings and make a timestamped backup only of files that will actually be edited;
- do not remove other coding harnesses or rewrite shell startup files unnecessarily.

After normalization, verify that `codex`, `pi`, `opencode`, and `muse` still resolve to their intended binaries.

## Phase 3 — Choose the provider route by evidence

### Route A — preferred: native Meta provider

If the installed Muse Code can directly authenticate to Meta Model API and exposes `muse-spark-1.3-contributor`, use this route.

Use the user's already authorized Muse/Meta credential if one exists and is valid. If interactive authentication is required, invoke only Muse Code's supported user-visible login/auth flow. Never ask the user to paste secrets into chat and never reveal stored credentials.

Confirm through live provider/model metadata that Contributor is actually selected.

### Route B — supported custom Responses provider, only if necessary

If Route A cannot expose Contributor but Muse Code's **current documented interface** supports a custom provider/base URL/model catalog that can target a Responses-compatible endpoint, configure an isolated provider profile for the user's already authorized Contributor service.

Requirements:

- target must resolve to `muse-spark-1.3-contributor`;
- transport must be Responses-compatible if that is what the provider advertises;
- do not route it through legacy `/chat/completions`;
- keep auth isolated to Muse Code's supported credential store/env mechanism;
- do not reuse a GPT/OpenAI provider block if it changes semantics;
- do not create an HTTP translation proxy merely to make incompatible APIs look compatible.

If the user's Contributor entitlement is currently via OpenCode Go, inspect the live official model catalog and supported auth interface. Do not assume that an OpenCode Go API credential is valid for native Meta Model API or vice versa.

### Route C — unsupported in current Muse Code

If neither A nor B is officially supported by the installed/current Muse Code, do not force it. Leave the working Pi/OpenCode Contributor lane untouched and report exactly what Muse Code capability is missing, along with the smallest future activation step once upstream support appears.

Do not falsely report success by invoking Pi/OpenCode from a wrapper named `muse`.

## Phase 4 — Configure a dedicated Contributor XHigh profile

Create the smallest maintainable Muse Code configuration/profile/launcher supported by the current release.

Desired operational identity:

- human-readable profile/alias: `muse13-contrib-xhigh` (or closest native equivalent);
- model: `muse-spark-1.3-contributor`;
- reasoning effort: `xhigh`;
- provider: the verified Route A or Route B provider;
- no model fallback;
- no reasoning downgrade;
- preserve Muse Code's native agent orchestration, tools, skills, context handling, sandbox, and approval behavior.

Do **not** invent configuration keys. Derive exact syntax from the live Muse Code version.

If Muse Code uses global settings rather than named profiles, prefer a tiny explicit launcher or documented invocation that selects Contributor XHigh without changing unrelated defaults. If the user already primarily uses Muse Code and the current config safely supports it, setting Contributor XHigh as Muse Code's default is acceptable only after proving it works and without affecting other harnesses.

Keep a one-command explicit invocation available even if a default is set.

## Phase 5 — Verify XHigh is real, including subagents

This is performance-first. A label is not enough.

Run a tiny deterministic request and inspect sanitized Muse Code JSON/event/runtime metadata when available.

Prove as much as the provider exposes:

- configured model ID is `muse-spark-1.3-contributor`;
- effective requested reasoning effort is `xhigh`;
- provider route is the intended provider;
- request succeeds without fallback;
- no 1.2/default-model substitution;
- no legacy Chat Completions misroute;
- no truncation during reasoning;
- normal tool calls work.

If the provider does not attest effective reasoning effort, label it `CONFIGURED_XHIGH_NOT_PROVIDER_ATTESTED`; do not claim stronger proof.

Muse Code is multi-agent. Determine whether spawned internal subagents inherit the root model and XHigh effort. If current Muse Code provides separate subagent/model settings, configure all performance-critical Muse agents to the same Contributor 1.3 XHigh lane unless first-party documentation explicitly requires a different fixed role model. Do not silently allow 1.2 or lower-effort workers.

If a built-in agent is intentionally provider-managed and cannot be overridden, record the limitation rather than patching internal code.

## Phase 6 — Performance-first harness settings

Preserve Muse Code's first-party strengths instead of turning it into a thin generic client.

Keep enabled when supported and already safe:

- native multi-agent orchestration;
- native planning/goal tracking;
- built-in coding skills;
- provider-native tool calling;
- context/state management;
- native compaction;
- sandbox and staged approvals;
- test execution and Git diff inspection.

Do not aggressively shorten the system prompt or disable built-in orchestration just to save tokens. The user prioritizes success rate over Contributor token cost.

Avoid unnecessary third-party MCP/tool catalogs during initial validation. Add existing essential MCPs only after the clean core lane passes, one at a time. A recursive/oversized schema or failing MCP must not make the base Contributor lane unusable.

Do not impose a tiny output cap. XHigh reasoning can fail if the output/reasoning ceiling is too low. Use Muse Code's normal supported limits and verify that no request ends because reasoning hit a hard cap.

Preserve decisive errors, failed tests, exact numerical values, changed-file evidence, and unresolved risks in final reports.

## Phase 7 — Contributor privacy boundary

Contributor intentionally trades data-use rights for lower price. Make this visible in the local operational documentation/profile description without spamming every turn.

Before live canaries:

- use a temporary synthetic workspace, not a private production repository;
- verify deny/exclude behavior for obvious secret-bearing paths if Muse Code provides it;
- never include credentials in prompts or fixtures;
- do not upload unrelated private files.

For later real projects, Contributor may be used only where the user accepts Meta's Contributor data-use terms for that material. Do not silently route sensitive/non-approved repositories through Contributor merely because it is the default Muse profile.

## Phase 8 — Real canary suite

Use a temporary non-destructive workspace.

### Canary A — provider/model/effort identity

Run a tiny deterministic task with the explicit Contributor XHigh invocation.

Pass requires:

- successful response;
- verified/sanitized runtime evidence of the requested model route;
- XHigh configured and not rejected;
- no fallback/retry into another model/provider;
- no `/chat/completions` routing error.

### Canary B — coding/tool loop

Create a small synthetic repository containing one real bug and deterministic tests.

Ask Muse Code Contributor XHigh to:

1. inspect the repository;
2. diagnose the bug;
3. edit the implementation;
4. run tests;
5. inspect the diff;
6. report exact pass/fail evidence.

Success requires the actual test command to exit successfully and the diff to implement the intended fix.

### Canary C — multi-agent inheritance

Run one bounded task that naturally invokes Muse Code's native multi-agent behavior if current Muse Code supports/uses it.

Inspect sanitized events/metadata to determine whether worker/subagent model/effort matches Contributor 1.3 XHigh or is provider-managed. Do not manufacture expensive parallel work merely to inflate proof.

### Canary D — session continuity and compaction sanity

Run a small multi-turn coding session with tool use and earlier-turn state. Confirm there is no obvious loss of task state, duplicate history explosion, invalid tool-call continuation, or provider protocol failure.

Do not force a giant context solely to trigger compaction. Use diagnostics/current behavior where possible.

### Canary E — coexistence

After setup, verify that existing `codex`, `pi`, `opencode`, and their primary configs/default models remain unchanged and functional.

Do not spend OpenAI allowance on a full benchmark as part of this setup unless necessary to verify coexistence.

## Phase 9 — Stability handling

For transient 429/5xx/network failures:

- use Muse Code/provider-native bounded retry behavior;
- do not retry indefinitely;
- preserve the exact terminal error after the bounded retry budget;
- do not trigger fallback to a different model;
- distinguish rate-limit exhaustion from model/protocol/configuration defects.

For a 400/404/500 that suggests wrong endpoint/model format:

- inspect current provider model metadata and Muse Code request route;
- specifically check whether a Responses-only model was misrouted to `/chat/completions`;
- correct only supported configuration;
- never solve it by disabling safety or credential checks.

For model-not-found or unsupported effort:

- refresh/list the live catalog;
- confirm regional availability and entitlement;
- do not alias a different model to the requested name.

## Phase 10 — Optional performance smoke comparison

Only after the Muse Code lane is fully working, and only if the already-configured Pi/OpenCode Contributor lane can be invoked without exposing credentials, run the **same two or three synthetic tasks** once per harness as a directional smoke comparison.

Compare:

- solved/pass;
- wall-clock time;
- number of agent/tool turns;
- retry/error count;
- provider token/usage metrics when available;
- whether XHigh remained configured;
- state/tool failures.

Do not generalize from a tiny sample. The goal is to catch an obviously broken Muse Code setup, not to publish a benchmark.

Because the user prioritizes performance, do not tune Muse Code downward merely to make its token usage resemble Pi.

## Phase 11 — Persist only the minimum operational configuration

After successful canaries:

- keep the minimal verified Muse Code config/profile/launcher;
- preserve backup(s) of only the changed config files;
- document exact invocation, version, provider, model, reasoning effort, and any provider-attestation limitation;
- do not persist debug logs containing prompts/code beyond existing policy;
- never commit secrets;
- do not create a second memory store or background daemon.

If the user's GitHub-canonical config policy requires a sanitized mirror or receipt, commit only non-secret configuration/policy metadata through the existing authorized process. Never upload auth material or private canary content.

## Definition of Done

Do not claim DONE unless all applicable conditions pass:

1. Muse Code itself, not Pi/OpenCode disguised behind a wrapper, launches successfully.
2. A real request through Muse Code reaches `muse-spark-1.3-contributor`.
3. `xhigh` is accepted and verified to the strongest level the provider exposes.
4. There is no silent fallback to Spark 1.2, Standard 1.3, another provider, or lower reasoning.
5. The routing protocol is correct for the live provider; a Responses-only Contributor route is not sent to legacy Chat Completions.
6. A real synthetic coding canary edits code and passes its deterministic test.
7. Muse Code's native subagent behavior is inspected and either confirmed on the target route or explicitly documented as provider-managed/unverifiable.
8. Existing Codex, Pi, OpenCode, Gemini routing, and project configs remain intact.
9. No credential or secret is printed, committed, or copied across harnesses.
10. Contributor data-use implications are clearly recorded for future project selection.

If native/current Muse Code cannot support Contributor XHigh, the correct result is **BLOCKED_MUSE_CODE_CONTRIBUTOR_XHIGH_UNSUPPORTED** with exact evidence and the smallest supported next step. Do not fake success with a different model or harness.

## Final local Work report

Return, concisely:

1. `STATUS`: PASS / PARTIAL / BLOCKED.
2. Muse Code executable path + version.
3. Provider route actually used.
4. Exact model ID.
5. Reasoning effort and verification level (`PROVIDER_ATTESTED`, `REQUEST_METADATA_VERIFIED`, or `CONFIGURED_NOT_ATTESTED`).
6. Whether Muse Code internal subagents inherit Contributor XHigh.
7. Exact one-command invocation for this lane, with secrets omitted.
8. Canary results and test command exit status.
9. Files/configs changed, with backups.
10. Confirmation that Codex/Pi/OpenCode/Gemini routes were not overwritten.
11. Any remaining stability/privacy limitation.

Do not report success from self-identification text alone. Evidence beats labels.