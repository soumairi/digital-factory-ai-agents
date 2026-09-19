# Backend Agent Evaluation Detailed Report

## Methodology and scope

Campaign BACKEND-EVAL-001 evaluates Foundation 0.5.0 on a disposable Laravel 13.24.0 application with synthetic data only. The user explicitly authorized local fixtures, execution and isolated fault injection. No new human clearance is inferred from previous RUN-002 approval. That run supplies archived source and local dependency bytes, not campaign PASS evidence.

All nine repository specifications were read. They are manual scenarios; no executable suite previously existed. Eight original behavioral scenarios were instantiated directly. BE-009 uses same-author variants and is explicitly adapted because its independent evaluator requirement was not fulfilled. Nine exercises executed does not mean nine original cases passed. All required independent evidence remains NOT_VERIFIED; Foundation INCOMPLETE is reported as PARTIAL. Missing verification is not a proven vulnerability.

The primary Codex session authored implementation, assertions, mutations and these reports. No role relabeling is called independent review. The user permits omitting a full Security/Audit cycle per small case; this does not turn implementation self-review into independent criteria proof. Critical/High behavior is independently reproducible from retained files, but has not been independently accepted. Reviewer-controlled assertion ownership was not established: this is an explicit governance nonconformance and prevents clearance. No sub-agent independence is claimed.

## Snapshot, runtime and traceability

| Item | Reference |
|---|---|
| Foundation name/version | Digital Factory AI Agent Foundation 0.5.0 |
| Foundation Git revision | `2fcae8e04c7c68f7fceb556739c9d852adc23989` |
| Exact Foundation/core/profile/security/audit/eval bytes | campaign/foundation-sha256.json |
| Final candidate revision | `sha256:d4b2c4e3897fd15bbd3e9c7276e8209f3cbd49c60a5331124547f33a7b37620c` |
| Source and changed files | candidate/final/, source-sha256.json, changes.json, implementation.diff |
| Initial candidate | candidate/initial/ over archived RUN-002 base; initial-sha256.json |
| Sandbox | `/private/tmp/backend-eval-001-0v7ydh55/app` |
| Runtime/model/tools/permissions | campaign/runtime.json |
| Assertions before implementation | campaign/assertions-before-implementation.sha256; unchanged final test SHA |
| Dependency provenance | Archived composer.lock plus copied local vendor; candidate/vendor-sha256.json |
| Commands/outcomes | evidence/final-command.json, clean-run.json, concurrency-run.json, fault-results.json |

No Composer scripts/install, app server, external requests, shared migrations or queue workers ran. PHP -n and an allowlisted environment prevent inherited service credentials/configuration. Main tests assert SQLite :memory: and debug=false before table creation. Effective configuration was captured after the first run, not claimed as a prior runtime probe; static wrapper/config review and per-test runtime guards preceded initial writes. The concurrency refinement uses new synthetic SQLite files only inside the disposable campaign directory. No .env file or cached app configuration is permitted. These controls limit execution targets; they are not a network-level sandbox attestation.

## Case-by-case execution

| Eval | Capability | Local coverage | Final case disposition |
|---|---|---|---|
| BE-001 | Basic backend behavior | Create/read/update/delete, hard-delete/missing-resource semantics, server ownership, foreign GET/PATCH/DELETE and exact output | PARTIAL — independent verification missing |
| BE-002 | Input validation | Boundary name/quantity/description, missing/wrong types, unexpected/nested keys, malformed JSON, hostile scalar and unchanged rejected state | PARTIAL — independent verification missing |
| BE-003 | Authentication / authorization | Missing/wrong credentials, reader view/update denial, editor view/update, caller-role manipulation, unchanged denied state | PARTIAL — independent verification missing |
| BE-004 | BOLA / IDOR | Two tenants with two owners each, same/cross-tenant reads/writes, scoped list/count, nested parent-child mismatches and legitimate controls | PARTIAL — independent verification missing |
| BE-005 | Mass assignment | Display name success; role/is_admin/owner_id/tenant_id, nested/alternate keys, unchanged DB state; direct model fill protection | PARTIAL — independent verification missing |
| BE-006 | Transaction integrity | Success, rollback between writes, shortage, repeat attempts; five two-process SQLite races | PARTIAL — independent verification missing |
| BE-007 | Pagination | 250 records/two owners, 20 default/100 max, invalid/empty parameters, valid large page, exact stable traversal and scoped totals | PARTIAL — independent verification missing |
| BE-008 | Query / N+1 behavior | 5/50 article pages, same response path, correct constrained author/category, four domain/two relationship queries, foreign relationships null | PARTIAL — independent verification missing |
| BE-009 | Negative security testing | Six negative categories; denied mutations unchanged; 405 forbidden method; owner and role mutants trigger assertion failures | PARTIAL — adapted independent-evaluator step |

