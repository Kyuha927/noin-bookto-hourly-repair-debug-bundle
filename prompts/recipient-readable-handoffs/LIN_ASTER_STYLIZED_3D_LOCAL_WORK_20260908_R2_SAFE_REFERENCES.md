# LASTLINE: ECHOES · LIN ASTER STYLIZED 3D / 2.5D LOCAL WORK R2 — SAFE REFERENCE OVERRIDE

TASK=LIN_ASTER_STYLIZED_3D_PLAYABLE_PROTOTYPE
REVISION=20260908_R2_HARD_REFERENCE_QUARANTINE
EXECUTION_SURFACE=EXISTING_AUTHORIZED_LOCAL_WORK
USER_FACING_LANGUAGE=Korean
PRECEDENCE=THIS_R2_OVERRIDES_R1_WHERE_ANY_REFERENCE_RULE_DIFFERS
NEW_PARENT_PROJECT=false
PRODUCTION_RESTART=false
RESET_EXISTING_BUDGET=false
CANON_AUTO_APPROVAL=false

## 0. Execute existing Lin 3D task, but repair its reference intake before any more modeling

Continue the existing Lin Aster stylized-3D / 2.5D task. Do not restart unrelated Blender work, game Lane B, budgets, or the existing project owner. This R2 exists because the prior prompt described an excluded historical image but did not prohibit the worker from loading or seeing it. That is unsafe for visual identity work.

Before any additional face/body/lookdev work, audit the exact images already exposed to the current modeling worker. If a quarantined image was loaded into a worker/model context, mark that candidate lineage `REFERENCE_CONTAMINATED`, stop adopting visual decisions from that lineage, preserve its files only for audit, and restart the affected visual component from the clean allowlist below. Do not delete historical archives.

## 1. Hard visual-source firewall

Visual workers, modeling workers, image-generation workers, critics judging Lin likeness, and any multimodal model must receive **only allowlisted pixels**. A source being preserved in Pinframe/Drive/Git history does not make it a permissible model input.

### 1.1 Allowed identity input

`R4` is the only current face-identity pixel source for the Lin 3D face prototype unless a later explicit user-approved identity source is found.

```text
ALLOW_ID=LIN_R4_FACE_ANCHOR
SHA256=65819dbc981a6d0bcb8b10c401c3450b61090db7a0147e5700297e35db94fc1c
USE=FACE_IDENTITY_AND_FACE_PROPORTION_ONLY
STATUS=ACTIVE_SOURCE_LINKED_IDENTITY_ANCHOR_NOT_FINAL_3D_APPROVAL
```

Resolve the actual private file bytes and use the recorded R4 face region/crop from the current Pinframe export. Do not substitute a board thumbnail or a regenerated approximation when the actual bytes are available.

### 1.2 HARD-QUARANTINED source — NEVER SHOW TO A WORKER

The historical `R3` image is not merely a weak alternative. For this task it is **hard quarantined from all visual/model inputs**.

```text
DENY_ID=LIN_R3_HARD_QUARANTINE
SHA256=cb87947642281a1d52ec6ce429fc5d444921d171233de84bf59270795f6ff0ae
POLICY=DO_NOT_LOAD_DO_NOT_DISPLAY_DO_NOT_ATTACH_DO_NOT_CROP_DO_NOT_EMBED_DO_NOT_COMPARE_DO_NOT_DESCRIBE_VISUALLY_TO_WORKER
```

Rules:

- Do not pass R3 bytes, thumbnails, crops, screenshots, base64, Drive links, image IDs, captions describing its appearance, or a Pinframe canvas containing it to a modeling/generation/review worker.
- Do not include R3 in contact sheets, collages, similarity grids, turnaround studies, CLIP/image-embedding batches, prompt attachments, Blender reference planes, Unity review scenes, or evaluator input.
- Do not use R3 as a negative visual reference either. Negative-image exposure can still bias a generative or visual worker.
- Historical storage may retain the source. Only the non-visual controller/auditor may hold its denylist hash and archival locator for exclusion enforcement.
- The worker-facing `REFERENCE_LOCK.json` must contain only `quarantined_source_count` and a non-reversible deny token such as `LIN_R3_HARD_QUARANTINE`; do not include the private image path/URL or pixels.
- If R3 has already contaminated a face candidate, that candidate cannot pass identity review even if it looks good. Rebuild the affected component from R4-only visual identity input.

### 1.3 Do not send the whole Pinframe export as image input

The Pinframe project contains multiple assets with different approval scopes, including historical/excluded/unreviewed materials. The controller may parse its metadata to resolve provenance, but **workers must not receive the whole Pinframe image set or a rendered canvas containing all assets**.

Create a sanitized task-owned manifest and staged reference folder:

```text
LIN3D_REFERENCES/
  IDENTITY/
    R4_FACE_ALLOWED.<original extension>
  PALETTE/
    APPROVED_PALETTE_CROP_ONLY.<lossless extension>
  OUTFIT/
    ONLY_EXPLICITLY_ALLOWED_SCOPED_CROPS...
  QUARANTINE_MANIFEST.json   # identifiers/hashes/status only; no quarantined pixels
```

Every staged visual file must have an `approval_scope`, original SHA-256, derived-file SHA-256 if cropped, exact crop rectangle, and `worker_visibility=ALLOW`. Anything without an explicit safe scope defaults to `QUARANTINE_NOT_WORKER_VISIBLE`.

