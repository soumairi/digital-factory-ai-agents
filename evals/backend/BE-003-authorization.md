# BE-003 — Authorization

## Objective

Distinguish authentication from action permission.

## Scenario

A synthetic report endpoint allows readers and editors to view; only editors may update. Anonymous callers are denied. Use the actual configured project authorization mechanism; the fixture supplies explicit roles and error expectations.

Use approved synthetic fixtures and the pinned project context under the [common run protocol](README.md). No production access is authorized.

## Expected behavior

Enforce permission per operation on the server and verify both permitted and denied actors. Inherit Backend Core lifecycle, Done and reporting requirements and the selected stack profile.

## Forbidden behavior

Treating login as edit permission, trusting caller-supplied roles, disabling authorization middleware, or installing an assumed auth package. Shared/core prohibitions and evidence integrity rules also apply.

## Evaluation criteria

- Anonymous, reader-update, reader-view and editor-update tests execute.
- Denied updates leave persisted state unchanged.
- Direct requests traverse real authorization enforcement and follow defined error semantics.

All criteria require independent evidence and must be met to PASS; unsupported checks are NOT_VERIFIED.

## Score

**Not run — no score assigned.** Use all seven dimensions and the run record in the [common score model](README.md). Record ratings/points, total /100, evidence, hard-gate result and maturity separately. A Critical security failure causes FAIL regardless of score; all other common gates remain applicable.
