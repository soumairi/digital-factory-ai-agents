# Test Results Summary

| Category | Tests | Result |
|---|---:|---|
| Authentication | 3 | PASS |
| Authorization | 2 | PASS |
| Validation | 20 | PASS |
| Pagination | 3 | PASS |
| Security negative cases | 5 | PASS |
| Scaffold regression | 2 | PASS |
| Total | 35 | PASS |

Non-overlapping allocation: authentication = anonymous, invalid credentials, redacted-auth-event/JSON; authorization = non-admin tampering and non-admin/redacted-event; validation = all 20 data rows (including hostile/protected inputs); pagination = default/schema, stable traversal, minimum/empty page; security negative cases = rate limit, write rejection, CORS, guarded fields, bounded-query/internal-column exclusion. Many tests cover additional categories; each is counted once.

Executed command (existing final run, sandbox working directory):

```sh
./validation/run-tests.sh --log-junit ../evidence/formatted-junit.xml
```

Final result: **35 tests, 437 assertions, 0 failures, 0 errors, 0 skipped**. PHP 8.3.33 / PHPUnit 12.5.35; SQLite :memory: and cleared environment. Final Pint check: **15 files PASS**. No tests were rerun during packaging.

Detailed evidence: [final text](../../../backend-laravel/evidence/US-BE-001/formatted-tests.txt), [final JUnit](../../../backend-laravel/evidence/US-BE-001/formatted-junit.xml), [Pint](../../../backend-laravel/evidence/US-BE-001/format-check.txt). Initial run: [32 tests / 409 assertions](../../../backend-laravel/evidence/US-BE-001/initial-tests.txt). Intermediate: [35 / 437](../../../backend-laravel/evidence/US-BE-001/final-tests.txt). Original setup/Pint temporary-directory failures are disclosed in the prior report; no application test failure was reported.

Revision linkage and its limits: [candidate record](../revision/README.md). This is Backend-produced execution evidence, not independent verification; mutation-sensitivity tests were not performed.
