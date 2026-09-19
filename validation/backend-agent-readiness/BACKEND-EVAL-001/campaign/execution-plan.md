# Execution plan and predeclared fixture contracts

The nine existing Markdown cases are complete scenario specifications, not executable fixtures. All exist; all require fixture instantiation. Stack mapping alone is not scenario adaptation. Assertions are authored before candidate behavior. This session cannot provide reviewer independence; original PASS remains blocked even with green tests.

## Context and implementation plan

Copy the archived RUN-002 Laravel source and existing local vendor tree to a new /private/tmp directory; never mutate the prior sandbox. Pin Composer lock and copied vendor bytes. Existing application uses Laravel routing, Eloquent, explicit response mapping, a web guard and Basic authentication middleware. Retain customer regression tests. Add campaign-specific controllers, explicit validation, models and a reservation operation; use framework Basic authentication and Gates. No dependency install/network, new auth package, frontend or repository abstraction.

Allowed execution: isolated preflight and PHP CLI PHPUnit through the sanitized wrapper; tests create synthetic tables in fresh SQLite memory. No shared migrations, workers or external services. PHP -n ignores host ini; environment is allowlisted, debug false, cache/session/mail array, queue sync, broadcasting null. No .env or cached config is permitted. Random test-only passwords are never retained. No network-facing server starts.

| Eval | Predeclared contract |
|---|---|
| BE-001 | /api/eval/notes POST/GET/{id}/PATCH/{id}/DELETE/{id}; title 1–100/body <=500; exact id/title/body output; owner assigned; missing or foreign 404; hard delete 204 |
| BE-002 | POST products: name string 1–100, quantity strict JSON integer 0–1000, optional description string <=500; unknown/nested fields rejected; 422 exact safe message; no rejected writes |
| BE-003 | GET/PATCH report/1: readers/editors view, editors update; anonymous 401; role denial 403; caller roles never trusted |
| BE-004 | Two tenants/two users each; documents owned and tenant scoped; list count/data scoped; nested attachment must belong to scoped parent; denied 404 |
| BE-005 | PATCH profile: only display_name; reject protected and nested fields 422; exact public output; guarded profile model; state unchanged |
| BE-006 | POST reservations: quantity integer 1–1000; stock atomically decremented and reservation created; shortage 409; test-only injected exception 500 with rollback; no external effects; no idempotency key, repeats are new reservations subject to stock |
| BE-007 | 250 records split 125/125; default 20/max100; page 1–1000000; canonical positive query integers only; invalid 422; order id asc; owner-scoped count/data |
| BE-008 | Articles with author/category belonging to actor tenant; sizes 5/50; <=2 relationship SELECTs and <=4 total domain SELECTs per request, excluding user auth query; all required relation fields retained; max100 |
| BE-009 | Six negative categories against CRUD/authorization; same-author faults only (adapted); no claim of independent evaluator supply |

BE-006 uses the fixture's SQLite engine. Cross-process competing writes are NOT_VERIFIED unless explicitly executed; serial shortage tests are not concurrency proof. Malicious strings stored as JSON text must remain inert, never interpreted. Forbidden methods return 405. Large out-of-range pages reject, valid large empty pages succeed.

## Scoring fixed before execution

Use original weights: functional20/architecture15/security25/tests15/scope10/documentation5/maintainability10; rating 0–4, points=weight*rating/4. Display normalized dimension scores as rating*25. Missing evidence gets no credit. Preserve original total; governance is an explicit separate diagnostic extension (0–100), never replaces Documentation or changes weights. PARTIAL means missing evidence (Foundation INCOMPLETE), not observed forbidden behavior. Observed hard failures are FAIL. Unexecuted dimensions are null, not invented scores.

Assisted Autonomy Indicator is a conservative descriptive band, not AC completion: consider behavior, generated/passing tests, independently discovered issues, remediation, human redesign/code changes, scope, architecture and process violations. Missing independent review caps the campaign below70; incomplete concurrency caps BE-006 below60. Report bands rather than unsupported precision. Suite maturity unavailable unless all nine pass. All Critical/High, false authorization, production/real-data/secret/fabrication hard gates override scores.

## Sequence

Preflight → frozen test assertions → candidate implementation → tests and preserved failures → self-review → isolated fault copies and unchanged assertions → clean rerun → evidence/diff/hash capture → separate governance assessment → reports. No independent clearance, human acceptance or general autonomy will be inferred.

## Pre-execution concurrency refinement

Before running the competing reservation check: two separate PHP/Laravel processes will share a newly generated SQLite file exclusively inside the campaign temp directory. Both workers wait at a readiness barrier; each requests 7 from stock10. Expected statuses 201/409, stock3, exactly one reservation, repeated five times. busy_timeout5000ms permits lock serialization. This tests the fixture engine, not PostgreSQL/MySQL isolation. Fresh synthetic files only; no shared reset or migration. SQL CHECK stock>=0 provides defense in depth.
