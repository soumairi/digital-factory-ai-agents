# BE-007 Test Results

| Evidence | Result |
|---|---|
| Foundation | 0.5.0; campaign/foundation-sha256.json |
| Candidate | `sha256:d4b2c4e3897fd15bbd3e9c7276e8209f3cbd49c60a5331124547f33a7b37620c` |
| Sandbox | `/private/tmp/backend-eval-001-0v7ydh55/app` |
| Exact execution | evidence/final-command.json; campaign/run-evidence.py |
| Named test | `test_BE007_pagination_traversal_scope_and_resource_limits` |
| Final result | PASS, 35 assertions; evidence/final-junit.xml |
| Initial result | FAIL: empty per_page accepted; evidence/attempt-1.txt |
| Full regression run | 57 tests / 951 assertions / 0 failures / 0 errors / 0 skipped |
| New suite vs prior regressions | 9 grouped methods / 484 assertions; 48 existing tests / 467 assertions |
| Fault detection | pagination-cap; evidence/fault-results.json |
| Independent execution | NOT RUN |

Coverage: 250 records/two owners, 20 default/100 max, invalid/empty parameters, valid large page, exact stable traversal and scoped totals.

Tests exercise framework requests, real authentication and database state. No live HTTP server or external service is involved. All paths above are campaign-relative. Fault assertion failures are expected positive sensitivity evidence, not unresolved clean-candidate failures.