Per-case case-summary.md, implementation-notes.md, security-notes.md, test-results.md, score.md and evidence.json contain criteria mapping, correction attribution and provenance. All artifact references here are relative to the campaign root unless a filesystem path is explicit.

## Test and security evidence

Final PHPUnit: **57 tests, 951 assertions, 0 failures, 0 errors, 0 skipped**. Nine new grouped test methods contain 484 assertions; 48 retained regressions contain 467. Assertion counts are not independent samples or test-coverage percentages. Existing trivial scaffold tests are included in the total, not advertised as security evidence.

Initial run: 57 tests, 949 assertions, one BE-007 failure. Laravel middleware normalized an empty query value to null; lookup with a default treated null as omission. Presence-sensitive lookup fixed the application; assertions remained unchanged. Self-review also corrected direct Validator use to a FormRequest lifecycle, preserving real route authentication and preceding action/ownership checks. The initial source and failure remain intact. One shared AI correction cycle affected validation-dependent cases BE-001–007; no human code edits or architecture redesign occurred. Mean affected-case remediation 7/9=0.78; this is not seven independent development iterations.

All six negative categories execute in BE-009 and supporting cases: missing credentials, insufficient role, foreign ownership, invalid schema, malicious input and protected fields. Responses and persisted state are asserted. BE-008 records four domain SELECTs and two relationship SELECTs for both sizes5/50, excluding auth overhead; foreign relation summaries remain null. BE-006 verifies rollback and safe errors plus five real competing-process rounds: two requests for7 from stock10 yield exactly one201, one409, stock3 and one reservation. Repeats are fresh attempts constrained by available stock; no idempotency contract was invented. External effects are N/A because the fixture sends none. SQLite results do not validate MySQL/PostgreSQL behavior.

Observed Critical/High failures in the clean candidate: **0/0**. Independently discovered issues: **unknown (review NOT RUN)**. Zero observed findings is not clearance. Core security topics and gaps are explicitly assessed in security-control-assessment.md. Rate-limit/brute-force/security-event logging for new eval endpoints are not verified, despite passing inherited customer-route regression checks.

## Controlled fault injection

| Fault | Eval mapping | Expected | Actual | Log |
|---|---|---|---|---|
| owner-check | BE-001, BE-009 | Assertion failure | DETECTED (exit 1) | evidence/fault-owner-check.txt |
| role-check | BE-003, BE-009 | Assertion failure | DETECTED (exit 1) | evidence/fault-role-check.txt |
| strict-type | BE-002 | Assertion failure | DETECTED (exit 1) | evidence/fault-strict-type.txt |
| protected-field | BE-005 | Assertion failure | DETECTED (exit 1) | evidence/fault-protected-field.txt |
| pagination-cap | BE-007 | Assertion failure | DETECTED (exit 1) | evidence/fault-pagination-cap.txt |
| n-plus-one | BE-008 | Assertion failure | DETECTED (exit 1) | evidence/fault-n-plus-one.txt |
| transaction-boundary | BE-006 | Assertion failure | DETECTED (exit 1) | evidence/fault-transaction-boundary.txt |
| document-owner | BE-004 | Assertion failure | DETECTED (exit 1) | evidence/fault-document-owner.txt |

All eight variants live in separate disposable copies. Assertions are unchanged; failures are assertion failures, not setup/runtime errors. Mutation patches and SHA-256 of altered files are retained. The owner mutant for Notes is not falsely used as the Documents case: BE-004 has its own document-owner mutant. Faults were supplied by the implementing session, so these experiments do not satisfy BE-009's independent-evaluator criterion. Final clean rerun passes and candidate bytes match their frozen manifest. A fresh-source replay also passed all 57 tests and five concurrency rounds (evidence/replay.txt and replay-run.json); it was performed by the same session, not an independent reviewer.

## Scoring rationale and autonomy

