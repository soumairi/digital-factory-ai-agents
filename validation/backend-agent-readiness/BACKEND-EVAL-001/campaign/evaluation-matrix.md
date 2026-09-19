# Evaluation inventory and matrix

All nine expected IDs exist. No missing specification or invented ID. None is runnable as-is: each is a manual scenario requiring a concrete fixture and assertions. No ambiguous original behavior was reconstructed. Missing reviewer assignment is a governance gap, not an ambiguity in the specification.

| Eval ID | Title | Exists | Runnable as-is | Requires adaptation |
|---|---|---|---|---|
| BE-001 | Simple CRUD | YES | NO — Markdown specification | Fixture required; No scenario change; Laravel instantiation |
| BE-002 | Validation | YES | NO — Markdown specification | Fixture required; No scenario change; Laravel instantiation |
| BE-003 | Authorization | YES | NO — Markdown specification | Fixture required; No scenario change; Laravel instantiation |
| BE-004 | BOLA / IDOR | YES | NO — Markdown specification | Fixture required; No scenario change; Laravel instantiation |
| BE-005 | Mass Assignment | YES | NO — Markdown specification | Fixture required; No scenario change; Laravel instantiation |
| BE-006 | Transaction | YES | NO — Markdown specification | Fixture required; No scenario change; Laravel instantiation |
| BE-007 | Pagination | YES | NO — Markdown specification | Fixture required; No scenario change; Laravel instantiation |
| BE-008 | N+1 Prevention | YES | NO — Markdown specification | Fixture required; No scenario change; Laravel instantiation |
| BE-009 | Negative Security Tests | YES | NO — Markdown specification | Fixture required; YES — independence adapted |

| Eval ID | Capability | Original Case | Adaptation Needed | Execution Status |
|---|---|---|---|---|
| BE-001 | Basic backend behavior | BE-001-simple-crud.md | NO — concrete Laravel fixture required | EXECUTED / PARTIAL |
| BE-002 | Input validation | BE-002-validation.md | NO — concrete Laravel fixture required | EXECUTED / PARTIAL |
| BE-003 | Authentication / authorization | BE-003-authorization.md | NO — concrete Laravel fixture required | EXECUTED / PARTIAL |
| BE-004 | BOLA / IDOR | BE-004-bola-idor.md | NO — concrete Laravel fixture required | EXECUTED / PARTIAL |
| BE-005 | Mass assignment | BE-005-mass-assignment.md | NO — concrete Laravel fixture required | EXECUTED / PARTIAL |
| BE-006 | Transaction integrity | BE-006-transaction.md | NO — concrete Laravel fixture required | EXECUTED / PARTIAL |
| BE-007 | Pagination | BE-007-pagination.md | NO — concrete Laravel fixture required | EXECUTED / PARTIAL |
| BE-008 | Query / N+1 behavior | BE-008-n-plus-one.md | NO — concrete Laravel fixture required | EXECUTED / PARTIAL |
| BE-009 | Negative security testing | BE-009-negative-security-tests.md | YES — evaluator separation absent | EXECUTED / PARTIAL |

Eight original behavioral scenarios executed with verification gaps; one adapted BE-009 exercise executed. Thus 9 executed exercises, 0 fully verified original cases, 9 PARTIAL, 0 NOT RUN. BE-006 external effects are NOT APPLICABLE (no external effect exists); non-SQLite engines and independent evaluations are NOT RUN, not N/A. Scope/architecture/governance are assessed across every case rather than invented eval IDs.
