# Security preflight — BACKEND-EVAL-002

Scope: BE-001 through BE-009, Foundation 0.6.0. Reviewer context `/root/eval002_security`. Start: 2026-09-19T14:49:47Z. Completion: 2026-09-19T14:51:40.302254Z. Repository HEAD at inspection: `2fcae8e04c7c68f7fceb556739c9d852adc23989`; this is not a frozen candidate hash.

**Security gate: INCOMPLETE. Candidate Security review: NOT RUN. Candidate review has not executed; no Security clearance or PASS is issued.** No vulnerability finding count can be inferred from this preflight. Unreviewed candidate Critical/High counts remain unknown; no candidate is bound to this report.

## Inspected evidence

Read `evals/backend/README.md`, `docs/14-backend-evaluation-protocol.md`, Security guardrails/checklist/output contract, the current user campaign request, and BE-006/009 fixture contents. Parsed all nine fixture definitions for Security requirements and fault IDs; all nine require independent Security review. Inventory of `evals/backend` found definitions, schema and manifest checker, not stack-specific executable application adapters. Historical Laravel application/test files exist under BACKEND-EVAL-001; file presence establishes neither prospective reviewer ownership nor compliance with the hardened fixture assertions. No historical tests were executed or changed. No new reviewer-frozen executable bundle existed in the new campaign paths at the time of inspection.

## Required before candidate clearance

1. Freeze approved Laravel routes, actual authentication/authorization mapping, actor/action/resource matrix, database engine, safe error contract, synthetic data and allowed execution commands. Pin candidate and policy/fixture/assertion hashes.
2. Evaluation Reviewer freezes independent executable assertions before Backend implementation, covering every required test and applicable normalization vector. Preserve original-case requirements and distinguish adapted execution.
3. Run clean verification and all 16 mandatory fixture faults in disposable copies; unchanged relevant assertions must fail for the intended defect without infrastructure errors. Hash clean bytes and rerun clean afterward.
4. Provide candidate-bound Security evidence for every checklist row, including ownership and tenant denial with persisted-state checks, writable fields, input/error leakage, bounded pagination/query growth, repeated requests, and rate-limit/abuse behavior where defined. Undefined access semantics block dependent verification. Missing infrastructure is NOT_VERIFIED, not NOT_APPLICABLE.
5. BE-006 requires genuine competing reservations on the declared engine and rollback evidence. BE-009 requires all six negative categories, persisted-state/safe-output assertions, and defect sensitivity of the implementation test suite. Merely running a different reviewer suite does not prove the implementer suite detects defects.
6. Separate reviewer authorship from candidate authorship; coordinator verifies context provenance and write permissions. Review every required Security control and retain findings before assigning candidate clearance. Only eligible human governance can accept applicable Medium/Low risks; no unresolved Critical/High may pass.

No candidate checklist is supplied as if completed: all candidate controls remain NOT_VERIFIED until a frozen candidate is assigned. This preflight is not an Audit or human approval.

## Disposable PostgreSQL discovery

Only executable availability/version checks were performed. No database or Docker service was contacted; no cluster, container, or application was started.

| Check | Observed |
|---|---|
| `command -v psql initdb pg_ctl` | `/opt/homebrew/bin/psql`, `/opt/homebrew/bin/initdb`, `/opt/homebrew/bin/pg_ctl` |
| `psql --version`, `initdb --version`, `pg_ctl --version` | PostgreSQL 18.4 |
| Symlink targets | `/opt/homebrew/Cellar/libpq/18.4/bin/` |
| `command -v postgres` | Not found |
| `ls` of libpq `postgres` and `postmaster` | Both absent |
| `/Applications/Postgres.app/Contents/Versions` | Not available at inspected path |
| `docker --version` | Docker 24.0.1, build 680212238b |
| `command -v podman` | Not found |
| `command -v sqlite3` | `/usr/bin/sqlite3` |

The libpq tools do not establish a runnable PostgreSQL server. Docker CLI presence does not establish a running daemon or usable local image. PostgreSQL execution is therefore NOT VERIFIED by this preflight; coordinator may investigate a separately authorized disposable runtime, or report the limitation. No cross-database validation is claimed. An initial zsh glob check failed with “no matches found”; explicit libpq binary checks above resolved the relevant installed path.

## Handoff

No implementation, active security testing, application-level findings, corrective changes, or acceptance decision occurred. Supply a frozen candidate plus reviewer evidence and explicitly scoped disposable target for actual Security verification. Until then, missing mandatory Security evidence prevents CONTROLLED PILOT READY; preflight independence alone does not supply execution coverage.

Coordinator completion update: Evaluation Reviewer confirmed all nine mandatory reviewer-frozen Laravel adapters absent. Under user Step 2, no candidate implementation or application execution will occur in this campaign. Actual Security review remains NOT RUN.
