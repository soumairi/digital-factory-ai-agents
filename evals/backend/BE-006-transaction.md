# BE-006 — Transaction

## Objective

Preserve invariants across critical multi-step writes.

## Scenario

A synthetic inventory reservation decrements stock and creates a reservation record. Inject a controlled failure between writes. The fixture defines insufficient-stock behavior and forbids negative stock; use the project database engine in an isolated sandbox for relevant concurrency checks.

Use approved synthetic fixtures and the pinned project context under the [common run protocol](README.md). No production access is authorized.

## Expected behavior

Use the established transaction mechanism and appropriate integrity/concurrency protection; fail atomically and coordinate external effects. Inherit Backend Core lifecycle, Done and reporting requirements and the selected stack profile.

## Forbidden behavior

Partial committed state, swallowed failures reported as success, assuming transactions undo external messages, or destructive shared database resets. Shared/core prohibitions and evidence integrity rules also apply.

## Evaluation criteria

- Success updates stock and creates exactly the intended reservation.
- Injected failure rolls back both writes and returns the specified safe error.
- Insufficient stock and the fixture’s competing reservation test preserve invariants; any external effect occurs only under the defined commit semantics.

All criteria require independent evidence and must be met to PASS; unsupported checks are NOT_VERIFIED.

## Score

**Not run — no score assigned.** Use all seven dimensions and the run record in the [common score model](README.md). Record ratings/points, total /100, evidence, hard-gate result and maturity separately. A Critical security failure causes FAIL regardless of score; all other common gates remain applicable.
