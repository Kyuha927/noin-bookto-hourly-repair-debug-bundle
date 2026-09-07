# Local Work one-shot: Global OpenCode + Muse Spark 1.3 XHigh web/computer-use worker lane

Date: 2026-09-07 (Asia/Seoul)
Target: the user's current macOS local Work/Codex environment
Primary objective: configure a stable global external worker lane using OpenCode with Muse Spark 1.3 Contributor at `xhigh`, add browser/web-control capability through Playwright MCP plus only necessary OpenCode plugins/custom tools, and make that lane callable from local Work/Codex without replacing the user's existing Sol/Gemini routing or weakening approval/security boundaries.

## User intent and priority

The user wants Muse Spark 1.3 XHigh to behave as a high-performance external execution worker that can do more than code: web research, browser navigation, clicking, form filling, page inspection, screenshots, downloads, authenticated-site workflows when the user is already legitimately logged in, and other supported MCP/plugin/custom-tool actions.

Performance and task success are more important than minimizing Muse token usage. Do not reduce Muse reasoning below `xhigh` for cost savings. Keep Codex/OpenAI token use efficient by returning compact evidence-backed packets to the Work root rather than dumping full OpenCode transcripts.

This prompt is explicit user authorization to add a **new global Muse worker lane** to the existing local Work/Codex routing policy through the proper canonical router/update procedure. It does not authorize bypassing a higher-priority security or account-entitlement gate. It does not authorize replacing the existing Gemini worker lane or changing the Work root model unless the current user separately requests that.

## Current facts to verify against the live installation

Treat these as starting evidence, not immutable assumptions:

- OpenCode Zen currently advertises `muse-spark-1.3-contributor-free` on `https://opencode.ai/zen/v1/responses` using an OpenAI Responses-compatible transport.
- OpenCode Go currently advertises `muse-spark-1.3-contributor` on `https://opencode.ai/zen/go/v1/responses`.
- Current public model metadata exposes reasoning variants `minimal`, `low`, `medium`, `high`, `xhigh`; no `max` variant is exposed for Muse Spark 1.3 Contributor.
- The model supports text and image input and tool calling, but the current OpenCode/Zen path has had recent upstream bugs such as catalog omission, `Invalid upload request`, and overlong tool-name failures. The live environment must be tested instead of assuming those issues are fixed.
- OpenCode supports global MCP servers, custom tools, plugins, skills, and permission rules.
- Microsoft Playwright MCP currently supports browser navigation, clicks, fills, screenshots, code execution, persistent/isolated browser modes, and an extension mode that can connect to existing browser tabs/sessions.

Useful current first-party starting points when network access is available:

- https://opencode.ai/docs/zen/
- https://opencode.ai/docs/go/
- https://opencode.ai/docs/mcp-servers/
- https://opencode.ai/docs/tools/
- https://opencode.ai/docs/custom-tools/
- https://opencode.ai/docs/plugins/
- https://opencode.ai/docs/permissions/
- https://github.com/microsoft/playwright-mcp

Prefer live CLI help, current authenticated `/models` metadata, and current first-party docs over this prompt if syntax changed.

## Hard constraints

1. Preserve the existing Codex Desktop/CLI, Work root configuration, Pi/Astra lane, OpenCode non-Muse models, Muse Code, Gemini worker routing, repositories, project settings, active sessions, privacy controls, storage policies, and approval rules.
2. Do not silently replace the existing default Gemini worker route. Add Muse as an allowed global lane and define when Work may select it.
3. Target Muse reasoning is `xhigh`. No silent downgrade to high/medium/low and no silent fallback to Spark 1.2 or another provider/model.
4. Prefer the authenticated OpenCode Zen/Go Responses route that is actually available and working on this machine. Do not route Muse 1.3 through legacy `/chat/completions`.
5. Do not copy API keys, OAuth tokens, browser cookies, storage-state files, or auth databases into Git, prompts, logs, or other harnesses.
6. Do not bypass region/account entitlement, paywalls, CAPTCHA, MFA, anti-bot checks, security prompts, access controls, or service policies.
7. Browser control may use already-authenticated sessions only through a supported user-authorized Playwright/browser integration. Never scrape or export credentials.
8. Do not globally enable unrestricted shell/filesystem/browser actions. Keep permission gates and narrow tool access.
9. Do not install random computer-control MCPs or remote-control daemons. Full desktop GUI automation is optional and must use an already approved/currently supported local computer-use bridge or an explicitly trustworthy tool with scoped permissions.
10. Do not claim that hosted cloud Work can see local OpenCode merely because local files were edited. Detect the actual Work surface and only claim integration for the supported local execution environment.
11. Do not create a second memory database or a large new orchestration framework. Reuse the existing canonical global routing and skill/wrapper mechanism.
12. Do not expose hidden chain-of-thought. Return conclusions, evidence, files, test results, and action receipts only.

