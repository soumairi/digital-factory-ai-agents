# Laravel adapter asset validation

Foundation remains **0.6.0**. Adapter bundle **1.0.0** contains executable assets for all nine original cases. This is adapter calibration against a separate known-good application, not a Backend Agent campaign, Release Candidate or independent review. The author did not perform the future review; REVIEW.md is the handoff.

| Eval | Setup | Clean | Fault Detection | Cleanup | Repeatable | Status |
|---|---|---|---|---|---|---|
| BE-001 | PASS | PASS (54 tests / 598 assertions) | PASS (1/1) | PASS | PASS | READY |
| BE-002 | PASS | PASS (2 tests / 170 assertions) | PASS (3/3) | PASS | PASS | READY |
| BE-003 | PASS | PASS (2 tests / 58 assertions) | PASS (1/1) | PASS | PASS | READY |
| BE-004 | PASS | PASS (2 tests / 150 assertions) | PASS (2/2) | PASS | PASS | READY |
| BE-005 | PASS | PASS (2 tests / 137 assertions) | PASS (1/1) | PASS | PASS | READY |
| BE-006 | PASS | PASS (2 tests / 61 assertions) | PASS (2/2) | PASS | PASS | READY |
| BE-007 | PASS | PASS (2 tests / 116 assertions) | PASS (3/3) | PASS | PASS | READY |
| BE-008 | PASS | PASS (2 tests / 220 assertions) | PASS (1/1) | PASS | PASS | READY |
| BE-009 | PASS | PASS (14 tests / 502 assertions) | PASS (2/2) | PASS | PASS | READY |

| Eval | Fault ID | Expected Clean | Actual Fault | Detection |
|---|---|---|---|---|
| BE-001 | BE-001-F1 | PASS | FAIL | PASS — 2 assertion failures, 0 errors |
| BE-002 | BE-002-F1 | PASS | FAIL | PASS — 2 assertion failures, 0 errors |
| BE-002 | BE-002-F2 | PASS | FAIL | PASS — 2 assertion failures, 0 errors |
| BE-002 | BE-002-F3 | PASS | FAIL | PASS — 2 assertion failures, 0 errors |
| BE-003 | BE-003-F1 | PASS | FAIL | PASS — 2 assertion failures, 0 errors |
| BE-004 | BE-004-F1 | PASS | FAIL | PASS — 1 assertion failures, 0 errors |
| BE-004 | BE-004-F2 | PASS | FAIL | PASS — 1 assertion failures, 0 errors |
| BE-005 | BE-005-F1 | PASS | FAIL | PASS — 2 assertion failures, 0 errors |
| BE-006 | BE-006-F1 | PASS | FAIL | PASS — 1 assertion failures, 0 errors |
| BE-006 | BE-006-F2 | PASS | FAIL | PASS — 1 assertion failures, 0 errors |
| BE-007 | BE-007-F1 | PASS | FAIL | PASS — 1 assertion failures, 0 errors |
| BE-007 | BE-007-F2 | PASS | FAIL | PASS — 2 assertion failures, 0 errors |
| BE-007 | BE-007-F3 | PASS | FAIL | PASS — 2 assertion failures, 0 errors |
| BE-008 | BE-008-F1 | PASS | FAIL | PASS — 1 assertion failures, 0 errors |
| BE-009 | BE-009-F1 | PASS | FAIL | PASS — 3 assertion failures, 0 errors |
| BE-009 | BE-009-F2 | PASS | FAIL | PASS — 4 assertion failures, 0 errors |

## Evidence and reproducibility

Authoritative evidence is release-calibration/ plus results.json. Every clean/fault result's log and JUnit hashes were verified against retained files; baseline and restored clean outputs have separate names. All runs used frozen bundle SHA-256 `d592ba263d82a988774f9c22e52d98b20f1ffa95d7e0f7a8aabd4203e6caceed`. Adapter fixture/verification hashes and full asset inventory match manifest.json/checksums.json. Source and tests remain unchanged under mutation; mutant source lives only in isolated copies which were removed. Initial and repeat setup targets were confirmed absent after cleanup. Five real two-process SQLite races execute each time BE-006 clean verification runs.

Commands: `python3 -B evals/backend/adapters/laravel/selftest.py --vendor /private/tmp/backend-eval-001-0v7ydh55/app/vendor --output validation/laravel-adapter-build/release-calibration`; framework checks: `python3 -B -m unittest discover -s tests/adapters -v` and `python3 -B -m unittest discover -s tests/evals -v`. Selftest refuses existing evidence destinations; choose a new output directory to reproduce. Exact PHP commands, temporary paths, JUnit outcomes and hashes are in the results and case evidence directories.

Seven adapter framework tests and fifteen hardened evaluation-framework regression tests pass. PostgreSQL support is a private socket-only BE-006 success/rollback/shortage probe, but validation is **NOT EXECUTED**: the checked local toolchain lacks postgres. See postgresql-validation.json. No existing database service, real credentials, production target or cloud resource was used. PostgreSQL concurrency/N+1 claims are not made.

All 339 historical files across BACKEND-EVAL-001 and002 retain identical bytes and inventory. Their original conclusions remain0 PASS/0 FAIL/9 PARTIAL and0 executed/9 NOT RUN. Neither campaign runner was rerun and no third campaign was started. Original fixture objectives/criteria are unchanged; new tests implement and strengthen coverage of the already-frozen definitions.

Development attempts and evidence-routing/log-retention corrections are preserved as diagnostics (build-tooling-note.md and coverage-refinement.md). Only release-calibration/ is used for the final READY decision; its records include calibration_only=true. No expectations were weakened to force a clean pass.

## Limits and review handoff

1. Independent evaluator ownership/adoption, L1 context provenance, semantic architecture/diff review, Security/Audit and human approval remain future campaign gates. READY is executability, not case PASS or Backend readiness.
2. PostgreSQL validation was not available; actual executed database behavior is SQLite-only. Logical data, IDs and expected outcomes are deterministic; cryptographic password salts, clock fields and test durations need not be byte-identical.
3. Bindings/runtime/vendor are deliberately pinned. Alternate candidate interfaces or mutations need reviewer-approved rebinding. Approved application exports are supported; this is not an OS/network sandbox for hostile PHP. Stronger external containment must be supplied before executing untrusted code.
