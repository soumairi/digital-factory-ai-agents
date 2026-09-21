# BE-006 test results

Own tests and original first-attempt/failure logs: implementer-tests/. Independent execution commands, cwd, exit codes, log/JUnit hashes and counts: ../../reviews/BE-006/execution-result.json. Tests were run in disposable synthetic SQLite workspaces against the actual candidate, calibration_only=false.

| Independent clean test | Assertions |
|---|---:|
| test_BE006_success_shortage_rollback_and_repeat | 19 |
| test_BE006_quantity_normalization_and_persistence | 42 |

Unique clean total: 2 tests / 61 assertions; errors 0, skipped 0. Per-criterion mappings in evaluator-review.json overlap these methods and must not be added together. Clean rerun and fresh workspace repeat: PASS / PASS.

| Eval | Fault | Expected | Actual | Result |
|---|---|---|---|---|
| BE-006 | BE-006-F1 | FAIL | FAIL | PASS |
| BE-006 | BE-006-F2 | FAIL | FAIL | PASS |

Every detected mutant failed intended assertions with zero infrastructure errors/skips; clean candidate and test bytes remained unchanged. Preserved mutant source manifests and changed source live under ../../reviews/BE-006/. BE-006 additionally records genuine two-process SQLite race evidence where applicable. Fault failures are expected detections, not candidate case failures.
