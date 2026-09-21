# BE-007 test results

Own tests and original first-attempt/failure logs: implementer-tests/. Independent execution commands, cwd, exit codes, log/JUnit hashes and counts: ../../reviews/BE-007/execution-result.json. Tests were run in disposable synthetic SQLite workspaces against the actual candidate, calibration_only=false.

| Independent clean test | Assertions |
|---|---:|
| test_BE007_pagination_traversal_scope_and_resource_limits | 35 |
| test_BE007_raw_null_whitespace_types_and_metadata | 81 |
| test_BE007_bounded_database_reads | 46 |

Unique clean total: 3 tests / 162 assertions; errors 0, skipped 0. Per-criterion mappings in evaluator-review.json overlap these methods and must not be added together. Clean rerun and fresh workspace repeat: PASS / PASS.

| Eval | Fault | Expected | Actual | Result |
|---|---|---|---|---|
| BE-007 | BE-007-F1 | FAIL | FAIL | PASS |
| BE-007 | BE-007-F2 | FAIL | FAIL | PASS |
| BE-007 | BE-007-F3 | FAIL | FAIL | PASS |
| BE-007 | BE-007-F4 | FAIL | FAIL | PASS |

Every detected mutant failed intended assertions with zero infrastructure errors/skips; clean candidate and test bytes remained unchanged. Preserved mutant source manifests and changed source live under ../../reviews/BE-007/. BE-006 additionally records genuine two-process SQLite race evidence where applicable. Fault failures are expected detections, not candidate case failures.
