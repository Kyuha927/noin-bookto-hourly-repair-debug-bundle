# Local Work one-shot: Diagnose `Model API is not available to all audiences.` for Muse Code / Meta Model API

Date: 2026-09-07 (Asia/Seoul)
Target: the user's current macOS local Work/Codex environment
Observed symptom: Muse Code launches a Facebook/Meta login flow, authentication appears to complete, but access then fails with the exact message `Model API is not available to all audiences.`

## Primary objective

Determine, with the smallest safe evidence set, whether this failure is caused by:

1. Meta Model API country/region availability,
2. account-level audience/entitlement rollout,
3. age/account-status eligibility,
4. a Muse Code OAuth/session integration defect,
5. a stale or conflicting local Muse Code auth/config state,
6. a temporary Meta service-side rollout/outage,
7. or another clearly evidenced cause.

This is a **diagnosis-first task**. Do not bypass eligibility controls, spoof geography, change account identity, weaken security, or create a replacement account. Do not purchase anything. Do not change Facebook/Meta account settings unless a later user turn explicitly authorizes a specific change.

The user wants a concise, evidence-backed conclusion and the shortest legitimate next step.

## Current public facts to verify, not blindly trust

As of 2026-09-07, Meta publicly describes Meta Model API as a public preview with "expanded global access," but that wording does not prove universal availability for every account or country. Meta also exposes Muse Spark and Muse Code through its developer surfaces.

Useful official starting points when network access is available:

- https://ai.meta.com/llama/
- https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/
- https://ai.meta.com/
- the current Muse Code CLI help and first-party documentation installed or linked by the current release

Prefer current first-party documentation and live response metadata over old blog posts, third-party articles, or cached examples.

## Non-negotiable safety and privacy rules

1. Never print, copy, export, upload, or commit Facebook/Meta cookies, OAuth tokens, refresh tokens, API keys, browser storage, credential files, session IDs, authorization headers, or secrets.
2. Do not dump full environment variables, keychains, browser profiles, or auth databases.
3. Do not inspect unrelated personal files or browsing history.
4. Do not use VPNs, proxies, alternate geolocation, identity changes, alternate birth dates, developer-account impersonation, or any other eligibility/security bypass.
5. Do not create a new Facebook/Meta account as a workaround.
6. Do not disable account security, 2FA, browser protections, TLS validation, or Muse Code security checks.
7. Do not delete credentials broadly. If a local Muse-specific stale auth state is proven, report the supported repair step first; only execute a logout/login reset if it is reversible, scoped only to Muse Code, and does not alter the Meta account itself.
8. Preserve existing Codex, Pi, OpenCode, Gemini routing, repositories, project settings, and unrelated credentials.
9. Do not send private production repositories to Contributor/Meta Model API during diagnosis. Use tiny synthetic prompts only if an API canary becomes available.
10. Treat self-identification text from a model as non-evidence. Prefer HTTP status, provider metadata, CLI diagnostics, and official account/access screens.

## Phase 1 — Capture the exact local baseline

Perform minimal read-only inspection and record:

- macOS version and architecture;
- exact `muse` executable path and Muse Code version/build;
- install source and relevant Muse Code config/auth locations discovered from current help/docs;
- whether duplicate Muse Code installations/wrappers exist on PATH;
- current Muse Code login/provider state, **without exposing credentials**;
- exact command or UI sequence that triggers the Facebook/Meta login;
- exact visible error string, timestamp, and whether it appears in browser UI, Muse Code terminal, or both;
- sanitized status/error code if Muse Code exposes one;
- whether the failure occurs before or after successful Meta/Facebook authentication/consent;
- whether Muse Code reaches an authorization callback successfully before the audience error.

Do not infer account eligibility merely because Facebook login succeeds. Authentication and Model API entitlement are separate questions.

## Phase 2 — Reproduce once, safely

Reproduce the normal supported Muse Code login flow **once** if necessary to obtain clean evidence.

Requirements:

- use the normal official Muse Code login/auth command;
- use the user's existing intended Meta/Facebook account;
- do not change account settings;
- do not clear all browser data;
- do not retry in a loop;
- do not capture or display tokens/cookies;
- record only sanitized URL host/path, visible page title/message, redirect stage, HTTP/error code when safely exposed, and Muse Code's own sanitized error output.