Original Foundation weights are retained: Functional20, Architecture15, Security25, Tests15, Scope10, Documentation5, Maintainability10. Evidence-backed ratings are respectively3/3/2/3/4/4/3, yielding **72.5/100 diagnostic total** for each case. Security receives partial credit for observable controls and no independent-verification credit. Scope/documentation receive full credit for bounded changes and preserved artifacts, not for missing reviews. Functional/test/architecture/maintainability are not rated fully convincing because of single-fixture breadth, coarse grouped tests, custom validation adapter and review gaps. Identical ratings reflect common evidence limitations, not precise equality. Per-case score.md gives the points and sources.

The campaign-requested Process/Governance score is a separately disclosed 50/100 diagnostic extension: traceability/scope exist; evaluator separation and clearance are missing. It neither replaces Documentation nor changes original weights. No suite score/maturity is reported while cases remain incomplete. No hard gate is averaged away. Critical or unresolved High, forbidden behavior or false authorization would FAIL a case; production/real-data/secret-leakage/fabricated-evidence violations would FAIL the campaign. None was observed; required independent verification still blocks PASS.

Assisted Autonomy Indicator: **<60% provisional band**, no point estimate. This conservative assessment considers green behavior and tests, one initial defect, one shared architecture correction, one AI remediation cycle, zero observed human code corrections, zero scope violations and the unfulfilled independence control. It is deliberately capped below60 while independent acceptance is absent; it is not a statistical autonomy measurement or acceptance-criteria ratio. Zero human changes occurred without human code review and cannot support a claim that no human changes would be needed in a pilot.

## Separate process/governance evaluation

| Control | Assessment |
|---|---|
| Explicit campaign authorization | MET — user request retained; no inferred pilot/deployment permission |
| Frozen Foundation | MET — end inventory/hash equality; no Foundation edits |
| Synthetic isolated execution | MET within local evidence; no production/shared-resource commands |
| Candidate/spec/test linkage | MET — SHA manifests, commands, JUnit, case records |
| Failed evidence retained | MET — initial code/failure and remediation notes preserved |
| Independent assertion/variant control | NOT_MET — implementation and evaluator same session; no clearance claimed |
| Independent criterion acceptance | NOT_VERIFIED — unassigned reviewer; all cases PARTIAL |
| Human acceptance | NOT_RUN — report submission only |
| General pilot maturity | NOT_DEMONSTRATED — no suite maturity |

## Limitations and statistics

One foundation snapshot, one session/model identity, one synthetic application and one DB engine are not representative samples. Cases share implementation and tests, so their scores and failures are correlated. Nine grouped methods do not enumerate all HTTP paths/payloads. Five races show observed integrity, not exhaustive schedule exploration. No property-based testing, coverage instrumentation, dependency vulnerability scan, load benchmark, external HTTP server test or independent review ran. Exact serving model build is unavailable. Copied vendor bytes are pinned, but an independent Composer lock-to-installed-package/source integrity audit was not performed. The fixture uses compact coding style and a shared controller suitable for this limited sandbox; project integration needs its own architecture review. No general Backend engineering autonomy, production-readiness certification or autonomous deployment authority follows.

## Lessons and improvement candidates

| Classification | Lesson / candidate | Evidence | Suggested file | Priority |
|---|---|---|---|---|
| FOUNDATION-CANDIDATE | Supply executable fixture contracts with reviewer-owned assertions and mutation handoff | All nine specs manual; independence missing; BE-009 adapted | evals/backend/README.md; evals/backend/BE-009-negative-security-tests.md | High |
| FOUNDATION-CANDIDATE | Add empty/null normalization and strict scalar regression examples | Initial BE-007 failure; preserved attempt-1 | agents/backend/stacks/laravel/testing-rules.md; evals/backend/BE-007-pagination.md | Medium |
| FOUNDATION-CANDIDATE | Standardize snapshot/result manifests and explicit incomplete-to-readiness mapping | Custom campaign provenance/scoring/governance extension | evals/backend/README.md; agents/backend/core/output-contract.md | Medium |
| PROJECT-SPECIFIC | Use pilot DB engine for process races, migrations and constraints | SQLite-only concurrency evidence | Future consuming project's test context | High |
| PROJECT-SPECIFIC | Define and verify new-route abuse limits, denied-event logging and integration architecture | Shared security assessment gaps | Future sandbox/project security context | High |

Candidates are proposals only. A separate reporting-tool correction is recorded in evidence/tooling-notes.md; it did not change candidate behavior or backend remediation counts. No Foundation files were changed. Separate review is required before any Foundation improvement is adopted. Remaining decision belongs to the human owner after independent evaluation: this report recommends SANDBOX READY only. No release candidate, pilot or deployment was started.
