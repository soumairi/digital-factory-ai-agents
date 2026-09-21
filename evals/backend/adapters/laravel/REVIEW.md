# Independent reviewer handoff — Laravel bundle1.0.1

This package is a new evaluation asset on Foundation0.6.0. It does not rerun or rescore BACKEND-EVAL-001/002, start BACKEND-EVAL-003, create a Release Candidate or authorize integration/deployment. READY means the adapter setup, clean calibration, all required fault detection, cleanup and repeatability were tested. It does **not** mean independent reviewer approval or Backend Agent readiness. The author did not perform the future independent review.

## Review ownership and scope

The Evaluation Reviewer must adopt the immutable assertion/mutation bundle in a separate execution context before Backend implementation. Compare each fixture.json to its original specification and hardened definition. Review all expected values, HTTP/state assertions, input matrices, role/tenant boundaries, query budgets, setup safety, cleanup guards and fault patches. Do not let Backend authors redefine expected results. Shared Core/Security/Audit/human gates still apply. Freeze candidate and context provenance independently; hashes cannot prove reviewer independence.

The bundle binds one canonical synthetic Laravel application interface with actual routes, web Basic guard, Gate definitions, table schema and a test-only between-writes exception hook. The calibration application is a separate copy derived from historical source, updated to the existing0.6.0 contracts. No historical test runner is called. Shared seed/setup and several original assertion blocks were reused read-only and expanded; provenance is intentional, not a claim of independent authorship. Model names and mutation anchors are canonical bindings, not mandatory engineering architecture for arbitrary projects. A materially different candidate requires reviewer-owned rebinding/versioning before execution, never weaker assertions after failure.

## Run and inspect

1. Verify the asset freeze: `python3 -B evals/backend/adapters/laravel/runner.py check-freeze`. It compares file inventory and content with checksums.json, including manifests and the calibration source. Each fixture hash and executable verification hash is separately recorded in manifest.json.
2. Supply the already-installed vendor tree matching common/vendor-sha256.json and the lockfile. No install/network access is automated. PHP default matches this machine; override `--php /absolute/php` only after reviewing/revalidating runtime compatibility.
3. Follow each BE-xxx/README.md setup.sh → verify.sh → every fault ID → verify.sh → cleanup.sh. Setup always creates a fresh marked /private/tmp/laravel-adapter-* directory. Candidate mode uses only the supplied candidate, not the calibration implementation. No candidate credentials/config cache are imported.
4. Save workspace/evidence before cleanup. It contains exact commands, PHPUnit stdout/JUnit, assertion/failure/error/skip counts, source hashes and mutation outcomes. A fault is detected only by relevant assertion failures with zero infrastructure errors/skips. Source and reviewer/candidate test bytes must stay unchanged. Clean PASS plus undetected fault blocks readiness.
5. Repeat setup/clean/cleanup in a new workspace. Compare deterministic source hash, assertion counts and outcomes, not timing or JUnit duration bytes.
6. Verify semantic architecture/scope against the approved story and baseline yourself. The runner checks scoped file changes, pinned dependencies and runtime immutability; these are not a replacement for design/diff review. Source edits outside approved paths require a new reviewer binding.

## BE-009 original-case safeguards

BE-009 has its own fixture.json, verification tests, fault definitions and manifest. It additionally runs BE-001/002/005 normalization checks and the **candidate's** tests/Feature/BackendNegativeTest.php. Six named methods must execute: test_negative_unauthenticated, unauthorized, ownership, invalid, malicious, sensitive_fields. Review the actual assertions and authorship; names alone are not proof. Both reviewer assertions and the appropriate candidate-owned test must fail for each BE-009 mutant. Calibration contains a sample candidate test contribution solely to validate this mechanism. A future evaluator must replace it with the actual implementer's contribution, not claim the sample as Backend output. An unavailable/renamed suite needs a separately frozen mapping; absence is INCOMPLETE.

## Database semantics

SQLite uses a new memory database per PHPUnit test; BE-006 additionally executes five genuine two-process races against fresh private files. Two reservations of7 from stock10 must produce one201/one409, stock3, one reservation. Atomic conditional decrement and transaction rollback are checked; serial repetitions alone do not stand in for races. The transaction-bypass mutant must leave observable partial persistence and fail the DB assertion. The swallowed-failure mutant must fail error semantics. No external messages exist in these fixtures, so after-commit messaging is not claimed.

