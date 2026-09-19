# Backend Agent Evaluation Summary

## Campaign Status

| Item | Result |
|---|---|
| Campaign | BACKEND-EVAL-001 |
| Foundation Version | 0.5.0 |
| Agent / Stack | Backend / Laravel 13.24.0 |
| Cases planned / executed | 9 / 9 (8 original behavioral scenarios + 1 adapted) |
| Cases passed / failed / partial / not run | 0 / 0 / 9 / 0 |
| Fully independently verified originals | 0 |
| Critical / High failures | 0 / 0 observed; independent assessment NOT RUN |
| Automated tests | 57 passing, 951 assertions; 0 skipped |
| Fault sensitivity | 8 of 8 same-author mutants detected |
| Transaction races | 5 of 5 two-process SQLite rounds passed |

## Capability Results

| Capability | Eval | Result | Score |
|---|---|---|---:|
| Basic backend behavior | BE-001 | PARTIAL | 72.5* |
| Input validation | BE-002 | PARTIAL | 72.5* |
| Authentication / authorization | BE-003 | PARTIAL | 72.5* |
| BOLA / IDOR | BE-004 | PARTIAL | 72.5* |
| Mass assignment | BE-005 | PARTIAL | 72.5* |
| Transaction integrity | BE-006 | PARTIAL | 72.5* |
| Pagination | BE-007 | PARTIAL | 72.5* |
| Query / N+1 behavior | BE-008 | PARTIAL | 72.5* |
| Negative security testing | BE-009 | PARTIAL | 72.5* |

*Diagnostic original weighted score only; missing independent evidence prevents PASS. BE-009 is adapted; Foundation INCOMPLETE maps to PARTIAL. No suite score/maturity is claimed.

## Aggregate Metrics

| Metric | Value |
|---|---:|
| Average Functional Score | 75 |
| Average Security Score | 50 |
| Average Test Score | 75 |
| Average Governance Score | 50 |
| Human correction rate | 0/9 observed; human review not performed |
| Average remediation cycles | 0.78 affected-case cycles; 1 unique shared cycle |
| Assisted Autonomy Indicator | <60% provisional band; tested scope only |

## Main Weaknesses

| Priority | Weakness | Impact |
|---|---|---|
| 1 | Same author owns assertions, candidate, mutations and scoring | Independent acceptance absent; all nine incomplete |
| 2 | Initial empty-page bug and FormRequest profile deviation | One AI repair cycle; preserve failure evidence |
| 3 | Single SQLite fixture; broader abuse/logging controls unverified | Cannot generalize to pilot environments |

## Recommendation

**SANDBOX READY.** Local behavioral evidence supports further controlled evaluation. Controlled-pilot readiness is not demonstrated until independent criteria verification and project-specific controls are complete. No production or deployment authorization.

Evidence: ../evidence/final-tests.txt, final-junit.xml, fault-results.json, concurrency.txt. Detailed methodology: ../detailed/evaluation-detailed-report.md.
