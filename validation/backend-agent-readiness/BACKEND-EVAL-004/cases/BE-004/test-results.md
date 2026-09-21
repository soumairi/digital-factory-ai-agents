# BE-004 test results

Own tests and original first-attempt/failure logs: implementer-tests/. Independent execution commands, cwd, exit codes, log/JUnit hashes and counts: ../../reviews/BE-004/execution-result.json. Tests were run in disposable synthetic SQLite workspaces against the actual candidate, calibration_only=false.

| Independent clean test | Assertions |
|---|---:|
| test_BE004_same_tenant_cross_tenant_nested_lists_and_unchanged_state | 107 |
| test_BE004_identifier_schema_and_protected_keys | 59 |

Unique clean total: 2 tests / 166 assertions; errors 0, skipped 0. Per-criterion mappings in evaluator-review.json overlap these methods and must not be added together. Clean rerun and fresh workspace repeat: PASS / PASS.

| Eval | Fault | Expected | Actual | Result |
|---|---|---|---|---|
| BE-004 | BE-004-F1 | FAIL | FAIL | PASS |
| BE-004 | BE-004-F2 | FAIL | FAIL | PASS |
| BE-004 | BE-004-F3 | FAIL | FAIL | PASS |

Every detected mutant failed intended assertions with zero infrastructure errors/skips; clean candidate and test bytes remained unchanged. Preserved mutant source manifests and changed source live under ../../reviews/BE-004/. BE-006 additionally records genuine two-process SQLite race evidence where applicable. Fault failures are expected detections, not candidate case failures.