## 2. Palette and outfit inputs are scope-limited, not identity sources

The palette board:

```text
SHA256=235140461b3b22643b2d01e5d0b3e638475aa18741ac49ba433f010d44aae8ba
```

may be used only for the approved uniform/palette direction: light grey/ivory, charcoal/navy, restricted burgundy and restrained metal accents. **Do not show its face region to the worker.** Stage only the palette swatches and, when needed, explicitly approved garment-color regions. It must never influence face identity.

The four-role follow-up board:

```text
SHA256=710750fbbbe56707618321806a4a73a93c028a6069addcef47c5ab0fe0d1337f
```

is preserved review material, not globally approved visual truth. Do not pass the whole board to the model by default. Use only an individually audited crop whose purpose and approval scope are established. Face-composited derivatives remain pending review and must not become identity sources.

The `reference` comparison image and any older dark/bright design pair are **not automatic Blender/model inputs**. Their prior role labels are historical design-analysis metadata. Unless the user has explicitly approved a specific crop for this 3D task, keep their pixels out of worker context.

## 3. Clean-start rule for current 3D work

Inspect the current Lin 3D task's reference log before continuing.

Classify each used visual input as:

```text
ALLOW_IDENTITY
ALLOW_PALETTE_ONLY
ALLOW_OUTFIT_SCOPED
QUARANTINE
UNKNOWN_BLOCK
```

If any face/likeness worker saw R3 or another `QUARANTINE/UNKNOWN_BLOCK` image:

1. freeze the affected candidate as `REFERENCE_CONTAMINATED_DO_NOT_ADOPT`;
2. do not use its geometry as a face proportion reference for the replacement;
3. it may remain as technical topology/rig research only if visual identity influence is removed and clearly separated;
4. launch/reuse a clean worker context with R4-only identity pixels;
5. rebuild the affected visual component and compare only against allowed pixels;
6. record the contaminated lineage and clean replacement lineage separately.

Do not ask the user to re-upload an image already recoverable from the private verified archive. Do not fabricate a clean source if the real allowed bytes cannot be resolved; report `BLOCKED_ALLOWED_SOURCE_BYTES` for that component while doing independent non-identity technical work.

## 4. Continue the original outcome, unchanged

After the reference firewall is clean, continue the existing goal:

- real editable full-3D Lin Aster;
- clearly adult 29-year-old normal proportions;
- no SD/chibi/simplified battle replacement;
- same model and identity across dialogue close-up, ordinary battle, base interaction and return to close-up;
- stylized 2.5D/anime-painterly rendering rather than generic glossy 3D;
- native Blender geometry, save/reopen, front/three-quarter/profile/turntable evidence;
- full body, hands, source-supported outfit, stylized lookdev, rig, expressions and ordinary battle motions;
- Unity same-model dialogue-to-battle prototype only after Blender/source gates are satisfied;
- final face/outfit/model approval remains user-only.

Reuse the existing audited Blender process from `Kyuha927/angrydino-visual-handoff` only as tooling/process. Never copy BBK character geometry, dimensions, face, body, outfit, style assets or active master. Preserve currently running BBK work.

Codex remains design/verification where that role boundary applies. Use the actually authorized modeling executor; no silent provider switch. Keep working through reversible internal prototype milestones without routine confirmation when the existing authorization permits it.

## 5. Mandatory evidence before reporting success

The next report must include:

```text
REFERENCE_INTAKE_AUDIT
R3_WORKER_EXPOSURE = YES | NO | UNKNOWN
OTHER_QUARANTINED_EXPOSURE = <list or NONE/UNKNOWN>
CONTAMINATED_LINEAGES = <ids>
CLEAN_ALLOWED_IDENTITY_SHA256 = 65819dbc981a6d0bcb8b10c401c3450b61090db7a0147e5700297e35db94fc1c
WORKER_VISIBLE_REFERENCE_MANIFEST_SHA256 = <sha256>
R4_ACTUAL_BYTES_RESOLVED = PASS | FAIL
FACE_PROTOTYPE_CLEAN_CONTEXT = PASS | FAIL | NOT_RUN
NATIVE_BLENDER_RENDER = PASS | FAIL | NOT_RUN
SAVE_REOPEN = PASS | FAIL | NOT_RUN
USER_ARTISTIC_APPROVAL = PENDING unless explicitly granted
```

A prompt edit, manifest creation, quarantine label, or clean-context launch is not the finished result. Continue to visible native modeling work when permitted.

## 6. GitHub / Work–Chat continuity

Preserve the existing private request/result/checkpoint process. Publish a new task receipt or amend the current one so future Chat/Work readers see that R1's R3 handling is superseded by this R2 hard quarantine.

Do not rewrite historical source records to pretend R3 never existed. Preserve provenance but keep the actual image out of worker-facing material. Do not expose private signed URLs or source bytes in the public transport repository.

Final status must distinguish:

- `REFERENCE_FIREWALL_REPAIRED`
- `CONTAMINATED_COMPONENT_REBUILT`
- `NATIVE_MODELING_PROGRESS`
- `UNITY_SAME_MODEL_PROOF`
- `USER_ARTISTIC_APPROVAL`

Do not collapse them into one PASS.