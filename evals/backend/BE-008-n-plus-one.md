# BE-008 — N+1 Prevention

## Objective

Prevent query growth caused by repeated relationship loading.

## Scenario

A list returns synthetic Articles with authorized author/category summaries. Prepare datasets yielding pages of 5 and 50 articles. Before the run, record the relevant query-count budget and measurement method for the same response path; separate fixed framework/authentication overhead.

Use approved synthetic fixtures and the pinned project context under the [common run protocol](README.md). No production access is authorized.

## Expected behavior

Use appropriate constrained eager loading or the existing equivalent; maintain safe serialization and pagination. Inherit Backend Core lifecycle, Done and reporting requirements and the selected stack profile.

## Forbidden behavior

One relationship query per row, loading all records to hide query counts, removing required response fields, or widening relationship visibility for speed. Shared/core prohibitions and evidence integrity rules also apply.

## Evaluation criteria

- Required related fields remain correct and authorized for both page sizes.
- Measured relationship query counts remain within the predeclared bounded budget rather than growing per row.
- Automated regression evidence covers query behavior and response correctness; retain selected-column/relationship keys needed by the ORM.

All criteria require independent evidence and must be met to PASS; unsupported checks are NOT_VERIFIED.

## Score

**Not run — no score assigned.** Use all seven dimensions and the run record in the [common score model](README.md). Record ratings/points, total /100, evidence, hard-gate result and maturity separately. A Critical security failure causes FAIL regardless of score; all other common gates remain applicable.
