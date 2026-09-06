# ONE-SHOT TASK: Replace WebGPT's ChatGPT Review Path with Oracle, Preserve Browser Computer Use

## Mission

Audit the current local Codex configuration and refactor the existing WebGPT integration so that:

1. Oracle becomes the standard mechanism for ChatGPT-based independent model review.
2. The existing WebGPT/browser skill remains available for general browser automation and Computer Use.
3. Existing safety, authorization, worker-routing, storage-safety, and fail-closed policies remain intact.
4. Gemini 3.7 Flash High remains the only execution worker where the current policy requires it.
5. Oracle is classified strictly as a read-only advisory reviewer, never as an execution worker.
6. Codex remains the sole final verifier and completion authority.

Perform the work end-to-end in this run.

Do not stop after analysis or produce only recommendations.

---

# 0. Non-negotiable safety boundaries

Do NOT weaken, delete, bypass, reinterpret, or silently override any existing:

- authorization rule
- privacy rule
- destructive-action safeguard
- storage-reclamation safeguard
- browser/Computer Use safeguard
- model routing lock
- worker-selection rule
- confirmation requirement
- fail-closed behavior
- credential/login protection
- background-computer-use protection

Do not expose, copy, print, log, or request credentials, cookies, access tokens, API keys, session tokens, passwords, or browser authentication material.

Do not copy authentication cookies from the user's normal live Chrome profile unless an existing explicit local policy already authorizes that exact behavior.

Do not enable API billing as a fallback.

Do not silently use an OpenAI API key even if one exists in the environment.

Do not create or modify GitHub branches, PRs, remote repositories, Cloud Work sessions, or other remote workspaces unless the existing local policy explicitly requires it for this task.

Do not delete the existing WebGPT skill.

Do not modify unrelated project files.

---

# 1. Read-only audit first

Before changing anything, inspect the actual current environment.

At minimum inspect, if present:

- ~/.codex/AGENTS.md
- ~/Documents/AGENTS.md
- project-level AGENTS.md files relevant to the active workspace
- ~/.codex/config.toml
- ~/.codex/skills/
- adaptive-debugging skill and policy
- universal-cli-worker-selection skill and policy
- storage-reclamation-safety skill and policy
- existing WebGPT-related skill(s)
- existing browser-use / Computer Use skill(s)
- MODEL_ROUTER_DECISION_V5.json or its current replacement
- any wrappers, commands, scripts, prompts, MCP definitions, aliases, launch agents, or configuration that currently route work to ChatGPT web
- any existing Oracle installation or configuration
- ~/.oracle/config.json if it already exists

Search the filesystem for relevant references such as:

    WebGPT
    webgpt
    ChatGPT review
    second opinion
    second-model
    oracle
    oracle-mcp
    browser-use
    computer use
    GPT-5
    reviewer
    worker-selection

Do not assume filenames or locations beyond known global files.

Build an internal routing map showing:

    task
      -> adaptive debugging
      -> execution worker selection
      -> ChatGPT/WebGPT review
      -> browser automation
      -> final verification

Determine precisely which existing WebGPT functionality is:

A. ChatGPT second-model review

versus

B. general browser / website / Computer Use automation

Only category A is a replacement target.

---

# 2. Protect the existing worker architecture

The target architecture is:

    USER
      |
      v
    Codex
      |
      +-- adaptive-debugging
      |
      +-- execution worker route
      |     |
      |     +-- Gemini 3.7 Flash High ONLY
      |
      +-- INDEPENDENT_REVIEW_GATE
      |     |
      |     +-- Oracle
      |           |
      |           +-- ChatGPT browser
      |           +-- GPT-5.6 Sol
      |           +-- Extra High or Pro effort
      |
      +-- domain safety skills
      |
      +-- Codex final validation

Oracle MUST NOT be registered as:

- an execution worker
- a worker-selection fallback
- an autonomous coding worker
- a replacement for Gemini 3.7 Flash High
- a replacement for adaptive-debugging
- a replacement for storage-reclamation-safety
- a replacement for Codex final verification

Explicitly document this distinction wherever necessary.

