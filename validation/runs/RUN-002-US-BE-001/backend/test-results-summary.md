# Test results — R2-01

| Category | Tests | Result |
|---|---:|---|
| Authentication | 4 | PASS |
| Authorization | 2 | PASS |
| Validation | 20 | PASS |
| Pagination | 4 | PASS |
| Negative security tests | 14 | PASS |
| Response schema / query behavior | 2 | PASS |
| Existing scaffold regression | 2 | PASS |
| Total | 48 | PASS |

467 assertions; categories are disjoint. Validation: 19 pagination datasets plus GET body. Negative security: 10 hostile/protected datasets plus limiter, log redaction, CORS and disallowed method. Schema test also verifies default pagination; query test verifies two customer queries independent of returned count. Authentication covers absent, invalid, unknown and prior-request credentials. Authorization covers non-admin denial and protected/default privilege assignment.

| Check | Command / evidence | Result |
|---|---|---|
| Final PHPUnit | /usr/bin/python3 preflight/run.py test; test-output.txt | PASS, exit 0; no skipped tests |
| Pint | /usr/bin/python3 preflight/run.py format-check; format-check-output.txt | PASS, 36 files, exit 0 |
| Resource inspection | /usr/bin/python3 preflight/run.py inspect; inspect-output.txt | PASS: sqlite/:memory:, no tables, debug false, isolated array services |
| Route inspection | /usr/bin/python3 preflight/run.py routes; routes-output.txt | PASS: GET/HEAD with throttle and actual auth middleware |
| Diff whitespace | git diff --check | PASS, exit 0 |
| Earlier failures | test-attempt-1.txt; test-attempt-2.txt | Initial 46-test run: 1 failure + 1 error; fixed; second 46-test run passed; final 48 passed |

Working directory: /private/tmp/digital-factory-run002-zct1ohhz/app; PHP 8.3.33, Laravel 13.24.0, PHPUnit 12.5.33. Test setup executes two inspected migration up methods on new empty in-memory connections; no reset trait or destructive command. Counts reflect PHPUnit including setup assertions. Ownership category: no tenant/owner domain; unauthorized collection access and supplied owner/tenant IDs tested. Expiring tokens/uploads/SSRF/write transactions: not applicable to this read-only Basic-auth endpoint. Production load/transport/monitoring and independent Security/Audit not performed.
