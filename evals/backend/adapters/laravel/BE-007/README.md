# BE-007 Laravel adapter1.0.1

Original source: `evals/backend/BE-007-pagination.md`; definition1.0.1 is copied byte-for-byte into fixture.json. Objective and criteria are unchanged. This is a reviewer-owned verification asset; Backend candidates do not set expected values. Independent evaluator adoption/review is pending, not self-certified here.

| Contract | Binding |
|---|---|
| Initial state | 250 synthetic rows:125 per owner, interleaved IDs and duplicate nonunique sort values; unchanged dataset during traversal. |
| Shared schema/seeds | ../common/AdapterTestCase.php; four synthetic users in two tenants, seeded Notes/Documents/Profiles, inventory10; new memory database per test |
| Routes | /api/eval/notes, products, report/1, documents, profile, reservations, records, articles; actual Basic web guard and server Gates/resource scopes |
| Runtime | PHP8.3.33, Laravel13.24.0, PHPUnit12.5.33; pinned Composer/vendor; see adapter-manifest.json |
| Expected outputs/effects | fixture.json and expected-results.json; executable tests in tests/ |
| Forbidden outputs/effects | No foreign/protected state/output, traces or invalid writes; DB and response assertions |
| Reset | Fresh application/memory DB per test; setup creates a NEW marked workspace; cleanup removes only that owned directory |
| Baseline | Separate calibration application for adapter self-tests; future campaign supplies approved candidate explicitly |
| Database | SQLite; PostgreSQL NOT EXECUTED |

From repository root:

```sh
bash evals/backend/adapters/laravel/BE-007/setup.sh --vendor /absolute/path/to/pinned/vendor
# Save the returned workspace; never substitute a shared application/database.
bash evals/backend/adapters/laravel/BE-007/verify.sh --workspace /private/tmp/laravel-adapter-XXXX
python3 -B evals/backend/adapters/laravel/runner.py fault --evaluation BE-007 --workspace /private/tmp/laravel-adapter-XXXX --fault-id BE-007-F1
# Run every listed variant, then verify the unchanged clean source again.
bash evals/backend/adapters/laravel/BE-007/verify.sh --workspace /private/tmp/laravel-adapter-XXXX
bash evals/backend/adapters/laravel/BE-007/cleanup.sh --workspace /private/tmp/laravel-adapter-XXXX
```

For a future evaluation, add `--candidate /approved/candidate` to setup and preserve evidence/ before cleanup. Source/test/fixture freeze and real L1 reviewer context records remain mandatory. Candidate tests are never substituted by calibration when a candidate path is supplied. No dependency install, environment import, server deployment, push or merge occurs.

| Eval | Fault ID | Expected Clean Result | Expected Fault Result |
|---|---|---|---|
| BE-007 | BE-007-F1 | PASS | FAIL — relevant assertions, no setup errors |
| BE-007 | BE-007-F2 | PASS | FAIL — relevant assertions, no setup errors |
| BE-007 | BE-007-F3 | PASS | FAIL — relevant assertions, no setup errors |

Faults apply exact reviewer-owned bindings only to disposable copies. If an alternate implementation lacks a source anchor, the runner reports INCOMPLETE rather than silently skipping/fuzzy-patching; a new independently approved frozen binding is required. See ../REVIEW.md for immutability, safety, scope and independent-review limitations.

## Review remediation

Adapter/fixture1.0.1 addresses IR-001. New mandatory fault `BE-007-F4`: Load all records before in-memory pagination. Expected clean PASS / mutant FAIL. Run it with the same runner fault command above and its own fault ID. Status is READY FOR RE-REVIEW only after targeted calibration; separate independent approval is required.

`tests/BoundedReads.php` instruments SQLite PDO statement fetchAll/fetch/fetchColumn during each measured request and restores the statement class in finally. It counts rows actually delivered by each statement, including cursor reads, without matching SQL text or replaying queries. Each statement must return at most the page size; total rows are bounded by the page plus fixed synthetic auth/count/relation overhead. Fixture datasets exceed the maximum page. This observes returned/materialized rows, not engine scan cost or memory bytes; bypassing Laravel's instrumented connection requires separate reviewer binding. PostgreSQL is NOT EXECUTED.