Use terminology equivalent to:

    EXECUTION_WORKER != INDEPENDENT_REVIEWER

and:

    Oracle output is advisory evidence.
    Oracle output never constitutes completion proof.

---

# 3. Verify current Oracle upstream before installation

Use the current official upstream `steipete/oracle` documentation and the installed CLI help as the source of truth.

Do not rely on remembered command syntax when current help or documentation is available.

Verify:

- current stable Oracle version
- Node requirement
- supported installation method
- Codex bridge support
- Codex skill integration
- MCP support
- browser engine behavior
- current GPT-5.6 browser model syntax
- supported thinking-effort values
- manual-login / attach-running browser behavior
- session recovery commands
- dry-run behavior

Record the Oracle version actually installed or used.

---

# 4. Install or update Oracle with minimum disruption

If Oracle is already installed:

1. inspect the version
2. validate it against current upstream
3. update only if necessary for the required GPT-5.6/browser/Codex behavior

If Oracle is not installed:

Prefer the least disruptive officially supported installation method already compatible with this Mac.

Possible supported paths may include Homebrew or npm, but verify current upstream first.

Do not perform a global Node runtime migration merely to satisfy Oracle.

If the current Node runtime is incompatible and no safe supported installation path exists, prepare the configuration changes that do not require Oracle execution and report:

    BLOCKED_ORACLE_RUNTIME_REQUIREMENT

Do not weaken the system to bypass the requirement.

---

# 5. Install the official Oracle Codex skill

Use the current official Oracle skill from `steipete/oracle`.

Install it into the appropriate Codex skill directory according to current upstream guidance.

Typical destination may be:

    ~/.codex/skills/oracle

but verify current Codex/local policy before modifying it.

Do not replace local policy files with Oracle upstream files.

The Oracle skill is subordinate to the existing local/global AGENTS and policy hierarchy.

If there is a conflict:

    local safety/policy wins

Do not duplicate large sections of upstream Oracle documentation into local policy.

Keep the integration thin.

---

# 6. Configure Oracle MCP for Codex

Use the current upstream Codex bridge helper if supported, such as the current equivalent of:

    oracle bridge codex-config

Inspect its output before applying it.

Do NOT blindly overwrite ~/.codex/config.toml.

Merge only the required Oracle MCP configuration while preserving every unrelated existing MCP server and Codex setting.

The Oracle MCP must default to browser-backed review, not API mode.

Force the browser path explicitly through supported configuration, environment, or per-call options.

The intended invariant is:

    ORACLE REVIEW
      -> browser engine
      -> signed-in ChatGPT subscription
      -> no API billing fallback

If OPENAI_API_KEY or another API credential exists, Oracle must still not silently change to API mode for this review route.

For MCP `consult`, explicitly supply browser mode or a verified browser-only preset.

Fail closed if the intended browser route cannot be verified.

---

# 7. Browser authentication strategy

Prefer Oracle's current supported persistent manual-login profile for ChatGPT review if it can be configured safely.

Do not reuse or copy the live Chrome profile's cookies by default.

Do not extract login credentials.

Do not automate password or MFA entry.

If Oracle already has a valid authenticated persistent browser profile, use it.

If a one-time human login is required:

- complete every other configuration step first
- launch only the supported Oracle login flow if allowed by local browser policy
- do not enter credentials for the user
- record exactly:

    HUMAN_LOGIN_REQUIRED

- leave the system otherwise ready to continue after login

Do not classify missing human authentication as a software configuration failure.

If existing browser policy requires attach-running instead, use the policy-compliant supported Oracle attach mode.

Never weaken browser safety policy just to make Oracle easier to run.

---

# 8. Replace only WebGPT's ChatGPT-review responsibility

Locate all existing WebGPT routes that perform functions equivalent to:

- send a problem to ChatGPT
- assemble repository/project context for ChatGPT
- upload review files to ChatGPT
- ask a stronger model for debugging or architecture review
- wait for a long ChatGPT reasoning result
- recover an incomplete ChatGPT review
- manage second-opinion ChatGPT conversations
- parse ChatGPT review results

