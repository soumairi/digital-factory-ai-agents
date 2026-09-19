# Laravel adapter remediation — Foundation 0.6.0

Implementation/calibration only; independent re-review required. This context performed remediation and cannot independently approve these changes.

| Finding | Adapter | Severity | Required Fix | Verification |
|---|---|---|---|---|
| IR-002 | BE-004 | High | Reload changed owner title from DB; exact output/state and unchanged foreign rows | Clean; F1/F2; new F3 no-op persistence; fresh repeat |
| IR-001 | BE-007 | High | Measure actual fetched rows, default/max/custom pages and stable order | Clean; F1/F2/F3; new F4 load-all; fresh repeat |
| IR-001 | BE-008 | High | Bound fetched rows as well as query count at two dataset sizes | Clean; existing F1 N+1; new F2 load-all; fresh repeat |
| IR-003 | Bundle | Medium | Move review reports unchanged outside exact frozen inventory | External report does not affect freeze; internal addition/modification/removal still fails |

Historical review: validation/adapter-reviews/LARAVEL-2026-09-19-001/. Historical campaign results remain unchanged. No BACKEND-EVAL-003 or Release Candidate.

## Calibration outcome

**READY FOR RE-REVIEW**; findings are not independently closed. Foundation remains0.6.0. Bundle1.0.1 contains BE-004/007/008 adapter and fixture1.0.1; other six adapters and their manifest entries/hashes are unchanged. Original objectives and application implementation were not modified.

| Adapter | Clean | Fault sensitivity | Fresh repeat | Cleanup | Tests / Assertions |
|---|---|---|---|---|---|
| BE-004 | PASS | 3/3 | PASS | PASS | 2 / 166 |
| BE-007 | PASS | 4/4 | PASS | PASS | 3 / 162 |
| BE-008 | PASS | 2/2 | PASS | PASS | 3 / 953 |

New faults BE-004-F3, BE-007-F4 and BE-008-F2 fail the required persistence/read-bound assertions with zero errors/skips. All existing targeted faults also fail relevant unchanged assertions. Clean reruns after faults pass; fresh repeats have identical assertion counts and candidate hashes. Each workspace was removed and absence checked.

BE-007's load-all mutant fetched125 primary rows for a requested page20 and was rejected. BE-008's load-all mutant fetched120 primary rows for a requested page5 and was rejected. Clean BE-008 requests at120 and600 rows per tenant remained within page size plus4 fetched rows and at most5 read statements; original N+1 thresholds still apply. The PDO statement class is restored after measurement. Measurements concern actual fetched result rows, not engine scan cost; no implementation-specific SQL comparison is used. Case-local helper copies deliberately avoid changing shared code or unrelated verification hashes.

Frozen inventory: PASS. No runner exclusion was introduced; internal unexpected files, edits and missing assets remain rejected. External review-output additions do not affect the freeze (framework regression test). Both prior report files are archived byte-for-byte under validation/adapter-reviews/LARAVEL-2026-09-19-001/. All prior validation/campaign files and calibration application bytes remain unchanged. All9 per-adapter fixture and verification hashes independently recomputed successfully.

Framework checks:8 adapter tests and15 evaluation-framework tests PASS. Commands: `python3 -B -m unittest discover -s tests/adapters -v`; `python3 -B -m unittest discover -s tests/evals -v`; `python3 -B evals/backend/adapters/laravel/runner.py check-freeze`; targeted execution: `python3 -B validation/laravel-adapter-remediation-2026-09-19/calibrate.py`. Exact PHP commands, source hashes, logs and JUnit are in execution/. Calibration refuses to overwrite its execution directory.

PostgreSQL: NOT EXECUTED. SQLite calibration is not cross-engine validation. Untrusted code still requires external containment; no containment architecture changes were made. This remediation context must not independently approve the modified adapters. No campaign, historical rerun, push, merge, deployment or Release Candidate occurred.
