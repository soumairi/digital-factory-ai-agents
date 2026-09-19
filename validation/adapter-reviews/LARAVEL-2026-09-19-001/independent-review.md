# Independent Laravel adapter review

Foundation **0.6.0**; adapter/fixture **1.0.0**; review date **2026-09-19**. **Not ready for BACKEND-EVAL-003.** Three adapters are rejected for demonstrated verification gaps. Six receive qualified approval for the reviewed SQLite calibration scope; package finding IR-003 must also be resolved before use.

| Eval | Clean | Faults | Repeatability | Safety | Result |
|---|---|---|---|---|---|
| BE-001 | PASS | 1/1 declared detected | PASS | PASS* | APPROVED WITH LIMITATION |
| BE-002 | PASS | 3/3 declared detected | PASS | PASS* | APPROVED WITH LIMITATION |
| BE-003 | PASS | 1/1 declared detected | PASS | PASS* | APPROVED WITH LIMITATION |
| BE-004 | PASS | 2/2 declared detected | PASS | PASS* | REJECTED |
| BE-005 | PASS | 1/1 declared detected | PASS | PASS* | APPROVED WITH LIMITATION |
| BE-006 | PASS | 2/2 declared detected | PASS | PASS* | APPROVED WITH LIMITATION |
| BE-007 | PASS | 3/3 declared detected | PASS | PASS* | REJECTED |
| BE-008 | PASS | 1/1 declared detected | PASS | PASS* | REJECTED |
| BE-009 | PASS | 2/2 declared detected | PASS | PASS* | APPROVED WITH LIMITATION |

*Safety PASS is limited to reviewed synthetic code and disposable local SQLite execution. It is not a hostile-code containment certification. Declared fault counts exclude the three additional reviewer probes that escaped detection.

## Reviewer Independence and Ownership

VALID: this execution context (`01a0ba52-2eaf-73f1-af31-a833539eb597`) did not implement or repair the adapters or application. Existing adapter/application files and historical campaigns were treated as read-only. Only separate review artifacts were added; disposable faulty copies were removed. Reviewed commit: `8dae8711847e3ef3665c384adb531b23cbd2dc65`. The runtime context identifier is recorded without claiming authenticated external provenance.

Expected values, denial rules, query budgets, seeds and fault expectations are defined in frozen reviewer fixtures/tests, not generated from candidate output. The original fixtures match byte-for-byte. Backend authors must not edit or rebind them. Exact mutation anchors fail closed. BE-009 requires both reviewer and candidate-owned negative tests to fail on its mutants; the bundled candidate suite remains a calibration sample. Candidate tests/TestCase and PHP execute in-process, so coordinator source review, write protection and external containment remain essential.

## Cross-Cutting Findings

| ID | Severity | Issue | Required Action |
|---|---|---|---|
| IR-001 | High | Unbounded database reads escape verification. Replacing SQL pagination with get()->slice()->values() passes unchanged tests (116 and 220 assertions), despite the explicit prohibition on loading all records. Query counts and response lengths do not establish bounded database reads. | Add reviewer-owned assertions for bounded database retrieval and sensitivity to a load-all/slice variant; freeze a new adapter version and independently reverify. |
| IR-002 | High | Authorized document updates need not persist. The owner control submits the existing title and only checks HTTP 200. A disposable variant that validates but omits the document update passes all 150 assertions. | Use a different valid title and assert the exact persisted and returned values, unchanged unrelated rows, and failure of a no-op update variant; freeze and independently reverify. |
| IR-003 | Medium | Requested independent-review.md/json paths are inside the exact frozen inventory. Adding separate review output makes check-freeze, setup and verification fail with Frozen adapter inventory/hash mismatch. Reproduced on a disposable bundle; original frozen files remain unchanged. | Resolve review-output packaging through a separately authorized bundle update or an approved report location outside the executable asset inventory; do not silently rewrite checksums during review. Recheck the published bundle before campaign use. |

IR-001 evidence: `BE-007/tests/BE007Test.php`, `BE-008/tests/BE008Test.php`, and `probes/BE-007/result.json`, `probes/BE-008/result.json` under the evidence root. Both disposable variants kept assertions unchanged, had zero failures/errors/skips, and were followed by a clean PASS.

IR-002 evidence: `BE-004/tests/BE004Test.php` and `owner-update-probe-2/BE-004/result.json`. The scoped no-op mutation retained input validation and authorization. The first probe attempt stopped at its exact-anchor guard before mutation (two matching methods); its incomplete attempt record is preserved. The corrected disposable document-only probe passed 150 assertions, with zero errors/skips; the unchanged clean copy passed again.

IR-003 is an integration defect, not evidence tampering: the requested reports add files but change no frozen bytes. A disposable bundle reproduced the failure before report publication. No checksum or runner fix was made.

## Setup, Clean Verification and Cleanup