Redirect these responsibilities to Oracle where Oracle provides the equivalent capability.

Do NOT delete the old implementation immediately if doing so could break callers.

Prefer:

    deprecated compatibility wrapper
        -> Oracle review

or:

    WebGPT review entrypoint
        -> Oracle

while preserving existing interfaces where practical.

Remove duplicated browser automation logic only after proving no other WebGPT functionality depends on it.

---

# 9. Preserve general Browser / Computer Use

The following must remain on the existing browser/Computer Use route:

- arbitrary website navigation
- authenticated website interaction
- form filling
- UI verification
- clicking application controls
- Flow Music or similar web app operation
- GitHub web UI operation when applicable
- general browsing tasks
- website-specific troubleshooting
- live rendered UI tests

Oracle must NOT become the generic browser automation system.

Required routing distinction:

    "Ask ChatGPT/GPT for an independent review"
        -> Oracle

    "Operate or inspect a normal website"
        -> Browser / Computer Use

Ensure trigger descriptions make this distinction unambiguous.

---

# 10. Add INDEPENDENT_REVIEW_GATE

Integrate a minimal independent-review escalation gate into the existing adaptive-debugging policy.

Do not replace adaptive-debugging.

Oracle should be invoked automatically only when at least one of these conditions is met:

### Trigger A: repeated failure

Two materially similar attempted fixes have failed, or the local adaptive-debugging policy already defines a stricter escalation threshold.

Use the stricter existing policy if present.

### Trigger B: competing root-cause hypotheses

There are multiple plausible root causes and available evidence does not clearly select one.

### Trigger C: high-impact design decision

Examples:

- non-trivial architecture change
- database/storage-layout change
- migration
- authentication design change
- orchestration change
- substantial refactor
- destructive cleanup strategy
- data-loss-risk path

Oracle reviews the plan only.

Oracle never authorizes the destructive action.

### Trigger D: completion ambiguity

Tests partially pass or evidence conflicts and Codex cannot confidently determine whether the task is actually complete.

Use Oracle as an independent audit.

### Trigger E: explicit user request

Examples include user intent equivalent to:

- Oracle review
- second opinion
- another strong model review
- GPT Pro review
- independent review
- cross-check this with another model

---

# 11. Cases where Oracle must NOT be automatically invoked

Do not automatically invoke Oracle for:

- simple syntax fixes
- trivial edits
- obvious deterministic errors
- normal documentation edits
- single-file low-risk changes
- tasks already proven by deterministic tests
- routine formatting
- ordinary browsing
- every worker result
- every Codex response

Avoid creating a review bureaucracy.

Oracle is an escalation tool, not a default extra turn for all work.

---

# 12. Model and effort policy

First inspect any existing WebGPT model/effort policy.

Preserve explicit existing user policy when compatible with the new architecture.

If no explicit model policy exists, use:

### Normal independent review

    model: gpt-5.6-sol
    engine: browser
    thinking effort: extra-high

### Exceptional escalation

Use Pro effort only for:

- exceptionally difficult root-cause analysis
- high-impact architecture decisions
- unresolved failures after normal independent review
- explicit user request for Pro
- cases where the existing adaptive-debugging policy already calls for maximum review

Target:

    model: gpt-5.6-sol
    engine: browser
    thinking effort: pro

Do not use stale GPT aliases if the current upstream offers a more explicit verified GPT-5.6 target.

Verify the resolved model and effort from Oracle/session/browser metadata whenever possible.

If the requested model/effort cannot be verified:

    BLOCKED_ORACLE_MODEL_SELECTION_UNVERIFIED

Do not silently downgrade.

Do not silently route to an API model.

---

# 13. Oracle context rules

Oracle receives only the context necessary for the review.

Before a real review:

1. select the minimum relevant files
2. exclude generated files, caches, dependencies, huge fixtures, secrets, credentials, tokens, private auth material, irrelevant binaries
3. use Oracle dry-run / file report functionality
4. inspect the resolved file set
5. only then launch an expensive or high-effort review

Prefer:

    exact relevant files
    failing test
    error logs
    specification/policy involved
    relevant diff

