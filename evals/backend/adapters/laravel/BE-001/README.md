# BE-001 Laravel adapter1.0.0

Original source: `evals/backend/BE-001-simple-crud.md`; definition1.0.0 is copied byte-for-byte into fixture.json. Objective and criteria are unchanged. This is a reviewer-owned verification asset; Backend candidates do not set expected values. Independent evaluator adoption/review is pending, not self-certified here.

| Contract | Binding |
|---|---|
| Initial state | Two synthetic users A/B; one Note each; no external effects. |
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
bash evals/backend/adapters/laravel/BE-001/setup.sh --vendor /absolute/path/to/pinned/vendor
# Save the returned workspace; never substitute a shared application/database.
bash evals/backend/adapters/laravel/BE-001/verify.sh --workspace /private/tmp/laravel-adapter-XXXX
python3 -B evals/backend/adapters/laravel/runner.py fault --evaluation BE-001 --workspace /private/tmp/laravel-adapter-XXXX --fault-id BE-001-F1
# Run every listed variant, then verify the unchanged clean source again.
bash evals/backend/adapters/laravel/BE-001/verify.sh --workspace /private/tmp/laravel-adapter-XXXX
bash evals/backend/adapters/laravel/BE-001/cleanup.sh --workspace /private/tmp/laravel-adapter-XXXX
```

For a future evaluation, add `--candidate /approved/candidate` to setup and preserve evidence/ before cleanup. Source/test/fixture freeze and real L1 reviewer context records remain mandatory. Candidate tests are never substituted by calibration when a candidate path is supplied. No dependency install, environment import, server deployment, push or merge occurs.

| Eval | Fault ID | Expected Clean Result | Expected Fault Result |
|---|---|---|---|
| BE-001 | BE-001-F1 | PASS | FAIL — relevant assertions, no setup errors |

Faults apply exact reviewer-owned bindings only to disposable copies. If an alternate implementation lacks a source anchor, the runner reports INCOMPLETE rather than silently skipping/fuzzy-patching; a new independently approved frozen binding is required. See ../REVIEW.md for immutability, safety, scope and independent-review limitations.