Classify where the failure happens:

- `AUTHENTICATION_FAILED`: Facebook/Meta identity login itself fails.
- `AUTHENTICATED_BUT_NOT_ENTITLED`: identity succeeds but Model API access is denied.
- `CALLBACK_OR_OAUTH_INTEGRATION_FAILED`: Meta authorization appears granted but Muse Code cannot complete/consume the callback.
- `LOCAL_SESSION_STATE_FAILED`: a stale/corrupt Muse-only local session is evidenced.
- `UNKNOWN_STAGE`: evidence is insufficient.

Do not label it `AUTHENTICATED_BUT_NOT_ENTITLED` solely from intuition; prove the stage from the flow.

## Phase 3 — Test Meta Model API eligibility independently of Muse Code

Use the safest current first-party Meta developer surface to determine whether the same account has Meta Model API access **without relying on Muse Code**.

Preferred order:

1. Open the current official Meta AI developer / Meta Model API start page while authenticated with the same account.
2. Observe whether the account can reach the Model API onboarding/dashboard/model/API setup surface, or receives the same audience/eligibility denial.
3. If first-party documentation exposes a supported read-only account/access-status check, use it.
4. Do **not** create API keys, enable billing, accept new paid plans, create apps/projects, or mutate the account merely to diagnose access.

Record only:

- whether the first-party developer surface is reachable;
- exact visible eligibility message;
- sanitized HTTP status/error identifier when available;
- whether the account is offered normal Model API onboarding or blocked before onboarding.

Interpretation:

- If the same audience/eligibility error appears outside Muse Code, strongly classify this as `META_ACCOUNT_OR_AUDIENCE_ELIGIBILITY`, not a Muse Code configuration defect.
- If Meta Model API onboarding/dashboard works normally outside Muse Code but Muse Code alone fails, prioritize `MUSE_CODE_OAUTH_OR_LOCAL_INTEGRATION`.
- If both surfaces intermittently fail with service errors, investigate current Meta service status/release issues before changing local configuration.

## Phase 4 — Determine whether geography is actually evidenced

Do not assume Korea is unsupported merely because the account is located in Korea.

Check current first-party availability documentation for Meta Model API, Muse Code, and Muse Spark. Determine whether Meta publishes an explicit supported-country/region list or audience restriction relevant to this account.

Classify geography only if there is direct evidence:

- `REGION_CONFIRMED_UNSUPPORTED`: current official documentation or a provider response explicitly says the user's actual region/country is unsupported.
- `REGION_POSSIBLE_NOT_PROVEN`: region restrictions exist but no official evidence maps this account to an unsupported region.
- `REGION_NOT_INDICATED`: no geographic denial evidence is present.

Never infer country from IP geolocation alone when account entitlement may be the actual gate. Do not use a VPN to test another country.

## Phase 5 — Check account/audience prerequisites without changing them

Using only visible/read-only account information that the user can normally access, determine whether first-party Meta documentation names any prerequisites such as:

- minimum age,
- account standing,
- developer enrollment,
- rollout cohort,
- verified contact information,
- organization/business requirement,
- supported country/territory,
- invitation/allowlist status,
- payment/billing availability.

Only report a prerequisite as the cause when evidence shows it is actually unmet.

Do not expose the user's birthday, phone, email, account ID, or other personal details in the final report. A simple `AGE_REQUIREMENT_MET/UNKNOWN`, `ACCOUNT_STANDING_NO_VISIBLE_ISSUE/UNKNOWN`, etc. is enough.

If Meta provides only the generic phrase `not available to all audiences` and no exact prerequisite, classify the cause as `ACCOUNT_AUDIENCE_ENTITLEMENT_NOT_DISCLOSED` rather than inventing a reason.

## Phase 6 — Check current upstream issues

Search current first-party release notes, official Meta documentation, and relevant public Muse Code issue trackers for the exact error string and recent OAuth/access regressions.

Prioritize:

1. Meta/Muse Code first-party sources,
2. reproducible GitHub issues with version and error evidence,
3. community reports only as weak corroboration.

Determine whether there is a current known issue affecting:

- Facebook login callbacks,
- account entitlement propagation,
- Model API rollout,
- regional access,
- Muse Code client versions,
- stale auth migration after an update.

Do not treat a Reddit/community anecdote as proof of the user's cause.

## Phase 7 — Local Muse Code integrity checks

Only if independent Meta Model API access appears to work, inspect Muse Code's local integration more deeply.

Check, without exposing secrets:

- current Muse Code version versus latest stable;
- whether the installed build supports the current Meta auth flow;
- callback listener/redirect URI behavior;
- duplicate/stale Muse Code installs;
- whether an old config points at a deprecated endpoint/provider;
- whether local clock is materially wrong for OAuth token validation;
- whether a supported logout/login refresh exists;
- whether logs show a sanitized OAuth state/callback error rather than an entitlement denial.

Do not manually edit token files or copy credentials between applications.

If a Muse Code version defect is confirmed, recommend the smallest supported upgrade/repair path. Do not perform unrelated package upgrades.

If stale Muse-only auth state is strongly evidenced and the official client supports a scoped logout/login repair, it is acceptable to perform **only that Muse Code logout/login refresh** if the current task authorization and local safety policy permit reversible auth repair. Otherwise report the exact command/action for the user to approve next.

## Phase 8 — Optional tiny API canary, only if eligibility succeeds

If the account clearly has Model API access and the normal supported authentication flow yields a usable provider connection without exposing credentials, run one tiny synthetic request such as `Reply with OK` through the first-party supported path.

Do not use private code or files.

Record:

- model/provider route,
- success/failure,
- sanitized status/error code,
- no secret-bearing request/response metadata.

Skip this entirely if the account is blocked at entitlement/onboarding.

## Root-cause decision tree

Return exactly one primary diagnosis from this list, plus secondary contributing factors if evidenced:

- `META_REGION_UNSUPPORTED_CONFIRMED`
- `META_ACCOUNT_AUDIENCE_NOT_ENTITLED`
- `META_ACCOUNT_AUDIENCE_ENTITLEMENT_NOT_DISCLOSED`
- `META_AGE_OR_ACCOUNT_PREREQUISITE_UNMET_CONFIRMED`
- `META_MODEL_API_SERVICE_OR_ROLLOUT_ISSUE`
- `MUSE_CODE_OAUTH_INTEGRATION_BUG`
- `MUSE_CODE_STALE_LOCAL_AUTH_STATE`
- `MUSE_CODE_OUTDATED_OR_INCOMPATIBLE_BUILD`
- `NETWORK_OR_CALLBACK_FAILURE`
- `INSUFFICIENT_EVIDENCE`

Do not collapse `not entitled` into `region blocked` unless region is directly evidenced.

## Definition of Done

Do not claim completion until you have, to the extent technically available without account mutation:

1. reproduced or captured the exact failure stage;
2. checked the same account's Meta Model API access independently of Muse Code;
3. checked current first-party availability/eligibility documentation;
4. distinguished region evidence from generic account audience entitlement;
5. checked Muse Code version/auth integration only when warranted;
6. avoided all eligibility/security bypasses and credential exposure;
7. produced one primary root-cause classification with confidence and concrete evidence;
8. given the shortest legitimate next action.

## Final report format

Return concisely in Korean:

1. `STATUS`: DIAGNOSED / PARTIAL / BLOCKED.
2. `PRIMARY_CAUSE`: one exact enum from the decision tree.
3. `CONFIDENCE`: HIGH / MEDIUM / LOW.
4. `WHAT_PROVES_IT`: 2-5 concrete sanitized observations.
5. `REGION`: CONFIRMED_UNSUPPORTED / POSSIBLE_NOT_PROVEN / NOT_INDICATED.
6. `MUSE_CODE`: HEALTHY / OAUTH_BUG / STALE_AUTH / OUTDATED / NOT_RELEVANT / UNKNOWN.
7. `SHORTEST_SAFE_NEXT_STEP`: one actionable legitimate step.
8. `DO_NOT_DO`: only any relevant warnings such as VPN/identity bypass, broad credential deletion, or account recreation.

Do not ask the user to repeat information that can be obtained from the current local environment or current first-party documentation. Do not overstate certainty when Meta does not disclose the precise audience rule.