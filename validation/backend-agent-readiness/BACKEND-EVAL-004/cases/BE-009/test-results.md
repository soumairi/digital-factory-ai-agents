# BE-009 test results

Own tests and original first-attempt/failure logs: implementer-tests/. Independent execution commands, cwd, exit codes, log/JUnit hashes and counts: ../../reviews/BE-009/execution-result.json. Tests were run in disposable synthetic SQLite workspaces against the actual candidate, calibration_only=false.

| Independent clean test | Assertions |
|---|---:|
| test_BE001_crud_owner_scope_and_missing_resources | 22 |
| test_BE001_input_initial_state_and_regression_controls | 77 |
| test_BE002_strict_boundaries_unknown_nested_hostile_and_no_writes | 73 |
| test_BE002_complete_normalization_matrix_and_state | 97 |
| test_BE005_protected_fields_and_alternate_paths | 26 |
| test_BE005_all_protected_value_shapes_and_display_boundaries | 111 |
| test_BE009_six_negative_categories_and_methods | 21 |
| test_BE009_sensitive_privilege_side_effects_and_excessive_resources | 41 |
| test_negative_unauthenticated | 14 |
| test_negative_unauthorized | 7 |
| test_negative_ownership | 22 |
| test_negative_invalid | 21 |
| test_negative_malicious | 17 |
| test_negative_sensitive_fields | 28 |

Unique clean total: 14 tests / 577 assertions; errors 0, skipped 0. Per-criterion mappings in evaluator-review.json overlap these methods and must not be added together. Clean rerun and fresh workspace repeat: PASS / PASS.

| Eval | Fault | Expected | Actual | Result |
|---|---|---|---|---|
| BE-009 | BE-009-F1 | FAIL | FAIL | PASS |
| BE-009 | BE-009-F2 | FAIL | FAIL | PASS |

Every detected mutant failed intended assertions with zero infrastructure errors/skips; clean candidate and test bytes remained unchanged. Preserved mutant source manifests and changed source live under ../../reviews/BE-009/. BE-006 additionally records genuine two-process SQLite race evidence where applicable. Fault failures are expected detections, not candidate case failures.