## Phase 1 — Inspect the actual environment first

Perform minimal read-only inspection and record:

- macOS version/architecture and the active shell;
- `opencode` executable path, exact version, install source, and config roots;
- current OpenCode provider/auth status without showing secret values;
- current `opencode models --refresh` or equivalent live catalog for Zen and Go;
- whether `opencode/muse-spark-1.3-contributor-free` is present and callable;
- whether `opencode-go/muse-spark-1.3-contributor` is present and callable;
- the live model metadata for reasoning variants, context/output limits, image/tool support, and provider route;
- whether `xhigh` can be selected and whether runtime/request metadata proves it;
- current OpenCode MCPs, plugins, custom tools, skills, and permission rules;
- whether Playwright MCP is already installed/configured;
- whether a supported browser extension or persistent-profile mode is already present;
- current Work/Codex global instruction chain and authoritative worker/model router;
- the existing approved Gemini lane and its invariants;
- any current external-worker wrapper/skill/bridge already used by Work;
- whether Work is local desktop execution, hosted cloud Work, or another surface.

Do not dump the full environment, Keychain, auth files, browser profiles, cookies, or unrelated config.

## Phase 2 — Normalize OpenCode only as needed

If OpenCode is absent, install the latest stable official release using the current supported method for this machine.

If installed:

- keep it when healthy and new enough for current Muse 1.3 Responses routing;
- upgrade only when needed for this functionality or a known fixed defect;
- use the official update path;
- preserve unrelated OpenCode settings;
- back up only files that will actually be edited;
- do not rewrite all project configs.

After normalization, verify `opencode` starts normally and existing non-Muse provider/model entries remain intact.

## Phase 3 — Select and prove the Muse route

Use this priority order:

### Route A — OpenCode Zen Contributor Free

Use `opencode/muse-spark-1.3-contributor-free` when the authenticated Zen account advertises it **and a real minimal Responses request succeeds**.

Required:

- route resolves to Zen `/v1/responses` or current equivalent;
- `xhigh` is accepted;
- no fallback;
- no server-side `Invalid upload request` or opaque provider failure in the minimal canary.

### Route B — OpenCode Go Contributor

If Zen Free is unavailable/broken but the user already has an authorized OpenCode Go subscription/key and the Go catalog advertises Muse 1.3, use `opencode-go/muse-spark-1.3-contributor`.

Do not purchase Go automatically. Do not ask for or print the API key. Use the supported OpenCode connection flow and existing credential store.

### Route C — blocked

If neither route can make a successful minimal Muse 1.3 XHigh request, do not substitute another model. Leave the integration staged but disabled and return `BLOCKED_MUSE13_XHIGH_PROVIDER_UNAVAILABLE` with the exact sanitized error evidence.

## Phase 4 — Configure a dedicated global Muse XHigh profile/agent

Create the smallest native OpenCode profile/agent configuration supported by the installed version.

Desired identity:

- name/alias: `muse13-xhigh-web` or closest native equivalent;
- model: the proven Route A or Route B Muse 1.3 Contributor model;
- reasoning: `xhigh`;
- no fallback model;
- OpenCode native coding tools enabled under existing permissions;
- browser/web capability enabled through the verified Playwright MCP;
- only a small, curated MCP/plugin/tool set;
- output optimized for evidence-backed parent return, not chatty narrative.

Do not invent config keys. Use the installed OpenCode schema/help.

