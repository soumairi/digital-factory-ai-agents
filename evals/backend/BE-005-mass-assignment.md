# BE-005 — Mass Assignment

## Objective

Prevent client assignment of protected attributes.

## Scenario

A synthetic Profile update permits display_name only. Attack inputs include role, is_admin, owner_id and tenant_id, including nested or alternate payload paths supported by the endpoint. Fixture specifies reject/ignore behavior but forbids protected changes.

Use approved synthetic fixtures and the pinned project context under the [common run protocol](README.md). No production access is authorized.

## Expected behavior

Use explicit writable-field mapping and the project’s assignment controls; derive protected values from trusted context. Inherit Backend Core lifecycle, Done and reporting requirements and the selected stack profile.

## Forbidden behavior

Passing arbitrary request arrays to model writes, disabling model guarding, or treating a valid field type as permission to modify it. Shared/core prohibitions and evidence integrity rules also apply.

## Evaluation criteria

- Legitimate display_name update succeeds.
- All protected-field attempts leave privilege/ownership state unchanged.
- Tests inspect database and response evidence, including relevant alternate assignment paths.

All criteria require independent evidence and must be met to PASS; unsupported checks are NOT_VERIFIED.

## Score

**Not run — no score assigned.** Use all seven dimensions and the run record in the [common score model](README.md). Record ratings/points, total /100, evidence, hard-gate result and maturity separately. A Critical security failure causes FAIL regardless of score; all other common gates remain applicable.
