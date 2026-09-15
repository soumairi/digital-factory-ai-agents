# BE-002 — Validation

## Objective

Verify strict server-side request/schema handling.

## Scenario

A synthetic Product accepts a required name (1–100 characters), integer quantity (0–1000) and optional description (at most 500 characters). The fixture requires rejection of unexpected top-level and nested keys and defines invalid response semantics.

Use approved synthetic fixtures and the pinned project context under the [common run protocol](README.md). No production access is authorized.

## Expected behavior

Validate on the server; accept boundary-valid inputs and reject invalid types, ranges, missing and unknown fields without writes. Inherit Backend Core lifecycle, Done and reporting requirements and the selected stack profile.

## Forbidden behavior

Frontend-only checks, silent coercion contrary to the schema, accepting forbidden keys, or persistence before validation. Shared/core prohibitions and evidence integrity rules also apply.

## Evaluation criteria

- Automated tests cover valid boundaries, missing fields, wrong types, overlong/out-of-range values and unknown keys.
- Malformed/hostile input is safely handled and response errors contain no internal secrets.
- Rejected requests produce no database changes.

All criteria require independent evidence and must be met to PASS; unsupported checks are NOT_VERIFIED.

## Score

**Not run — no score assigned.** Use all seven dimensions and the run record in the [common score model](README.md). Record ratings/points, total /100, evidence, hard-gate result and maturity separately. A Critical security failure causes FAIL regardless of score; all other common gates remain applicable.
