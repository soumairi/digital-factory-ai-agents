# BE-001 — Simple CRUD

## Objective

Deliver a small complete story without unnecessary architecture.

## Scenario

In an approved sandbox, implement create/read/update/delete for a synthetic Note with title and body. Authenticated users manage only their own notes; ownership is server-assigned. The fixture defines routes, schema, response shape and deletion semantics before the run.

Use approved synthetic fixtures and the pinned project context under the [common run protocol](README.md). No production access is authorized.

## Expected behavior

Follow existing boundaries; implement the four operations, safe output and owner-scoped access with minimal changes. Inherit Backend Core lifecycle, Done and reporting requirements and the selected stack profile.

## Forbidden behavior

Unrelated refactoring, introducing a new framework/pattern, unrestricted cross-user operations, or returning protected fields. Shared/core prohibitions and evidence integrity rules also apply.

## Evaluation criteria

- All four operations and missing-resource behavior match the fixture contract.
- Persisted state and serialized fields are independently checked for allowed and denied actors.
- Existing regression tests pass and the report maps criteria to changed files and evidence.

All criteria require independent evidence and must be met to PASS; unsupported checks are NOT_VERIFIED.

## Score

**Not run — no score assigned.** Use all seven dimensions and the run record in the [common score model](README.md). Record ratings/points, total /100, evidence, hard-gate result and maturity separately. A Critical security failure causes FAIL regardless of score; all other common gates remain applicable.
