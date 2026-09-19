# BE-002 Test Results

| Evidence | Result |
|---|---|
| Foundation | 0.5.0; campaign/foundation-sha256.json |
| Candidate | `sha256:d4b2c4e3897fd15bbd3e9c7276e8209f3cbd49c60a5331124547f33a7b37620c` |
| Sandbox | `/private/tmp/backend-eval-001-0v7ydh55/app` |
| Exact execution | evidence/final-command.json; campaign/run-evidence.py |
| Named test | `test_BE002_strict_boundaries_unknown_nested_hostile_and_no_writes` |
| Final result | PASS, 73 assertions; evidence/final-junit.xml |
| Initial result | Behavior test PASS; shared architecture self-review pending; evidence/attempt-1.txt |
| Full regression run | 57 tests / 951 assertions / 0 failures / 0 errors / 0 skipped |
| New suite vs prior regressions | 9 grouped methods / 484 assertions; 48 existing tests / 467 assertions |
| Fault detection | strict-type; evidence/fault-results.json |
| Independent execution | NOT RUN |

Coverage: Boundary name/quantity/description, missing/wrong types, unexpected/nested keys, malformed JSON, hostile scalar and unchanged rejected state.

Tests exercise framework requests, real authentication and database state. No live HTTP server or external service is involved. All paths above are campaign-relative. Fault assertion failures are expected positive sensitivity evidence, not unresolved clean-candidate failures.