Optional PostgreSQL support is restricted to BE-006's transaction probe:

```sh
python3 -B evals/backend/adapters/laravel/postgres.py --workspace /private/tmp/laravel-adapter-XXXX --pg-bin /absolute/postgresql/bin
```

Requires complete postgres/initdb/pg_ctl/createdb binaries. It creates a NEW cluster inside the marked workspace, synthetic local role/database, socket-only listening in a private directory, runs success/rollback/shortage checks and stops the cluster in finally. No DSN/host/password option is accepted. The runner refuses cleanup while a PostgreSQL pid file remains. PostgreSQL validation is NOT EXECUTED on this machine: the checked libpq installation lacks a postgres server binary. PostgreSQL concurrency/query behavior is not claimed; extension must be independently tested before use as such evidence. PostgreSQL absence does not block SQLite-ready adapters.

## Safety and known limits

Only reviewed, authorized synthetic candidate code is supported. A fresh workspace, sanitized environment, PHP -n, debug=false and explicit runtime SQLite assertions prevent accidental inherited-service configuration. Candidate .env/config-cache, unexpected dependency bytes and symlinks are rejected. Credentials/keys are deliberately synthetic; no real secrets are loaded. No cloud/push/merge/deploy commands exist.

This is not an OS sandbox for malicious PHP. A native network-denial sandbox probe was unavailable under current host permissions; arbitrary hostile candidate code must not be passed to this runner. The future coordinator must inspect approved source and enforce any stronger filesystem/network containment externally. Do not claim distributed/production rate limits or production PostgreSQL semantics from local tests. Existing customer-route limiter/logging regressions are baseline regressions, not evidence for unrelated eval routes.

Mutation bindings are exact and fail closed. Constructor/source hooks, models and middleware in an alternate application may require a new frozen adapter binding. Full Security review, source-level architecture judgment, L1 provenance verification and final campaign scoring remain outside this calibration task. Framework unit tests and build logs are in tests/adapters/ and validation/laravel-adapter-build/; they are not campaign outcomes.

## Remediation and external review output

BE-004, BE-007 and BE-008 adapter/fixture versions are1.0.1; other adapters remain1.0.0. Targeted calibration may establish READY FOR RE-REVIEW, never independent approval. The remediator cannot independently approve these changes; a separate future context must adopt and verify the revised assertions and all19 mandatory faults across the bundle.

Save reviewer-generated output only in `validation/adapter-reviews/<REVIEW-ID>/independent-review.md` and `independent-review.json`, outside this adapter directory. The original rejected review is preserved byte-for-byte at `validation/adapter-reviews/LARAVEL-2026-09-19-001/`; its verdict is not rewritten by remediation. See its relocation README for original evidence paths. Freeze protection is unchanged: every adapter-owned file and unexpected file in this directory remains checked; there are no report-name exclusions. Do not place reports here or regenerate checksums to accommodate review output.

BE-004 now requires a changed title reloaded from persistent storage, exact response/read-back values and unchanged unrelated/denied rows. BE-007/008 measure actual PDO-fetched rows through their case-local statement instrumentation, including fetchAll and cursor fetch, without SQL-string matching. BE-007 allows page size plus2 scalar/auth rows; BE-008 allows page size plus4 auth/count/relation rows and at most5 read statements including auth at datasets120/600 per tenant and pages5/50/100. Existing domain/relationship query budgets remain. New faults cover a non-persisting owner update (BE-004-F3), load-all records (BE-007-F4), and load-all articles (BE-008-F2). This measures materialized result rows, not database scan cost, and is bound to the fixture's SQLite connection. PostgreSQL remains NOT EXECUTED.

## Prospective Foundation 0.6.1 freeze

For new campaigns, the [governed inventory policy](../../../../docs/evaluation-freeze.md) supersedes exact arbitrary directory enumeration above. `check-freeze` returns the externally pinnable governed inventory digest, covering source and relevant Foundation rules while tolerating only narrow runtime artifacts. Historical reviews and campaign conclusions remain unchanged; their approval does not certify the changed framework runner. Assertions, fixture and fault versions remain unchanged.
