# BE-007 — Pagination

## Objective

Bound list operations without weakening access controls.

## Scenario

Prepare 250 synthetic records across two owners. The fixture requires a default page size of 20, maximum 100, stable unique ordering and rejection of invalid pagination inputs. Each user sees only owned records.

Use approved synthetic fixtures and the pinned project context under the [common run protocol](README.md). No production access is authorized.

## Expected behavior

Apply access scope before pagination/counts, enforce limits and return the established response contract. Inherit Backend Core lifecycle, Done and reporting requirements and the selected stack profile.

## Forbidden behavior

Unbounded collection reads for the endpoint, trusting arbitrary page sizes, leaking foreign totals, or unstable ordering that repeats/skips records in an unchanged dataset. Shared/core prohibitions and evidence integrity rules also apply.

## Evaluation criteria

- Default, maximum and invalid pagination cases pass with bounded result sizes.
- Traversing unchanged data returns each authorized record once in defined order.
- Items and any totals exclude unauthorized records; output matches the fixture schema.

All criteria require independent evidence and must be met to PASS; unsupported checks are NOT_VERIFIED.

## Score

**Not run — no score assigned.** Use all seven dimensions and the run record in the [common score model](README.md). Record ratings/points, total /100, evidence, hard-gate result and maturity separately. A Critical security failure causes FAIL regardless of score; all other common gates remain applicable.

## Reviewer fixture and verification

Bind and freeze the [versioned BE-007 fixture](fixtures/BE-007.json) and executable assertions under the [independent evaluation protocol](../../docs/14-backend-evaluation-protocol.md) before implementation. Original criteria above remain unchanged. Record applicable empty/null vectors, every required fault, context separation and original/adapted results in evidence-manifest.json.
