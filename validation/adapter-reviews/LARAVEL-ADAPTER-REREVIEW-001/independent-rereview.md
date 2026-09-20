# Independent Laravel adapter re-review

Foundation 0.6.0; bundle 1.0.1; completed 2026-09-20. Reviewer independence: **VALID**. **Ready for BACKEND-EVAL-003: YES**, within the frozen SQLite binding and existing operational limitations. This is adapter approval, not a campaign result or approval of a future candidate.

This execution context did not implement remediation. It reviewed commit `090e051` and treated existing adapters, original fixtures, prior reports and historical campaigns as read-only. All new output is under `validation/adapter-reviews/LARAVEL-ADAPTER-REREVIEW-001/`. Mutations occurred only in disposable copies. Independence is based on this execution history; no authenticated external identity or independent authorship of the inherited test suite is claimed.

## Findings disposition

The prior Markdown and JSON reports at `../LARAVEL-2026-09-19-001/` were reviewed. Their original findings were:

| ID | Prior severity | Original defect | Independent disposition |
|---|---|---|---|
| IR-002 | High | BE-004 accepted an authorized non-persisting update because the owner control submitted the existing title and checked only HTTP 200. | CLOSED: changed-title database reload and exact response/read-back pass; F3 fails specifically with `Owner update must persist`. |
| IR-001 | High | BE-007 and BE-008 load-all/slice implementations passed response-size and query-count checks. | CLOSED: actual PDO row measurements pass on clean code and reject both load-all variants. Existing BE-008 N+1 detection also fails the relevant query assertion. |
| IR-003 | Medium | Reviewer reports inside the exact frozen inventory invalidated setup and verification. | CLOSED: external reports coexist with unchanged hashes; disposable edits, removals and internal report additions still fail. |

No remaining or new findings. Unresolved counts: Critical 0, High 0, Medium 0, Low 0. The limitations below are scope and operational constraints, not newly discovered defects.

## Fresh execution results

| Adapter / version | Clean tests / assertions | Declared faults detected | Clean rerun | Fresh repeat | Cleanup | Decision |
|---|---|---|---|---|---|---|
| BE-004 / 1.0.1 | 2 / 166 | 3 / 3 | PASS | PASS | PASS | APPROVED |
| BE-007 / 1.0.1 | 3 / 162 | 4 / 4 | PASS | PASS | PASS | APPROVED |
| BE-008 / 1.0.1 | 3 / 953 | 2 / 2 | PASS | PASS | PASS | APPROVED |

Every fault returned FAIL with relevant assertion failures, zero errors and zero skips. Each mutant used a separate copy; reviewer and candidate test bytes and clean source remained unchanged. Fresh setups reproduced clean assertion counts and candidate hashes. Workspace absence was asserted after cleanup. Raw commands, source hashes, JUnit and logs are in `execution-results.json` and `execution/`; `execute_review.py` records the orchestration. Prior calibration results were not substituted for these executions.

BE-004 changes each of four owners' document titles, queries the database afresh, checks exact returned and subsequent GET values, and checks unrelated rows. Same-tenant non-owner and cross-tenant PATCH requests return 404 and fresh database snapshots remain unchanged. F3 retains authorization and validation but removes persistence; it fails the database assertion. Persistence here means database state beyond the request/model response in the specified SQLite memory fixture, not disk/crash durability certification.

BE-007 verifies default 20, maximum 100, a custom size 7 on page 2, rejection of 101/excessive/invalid sizes, stable ordered traversal without omissions or duplicates, and owner scope. The clean measured requests fetch 22, 102 and 9 total rows respectively (page plus authentication/count). F4 still produces correct response pages but fetches 125 primary rows for page 20 and fails `test_BE007_bounded_database_reads`.

BE-008 retains the existing 5/50 response and query-budget checks, with 4 domain queries and 2 relationship queries. At deterministic datasets of 120 and 600 articles per tenant, page sizes 5/50/100 fetch 9/54/104 total rows with exactly 5 read statements including authentication. F1 fails the query-count assertion (12 domain reads against a budget of 4) and fetched-row overhead. F2 retains constant query counts and valid page output but fetches 120 primary rows for page 5; the bounded-read test rejects it. PDO statement instrumentation is restored in finally and measures fetched rows rather than SQL text patterns.

## Frozen inventory and regression

Freeze SHA-256: `15c729443169c68fe8969b8abd48a18182587a81d94e4e405185ce635952a448`.

The full real asset inventory passed before and after external output. A complete disposable asset copy passed unchanged, then rejected modification of the actual BE-004 test artifact, removal of that artifact, and addition of an internal `independent-review.json`. No report-name exclusion or checksum rewrite was introduced. `freeze.json` records these probes; `final-integrity.json` records publication-time checks.

All nine fixture hashes, verification hashes, version bindings and original-fixture byte comparisons passed (`hash-checks.json`). The other six adapter directories and manifest entries, shared runner/common code, calibration application and historical campaign directories are unchanged from the prior-review commit. Both relocated prior report files match their original Git bytes. The before/after snapshot verifies this review preserved every pre-existing file under evals, tests and validation.

Framework regression: **PASS**, 8 adapter tests and 15 evaluation-framework tests, executed using `python3 -B -m unittest discover -s tests/adapters -v` and the corresponding `tests/evals` command. Logs are `framework-adapters.txt` and `framework-evals.txt`. These cover manifest/fault bindings, status rules, required evidence schema, reviewer ownership/independence, immutable expectations, original/adapted separation, fault relevance and unchanged assertions, skipped/error rejection, source hashes, environment isolation and cleanup guards. Nine relevant faults were additionally executed against PHP; the unrelated six adapters were not fully rerun.

BE-001, BE-002, BE-003, BE-005, BE-006 and BE-009 remain **PREVIOUSLY APPROVED WITH LIMITATION**. They are not upgraded by this re-review.

## Remaining limitations

1. PostgreSQL is **NOT EXECUTED** and is not mandatory for BACKEND-EVAL-003 under the documented SQLite contract. Target-engine validation is recommended and is required before a real PostgreSQL pilot, especially BE-006 competing transactions/rollback and BE-008 query, retrieval and relationship behavior. SQLite results provide no PostgreSQL coverage. Bounded reads concern fetched result rows on the fixture connection, not engine scan cost or production-scale performance; alternate bindings need independent freezing and validation.
2. Untrusted code requires external containment. The runner is not an OS filesystem/network isolation boundary. This review executed only the reviewed synthetic source and declared variants; no sandbox-boundary violation was observed. No containment architecture changes were attempted.
3. The six carried-forward adapters retain their prior limitations. Future candidate provenance, actual BE-009 implementer tests, independent Security review and campaign/human gates remain required. Readiness permits using these adapters; BACKEND-EVAL-003 was not run, historical campaigns were not rerun or rescored, and no Release Candidate, deployment or adapter change was made.
