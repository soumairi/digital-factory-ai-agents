# BE-001 test results

Own tests and original first-attempt/failure logs: implementer-tests/. Independent execution commands, cwd, exit codes, log/JUnit hashes and counts: ../../reviews/BE-001/execution-result.json. Tests were run in disposable synthetic SQLite workspaces against the actual candidate, calibration_only=false.

| Independent clean test | Assertions |
|---|---:|
| test_BE001_crud_owner_scope_and_missing_resources | 22 |
| test_BE001_input_initial_state_and_regression_controls | 77 |
| test_negative_unauthenticated | 5 |
| test_negative_unauthorized | 5 |
| test_negative_ownership | 6 |
| test_negative_invalid | 6 |
| test_negative_malicious | 6 |
| test_negative_sensitive_fields | 6 |
| test_created_note_is_owned_private_and_deletable | 15 |
| test_administrator_receives_exact_schema_and_default_pagination | 115 |
| test_missing_credentials_are_denied_before_customer_query | 9 |
| test_invalid_password_is_denied | 5 |
| test_unknown_identity_is_denied | 5 |
| test_previous_authentication_does_not_authorize_next_request | 6 |
| test_non_administrator_is_denied_before_customer_query | 7 |
| test_admin_flag_is_not_mass_assignable_and_defaults_false | 4 |
| test_second_page_has_stable_order_and_preserves_page_size | 9 |
| test_maximum_page_size_is_bounded | 6 |
| test_empty_collection_is_valid | 6 |
| test_maximum_page_is_valid_and_out_of_data_is_empty | 7 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #0 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #1 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #2 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #3 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #4 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #5 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #6 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #7 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #8 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #9 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #10 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #11 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #12 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #13 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #14 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #15 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #16 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #17 | 6 |
| test_invalid_pagination_is_rejected_without_customer_queries with data set #18 | 6 |
| test_hostile_or_protected_parameters_cannot_change_state with data set #0 | 7 |
| test_hostile_or_protected_parameters_cannot_change_state with data set #1 | 7 |
| test_hostile_or_protected_parameters_cannot_change_state with data set #2 | 7 |
| test_hostile_or_protected_parameters_cannot_change_state with data set #3 | 7 |
| test_hostile_or_protected_parameters_cannot_change_state with data set #4 | 7 |
| test_hostile_or_protected_parameters_cannot_change_state with data set #5 | 7 |
| test_hostile_or_protected_parameters_cannot_change_state with data set #6 | 7 |
| test_hostile_or_protected_parameters_cannot_change_state with data set #7 | 7 |
| test_hostile_or_protected_parameters_cannot_change_state with data set #8 | 7 |
| test_hostile_or_protected_parameters_cannot_change_state with data set #9 | 7 |
| test_get_body_is_rejected | 5 |
| test_rate_limit_precedes_authentication | 67 |
| test_denial_logs_have_no_request_or_credentials | 8 |
| test_customer_query_count_does_not_grow_with_page_size | 11 |
| test_cross_origin_access_is_not_enabled | 6 |
| test_write_method_is_not_available | 5 |

Unique clean total: 55 tests / 613 assertions; errors 0, skipped 0. Per-criterion mappings in evaluator-review.json overlap these methods and must not be added together. Clean rerun and fresh workspace repeat: PASS / PASS.

| Eval | Fault | Expected | Actual | Result |
|---|---|---|---|---|
| BE-001 | BE-001-F1 | FAIL | FAIL | PASS |

Every detected mutant failed intended assertions with zero infrastructure errors/skips; clean candidate and test bytes remained unchanged. Preserved mutant source manifests and changed source live under ../../reviews/BE-001/. BE-006 additionally records genuine two-process SQLite race evidence where applicable. Fault failures are expected detections, not candidate case failures.