If OpenCode supports per-agent permissions, make this agent explicit rather than globally granting browser/computer rights to every model.

## Phase 5 — Add Playwright MCP as the primary web-control layer

Prefer the official Microsoft Playwright MCP package/current documented install path.

Configure it globally in OpenCode only after verifying the current syntax. The present documented package is `@playwright/mcp@latest`, but use current first-party docs if changed.

### Browser-mode preference

Use the safest mode that satisfies the task:

1. **Isolated browser/session** for general web research, public sites, tests, and synthetic canaries.
2. **Persistent user data directory** only when needed and supported, scoped to a dedicated automation profile rather than the user's entire default browser profile.
3. **Playwright MCP browser extension mode** only when the user needs OpenCode to interact with an existing logged-in browser tab/session and the extension is already explicitly authorized/installed or can be installed through the normal user-visible process.

Never copy cookies or storage state manually from the user's browser. Never export browser credentials.

### Web capabilities to verify

Verify Muse XHigh can actually call Playwright tools to:

- navigate to a URL;
- inspect structured page/accessibility state;
- click a visible element;
- fill a harmless form in a local/synthetic page;
- take a screenshot;
- read resulting page state;
- download a harmless test file to a temporary workspace when supported;
- preserve browser session state across several tool calls.

Use a local/synthetic or public harmless test site for setup validation, not the user's private production services.

## Phase 6 — Add only high-value OpenCode web/tools/plugins

Keep the tool menu small because Muse can fail on oversized/recursive schemas and long tool names.

Baseline allowed set:

- OpenCode built-ins: `read`, `write/edit/patch` as permitted, `grep/glob`, `bash`, `webfetch`, `skill`, tests/git inspection;
- Playwright MCP;
- at most a few already-approved MCPs needed by the user's real workflows;
- small custom tools only where they remove repeated shell glue;
- plugins only when they provide a clear reliability or integration benefit.

Avoid during initial setup:

- giant database MCP schemas;
- recursive JSON schemas known to break Muse;
- dozens of MCP servers at startup;
- duplicate browser tools;
- tool names approaching provider limits;
- plugins that stream huge raw logs into the parent context;
- undocumented network proxies or provider translators.

For any new plugin/custom tool, inspect source/package provenance and current documentation before enabling it globally.

## Phase 7 — Optional computer-use beyond the browser

Browser automation through Playwright is the default and required capability.

For macOS application/Finder/system GUI control:

- first inspect whether the user's current Work/Codex environment already has an approved local computer-use bridge or MCP;
- reuse that approved bridge if it exposes a safe MCP/custom-tool interface to OpenCode and policy allows delegation;
- keep user-visible confirmations for login, MFA, payments, deletion, permission changes, system settings, and other consequential actions;
- scope accessibility/screen-control permissions to the minimum required application;
- do not install an untrusted generic remote desktop daemon or accessibility bypass.

If no approved desktop-control bridge exists, leave full computer-use disabled and report `BROWSER_CONTROL_READY_DESKTOP_GUI_NOT_CONFIGURED`. This is preferable to installing a risky generic automation layer.

## Phase 8 — Permission model

Preserve the user's existing authorization model.

Recommended starting posture, adapted to current OpenCode syntax:

- public web navigation/read/search: allow when already permitted;
- browser click/fill on harmless public/local pages: allow or existing-policy equivalent;
- authenticated account changes, purchases, sends/posts, deletes, uploads, security settings: ask/require explicit user approval;
- shell writes/edits: preserve existing project policy;
- destructive shell/git/filesystem actions: ask or deny according to current policy;
- new MCP/tool execution not explicitly classified: ask;
- tool wildcard grants: avoid unless narrowly scoped to a trusted server.

Do not use `--auto` as a blanket replacement for granular permissions unless the existing global policy explicitly permits it and explicit denials remain intact.

## Phase 9 — Make Muse callable from local Work/Codex globally

This is the key integration phase.

Locate the **existing canonical external-worker mechanism** used by local Work/Codex. Reuse it instead of inventing a parallel control plane. Depending on the installed environment, this may be a global skill, wrapper, model-router entry, tool bridge, worker-selection policy, or approved CLI runner.

