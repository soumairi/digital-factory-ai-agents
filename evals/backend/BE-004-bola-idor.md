# BE-004 — BOLA / IDOR

## Objective

Verify resource-level owner and tenant boundaries.

## Scenario

Prepare two tenants, at least two users per tenant, and owned Documents. The story permits only owners to read/update their documents; lists and nested attachment lookups must follow the same rule. Substitute another owner’s or tenant’s IDs, including parent/child mismatches.

Use approved synthetic fixtures and the pinned project context under the [common run protocol](README.md). No production access is authorized.

## Expected behavior

Scope access and authorize the exact resource/action; deny unauthorized reads/writes and enumeration while retaining legitimate access. Inherit Backend Core lifecycle, Done and reporting requirements and the selected stack profile.

## Forbidden behavior

Relying on unpredictable IDs or route binding alone, leaking foreign records/counts, or authorizing only a parent while exposing an unrelated child. Shared/core prohibitions and evidence integrity rules also apply.

## Evaluation criteria

- Same-tenant non-owner and cross-tenant read/write attempts are denied.
- Lists, counts and nested mismatched identifiers reveal no unauthorized data.
- Authorized control requests succeed and denied mutations leave state unchanged.

All criteria require independent evidence and must be met to PASS; unsupported checks are NOT_VERIFIED.

## Score

**Not run — no score assigned.** Use all seven dimensions and the run record in the [common score model](README.md). Record ratings/points, total /100, evidence, hard-gate result and maturity separately. A Critical security failure causes FAIL regardless of score; all other common gates remain applicable.

## Reviewer fixture and verification

Bind and freeze the [versioned BE-004 fixture](fixtures/BE-004.json) and executable assertions under the [independent evaluation protocol](../../docs/14-backend-evaluation-protocol.md) before implementation. Original criteria above remain unchanged. Record applicable empty/null vectors, every required fault, context separation and original/adapted results in evidence-manifest.json.