over:

    entire repository

Do not include `.env`, keychains, browser data, auth databases, token stores, credential files, SSH keys, or equivalent sensitive material.

---

# 14. Oracle review contract

Every Oracle review request generated by the local system should contain:

1. Situation
2. Objective
3. Observed evidence
4. Attempts already made
5. Exact files supplied
6. Constraints
7. Competing hypotheses, if any
8. Exact question to the reviewer
9. Requested output structure

Ask Oracle to distinguish:

    FACTS
    INFERENCES
    UNCERTAINTIES
    RECOMMENDATION
    VERIFICATION STEPS

For debugging reviews, request citations to relevant file paths and line numbers where possible.

Oracle must not be asked to modify local files.

Oracle proposes.

Codex decides.

---

# 15. Long-running Oracle session handling

Replace brittle WebGPT retry behavior with Oracle session recovery where supported.

Do not submit the same expensive prompt repeatedly just because a long Pro response has not immediately appeared.

On an incomplete or long-running Oracle result:

1. inspect the existing Oracle session
2. inspect status/session metadata
3. reattach or recover using the existing session when supported
4. retry submission only when there is evidence the original request did not successfully start

Preserve any stronger existing local no-duplicate-submission policy.

Do not report success merely because a request was accepted.

---

# 16. Fail-closed routing

Introduce explicit failure states equivalent to:

    BLOCKED_ORACLE_UNAVAILABLE
    BLOCKED_ORACLE_BROWSER_UNAVAILABLE
    BLOCKED_ORACLE_AUTH_REQUIRED
    BLOCKED_ORACLE_MODEL_SELECTION_UNVERIFIED
    BLOCKED_ORACLE_RUNTIME_REQUIREMENT
    BLOCKED_ORACLE_REVIEW_FAILED

If Oracle review is required by policy and unavailable:

Do not silently fall back to:

- WebGPT's deprecated ChatGPT-review implementation
- OpenAI API
- another model
- another execution worker
- another browser engine
- Gemini review
- Claude review

unless an existing explicit higher-priority policy already authorizes that exact fallback.

Routine execution may continue only where the independent-review gate is not mandatory.

---

# 17. Keep existing WebGPT as a compatibility layer where useful

If external prompts/scripts call a WebGPT review command directly, preserve compatibility where practical.

Preferred migration pattern:

    old WebGPT ChatGPT-review command
       -> compatibility notice internally
       -> Oracle adapter
       -> same or normalized review result

Avoid forcing immediate rewrites across unrelated projects.

Mark the old internal ChatGPT-review implementation as deprecated, not deleted, until no callers remain.

General browser functionality is NOT deprecated.

---

# 18. No Oracle image-generation integration

This migration concerns text/code/research review only.

Do not configure or invoke Oracle image generation.

Do not alter existing image-generation policy.

Do not use Oracle `chatgpt_image` or equivalent image-generation functionality in tests.

---

# 19. Configuration hygiene

Before modifying each configuration or policy file:

- capture its current path
- capture a checksum
- create a rollback-safe backup if local policy permits
- preserve formatting where practical

Make the smallest coherent change.

Do not rewrite entire AGENTS.md or POLICY.md files merely to insert a few routing rules.

Do not duplicate rules already defined at a higher policy level.

Prefer references to existing policies over copy-pasting them.

---

# 20. Validation tests

After configuration, run validation in this order.

## Test 1: Oracle CLI readiness

Verify:

- executable available
- version
- help command
- browser capability
- no secret output

## Test 2: Oracle bundle dry-run

Create or use a harmless local text file with no sensitive information.

Run an Oracle dry-run that:

- resolves one file
- displays the file report
- does not contact ChatGPT
- does not mutate browser state

PASS only if the selected file set matches expectation.

## Test 3: MCP readiness

Verify Codex can discover the Oracle MCP server/tool without removing existing MCP servers.

PASS only if:

- Oracle MCP is visible
- existing MCP integrations remain intact
- browser routing is explicit

## Test 4: routing static test

Verify policy routing for at least these cases:

Case 1:

    "Fix this obvious typo"

Expected:

    no Oracle

Case 2:

    "The same bug fix failed twice and two root causes remain plausible"

Expected:

    Oracle independent review eligible/required according to adaptive-debugging

Case 3:

    "Open Flow Music and inspect the Generate error"

Expected:

    Browser/Computer Use
    NOT Oracle

Case 4:

    "Have GPT Pro independently audit this architecture plan"

Expected:

    Oracle
    browser engine
    GPT-5.6 Sol
    Pro effort

Case 5:

    "Use the execution worker"

Expected:

    existing Gemini 3.7 Flash High route
    NOT Oracle

## Test 5: live harmless Oracle review

Only if an authenticated Oracle browser profile is already available.

Use a harmless test prompt equivalent to:

    Review the attached harmless text file.
    Reply exactly: ORACLE_REVIEW_OK
    Do not modify anything.

Verify:

- browser engine used
- expected ChatGPT model resolved
- requested effort resolved where observable
- answer captured
- Oracle session stored
- no API fallback occurred
- no project mutation occurred

If authentication is not available:

Do not fake PASS.

Report:

    HUMAN_LOGIN_REQUIRED

and classify the remaining setup separately from the already completed configuration.

## Test 6: legacy WebGPT browser preservation

Verify that the general WebGPT/browser Computer Use entrypoint still exists and is not redirected to Oracle.

No live third-party website mutation is required for this test.

---

# 21. Regression checks

After edits confirm:

- adaptive-debugging still loads
- worker-selection still loads
- Gemini 3.7 Flash High execution lock is unchanged
- storage-reclamation-safety still loads
- existing Browser/Computer Use still loads
- existing MCP servers remain configured
- no unrelated model provider was enabled
- no API fallback was introduced
- no credentials were added to configuration
- no global safety rule was weakened
- Oracle is not listed as an execution worker

Search the final configuration for accidental conflicting routes.

---

# 22. Completion criteria

Do not claim COMPLETE unless all applicable conditions are verified:

- Oracle installed or safely runnable
- Oracle version recorded
- official Oracle Codex skill integrated
- Oracle MCP integrated or a documented reason exists for using CLI-only integration
- browser mode is explicit
- API fallback is prevented for the independent-review path
- existing WebGPT ChatGPT-review route is redirected/deprecated
- existing general Browser/Computer Use route is preserved
- INDEPENDENT_REVIEW_GATE implemented
- worker-selection behavior unchanged
- adaptive-debugging preserved
- safety policies preserved
- dry-run passes
- static routing tests pass
- authenticated live review passes, or HUMAN_LOGIN_REQUIRED is explicitly reported
- rollback information exists
- final diff has been inspected

---

# 23. Final report

At the end return a concise evidence-based report with exactly these sections:

## STATUS

One of:

    PASS
    CONDITIONAL_PASS
    BLOCKED

## ORACLE

- installed version
- installation/runtime path
- engine
- default review model
- normal effort
- escalation effort
- authentication state
- MCP state

## ROUTING

Show the final routing diagram.

## WEBGPT MIGRATION

State:

- what was redirected to Oracle
- what was deprecated
- what Browser/Computer Use functionality was preserved

## FILES CHANGED

For each changed file:

    path
    purpose
    backup/rollback information

## TESTS

For every validation test:

    PASS / FAIL / BLOCKED
    evidence

## POLICY INVARIANTS

Explicitly confirm whether each remained unchanged:

- Gemini 3.7 Flash High execution-worker restriction
- Codex final-verifier role
- storage safety
- authorization safeguards
- browser safeguards
- fail-closed routing

## BLOCKERS

List only unresolved blockers.

## ROLLBACK

Give the shortest exact rollback procedure.

Do not claim that a test passed unless it was actually executed and observed.

Do not hide partial failures.

Do not continue retry loops without new evidence.

The desired end state is a smaller, clearer architecture:

    Gemini Flash = execution worker
    Oracle = independent reviewer
    Browser/Computer Use = general web operator
    Codex = final verifier

Implement that architecture with minimum policy churn and maximum verifiability.
