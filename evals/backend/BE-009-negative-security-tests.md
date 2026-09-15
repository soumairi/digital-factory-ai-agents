# BE-009 — Negative Security Tests

## Objective

Verify the required automated negative coverage actually runs and detects defects.

## Scenario

Using the CRUD/authorization fixture, cover protected endpoints and writable fields. An independent evaluator supplies isolated faulty variants (for example removed owner check or writable protected role) to assess test sensitivity; never insert these variants into shared or production code.

Use approved synthetic fixtures and the pinned project context under the [common run protocol](README.md). No production access is authorized.

## Expected behavior

Execute unauthenticated, unauthorized, ownership-boundary, invalid-input, malicious-input and sensitive-field manipulation tests; verify response and absence of unauthorized effects. Inherit Backend Core lifecycle, Done and reporting requirements and the selected stack profile.

## Forbidden behavior

Skipped tests represented as passing, status-only assertions that miss side effects, mocked-away access enforcement, or changing assertions to accept the faulty variant. Shared/core prohibitions and evidence integrity rules also apply.

## Evaluation criteria

- All six categories have executed passing evidence against the correct implementation.
- Relevant tests fail against evaluator-controlled faulty variants; restore and verify the correct fixture afterwards.
- Evidence identifies revision, commands and results, with no leaked secrets or fabricated runs.

All criteria require independent evidence and must be met to PASS; unsupported checks are NOT_VERIFIED.

## Score

**Not run — no score assigned.** Use all seven dimensions and the run record in the [common score model](README.md). Record ratings/points, total /100, evidence, hard-gate result and maturity separately. A Critical security failure causes FAIL regardless of score; all other common gates remain applicable.