| Eval | Setup | Clean Verification | Cleanup | Tests / Assertions | Fresh Repeat |
|---|---|---|---|---|---|
| BE-001 | PASS | PASS; post-fault PASS | PASS; absence confirmed | 54 / 598 | PASS; same source hash and assertion count |
| BE-002 | PASS | PASS; post-fault PASS | PASS; absence confirmed | 2 / 170 | PASS; same source hash and assertion count |
| BE-003 | PASS | PASS; post-fault PASS | PASS; absence confirmed | 2 / 58 | PASS; same source hash and assertion count |
| BE-004 | PASS | PASS; post-fault PASS | PASS; absence confirmed | 2 / 150 | PASS; same source hash and assertion count |
| BE-005 | PASS | PASS; post-fault PASS | PASS; absence confirmed | 2 / 137 | PASS; same source hash and assertion count |
| BE-006 | PASS | PASS; post-fault PASS | PASS; absence confirmed | 2 / 61 | PASS; same source hash and assertion count |
| BE-007 | PASS | PASS; post-fault PASS | PASS; absence confirmed | 2 / 116 | PASS; same source hash and assertion count |
| BE-008 | PASS | PASS; post-fault PASS | PASS; absence confirmed | 2 / 220 | PASS; same source hash and assertion count |
| BE-009 | PASS | PASS; post-fault PASS | PASS; absence confirmed | 14 / 502 | PASS; same source hash and assertion count |

Every adapter was repeated after cleanup in a new workspace, exceeding the required representative subset. All 16 declared mutants produced relevant assertion failures with zero infrastructure errors/skips; reviewer/candidate test bytes and clean source remained unchanged. BE-006 performed five two-process SQLite races per clean verification: one 201 and one 409, stock 3, one reservation.

## Contract Verification

PASS means the binding is present, coherent and verified within the declared scope. FAIL identifies a demonstrated gap, even when clean calibration and the declared mutants pass. All 15 requested items are recorded per adapter below and in the JSON report.

| Contract item | 001 | 002 | 003 | 004 | 005 | 006 | 007 | 008 | 009 |
|---|---|---|---|---|---|---|---|---|---|
| evaluation id | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| adapter version | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| fixture version | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| supported environment | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| initial state | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| synthetic data | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| setup | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| verification | PASS | PASS | PASS | FAIL | PASS | PASS | FAIL | FAIL | PASS |
| cleanup | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| expected clean behavior | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS |
| forbidden behavior | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | FAIL | PASS |
| fault variants | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| expected fault detection | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| security review requirement | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| database requirement | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

Security-review requirement PASS means the requirement exists; it does not grant candidate Security clearance. Database-requirement PASS means SQLite scope and PostgreSQL limitations are explicit. Setup/verification/cleanup PASS observations precede publication of the reports (IR-003).

## Freeze, Safety and Evidence

The initial full inventory freeze passed with SHA-256 `d592ba263d82a988774f9c22e52d98b20f1ffa95d7e0f7a8aabd4203e6caceed`. Independently recomputed all nine fixture hashes and verification hashes; all version comparisons and original-fixture byte comparisons passed. Runner framework tests exercised source changes, symlink rejection, guarded cleanup, environment isolation and skipped-test rejection. All 7 adapter tests and 15 evaluation-framework tests passed before report publication.

Execution used PHP 8.3.33, Python 3.14.4 and the pinned vendor bytes. The existing vendor tree was read/copied only; no historical runner was executed. Setup creates marked `/private/tmp/laravel-adapter-*` workspaces, rejects symlinks and inherited candidate env/config cache, uses sanitized environment/PHP `-n`, and checks SQLite/debug configuration. No production, real credentials/customer data, push, merge, deployment or external infrastructure mutation was used. Synthetic passwords/keys are deliberate fixture values. Existing source hashes are compared against `tracked-baseline.json`.

Evidence root: [`validation/laravel-independent-review-2026-09-19`](../../../../validation/laravel-independent-review-2026-09-19/). It contains `execution/results.json`, per-case original/repeat JUnit and logs, declared fault outcomes, independent probe patches/logs/results, hash checks and provenance. Commands are recorded in `provenance.json` and execution results. `selftest.py` was read and invoked anew as an orchestration of setup → verify → each fault → clean rerun → cleanup → fresh setup/verify/cleanup; previous counts were not reused.

## Limitations

| PostgreSQL assessment | Status | Consequence |
|---|---|---|
| Actual PostgreSQL execution | NOT EXECUTED | No engine validation is claimed; checked local server binary locations were unavailable. |
| SQLite-only adapter calibration | OPTIONAL | PostgreSQL absence alone does not reject any adapter. |
| BE-006 on a PostgreSQL pilot | REQUIRED BEFORE PILOT | Revalidate success, rollback, shortage and genuinely competing transactions; supplied optional probe does not cover PostgreSQL concurrency. |
| BE-008 on a PostgreSQL pilot | REQUIRED BEFORE PILOT | Rebind and validate query counting, bounded retrieval, relationship filtering and serialization on that engine; no PostgreSQL adapter probe is supplied. |
| Other cases | OPTIONAL for SQLite scope | BE-002 type/persistence behavior and BE-007 pagination also benefit from target-engine runs; target-project database bindings must be frozen before use. |

Untrusted code requires external containment. The harness does not enforce OS-level filesystem/network isolation; reviewer assets and provenance need coordinator-controlled permissions. This documented limitation is not treated as an adapter safety violation.

Provenance is limited to this separate review context, observed runtime ID, source hashes and new execution evidence. Calibration intentionally derives from historical source and reuses some assertions; it is not independent test authorship, human review or external audit. Future BE-009 evidence must use the actual implementer contribution with reviewed assertions. Security, architecture, Audit and human campaign gates remain separate.

No historical campaign was rerun or rescored, no BACKEND-EVAL-003 was run, no application/adapter implementation was changed, and no Release Candidate was created.