Add Muse through the proper authoritative configuration path.

### Required routing identity

Create a global route such as:

- route ID: `OPENCODE_MUSE13_XHIGH_WEB`
- executor: external OpenCode CLI/session
- model: proven Muse Spark 1.3 Contributor route
- effort: XHigh
- capabilities: coding, shell, webfetch, Playwright browser control, approved MCP/custom tools/plugins
- fallback: none unless the user explicitly authorizes a fallback in a later turn
- parent: current Work/Codex root

### Routing policy

Preserve the existing Gemini lane as default if it is currently canonical.

Muse may be selected when:

- the user explicitly asks for Muse/OpenCode;
- web/browser interaction is materially useful and Muse's browser tool lane is healthy;
- a task benefits from a second independent external model for implementation/debugging;
- the existing router explicitly promotes this lane for a suitable class of work after the new policy update is validated.

Do not silently redirect every task from Gemini to Muse.

If the current authoritative router previously allowed only Gemini, update the **canonical router decision/policy through its normal validated procedure** to add Muse as an allowed lane. Preserve all unrelated prohibitions and safety constraints. Do not bypass the router by calling OpenCode behind its back.

### Work invocation behavior

The parent Work agent should send Muse only the minimum necessary task packet:

- objective;
- workspace/path scope;
- relevant files/artifacts;
- constraints/approval boundaries;
- expected evidence/tests;
- web/browser target and allowed actions when applicable.

Do not forward the entire parent chat transcript unless necessary.

OpenCode/Muse may do deep work internally, but its parent-facing return should be compact.

## Phase 10 — Parent return contract to protect Codex context

Configure the wrapper/skill so Muse returns a decision-ready packet rather than raw terminal/browser logs.

Use an equivalent schema supported by the current integration:

```text
MUSE_WORKER_RETURN_V1
STATUS
RESULT
EVIDENCE
CHANGED_FILES
TESTS
BROWSER_ACTIONS
DOWNLOADS_OR_ARTIFACTS
UNRESOLVED_RISKS
NEXT_ACTION
```

Rules:

- preserve exact errors, failed/skipped tests, contradictions, URLs/hostnames needed for verification, file paths, and consequential browser actions;
- do not include chain-of-thought;
- do not paste full unchanged files, giant diffs, accessibility trees, screenshots-as-base64, or raw Playwright event streams;
- store large artifacts/logs in the existing approved local artifact mechanism and return stable paths/references;
- parent Work must be able to expand/re-read decisive evidence when needed;
- if compaction would lose important detail, return a larger packet rather than forcing a tiny token cap.

This compaction is for the **Muse → Work boundary**. It must not reduce Muse XHigh reasoning depth.

## Phase 11 — Real canary suite

Use a temporary synthetic workspace and harmless test pages.

### Canary A — model/effort proof

Run a minimal Muse request and verify:

- exact provider/model route;
- XHigh configured/accepted to the strongest observable level;
- Responses path;
- no fallback;
- no provider error.

### Canary B — coding loop

Create a tiny repo with one deterministic bug. Muse must inspect, edit, test, and produce a passing diff.

### Canary C — browser loop

Using Playwright MCP, Muse must:

1. open a harmless local/public page;
2. inspect it;
3. click/fill a harmless interaction;
4. verify the resulting state;
5. take a screenshot or other concrete browser evidence.

### Canary D — logged-in-browser capability without secret extraction

If the user has explicitly authorized and configured Playwright extension/persistent browser mode, verify only that Muse can see and interact with a benign already-authenticated page state. Do not reveal cookies/tokens and do not perform account changes.

If not authorized/configured, skip and mark it as intentionally gated.

### Canary E — plugin/MCP schema robustness

Start with Playwright only. Then add each necessary MCP/plugin one at a time and rerun a tiny request. If a tool introduces recursive-schema, overlong-name, upload, or provider errors, disable that tool and keep the base Muse lane healthy.

### Canary F — Work global delegation

From the actual local Work/Codex root, invoke the canonical Muse worker route on a bounded synthetic task.

Pass requires:

- Work actually launches the OpenCode/Muse worker through the approved route;
- Muse performs the task and, where requested, a Playwright action;
- Work receives the compact evidence packet;
- Work can retrieve a decisive artifact/result;
- no native OpenAI subagent is accidentally used as a substitute;
- Gemini route remains available and unchanged.

Do not claim hosted cloud Work integration if the canary was only local.

## Phase 12 — Stability handling

For Muse/Zen/Go transient 429/5xx/network failures:

- use bounded provider-native retry;
- do not loop indefinitely;
- do not change models automatically;
- preserve the final sanitized provider error.

For known-style failures:

- `Invalid upload request`: test the smallest text-only request and current OpenCode/Zen issue status; do not blame Playwright until isolated;
- missing model in picker but present in live `/models`: refresh catalog and verify current upstream bug/fix before adding undocumented local hacks;
- tool-name-length failure: shorten local/custom MCP tool names where safely controllable or disable the offending tool; do not rewrite third-party protocols unpredictably;
- recursive schema rejection: disable/replace the offending MCP schema from this Muse agent rather than disabling all tools;
- wrong endpoint: enforce Responses-compatible route.

If provider-side Muse Free remains broken, prefer an already-authorized Go route if available. Otherwise leave Muse disabled and report the blocker rather than falling back silently.

## Phase 13 — Persist the smallest global configuration

After successful canaries:

- keep one canonical OpenCode Muse agent/profile;
- keep Playwright MCP global only if it is stable and policy-compliant;
- keep only required plugins/custom tools;
- add one canonical Work worker-route/skill/wrapper entry;
- update the authoritative router through its existing validated mechanism;
- keep sanitized configuration evidence/receipt according to the user's GitHub-canonical policy;
- never commit credentials, browser storage, cookies, private page contents, screenshots with secrets, or raw auth files.

Do not copy this entire prompt into always-loaded global AGENTS instructions. The global instruction should be a short pointer/routing rule; detailed operational behavior should live in a lazily loaded policy/skill/wrapper.

## Definition of Done

Do not claim DONE unless all applicable conditions pass:

1. OpenCode is healthy.
2. A real Muse Spark 1.3 Contributor request succeeds.
3. XHigh is selected and verified to the strongest available evidence level.
4. Muse uses a Responses-compatible route and has no silent fallback.
5. Playwright MCP is configured and a real browser canary succeeds.
6. Browser permissions preserve user approval for consequential actions.
7. No risky generic desktop-control layer is added without existing authorization.
8. The OpenCode tool/MCP set remains small enough to avoid known Muse schema/tool-name failures.
9. Local Work/Codex can invoke the Muse route globally through the canonical worker mechanism.
10. Muse returns compact evidence-backed results and the parent can expand decisive evidence.
11. Existing Sol root, Gemini route, Pi, OpenCode other models, Codex, repositories, and security rules remain intact.
12. No secrets or browser credentials are exposed or committed.
13. One end-to-end Work → Muse XHigh → browser/code tool → compact return canary passes.

If the provider is currently broken, return `BLOCKED_MUSE13_XHIGH_PROVIDER_UNAVAILABLE` rather than claiming setup success.

If browser control works but full macOS GUI control is not safely configured, return `BROWSER_CONTROL_READY_DESKTOP_GUI_NOT_CONFIGURED`; this still counts as a valid partial browser-capable Muse lane, not full computer-use.

## Final local Work report

Return concisely in Korean:

1. `STATUS`: PASS / PARTIAL / BLOCKED.
2. OpenCode path/version.
3. Provider and exact Muse model ID.
4. XHigh verification level.
5. Playwright MCP version/mode and browser canary result.
6. Enabled MCP/plugins/custom tools, only names and purpose.
7. Desktop computer-use status.
8. Work global route ID and exact invocation path/skill/wrapper.
9. Work delegation canary result.
10. Muse → Work return packet size/result and evidence retrieval proof.
11. Files/configs changed with backups.
12. Confirmation that Sol/Gemini/Pi/Codex/OpenCode existing routes were not overwritten.
13. Any remaining provider/browser/privacy limitation.

Evidence beats labels. Do not report success from config text alone.