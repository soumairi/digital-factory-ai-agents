# Security context start — BACKEND-EVAL-003

- Authentic runtime context: `/root/security` (separate spawned execution context assigned by `/root`).
- Role: independent Security Reviewer; implementation authored by `/root/implementer`; evaluation owned by `/root/evaluator`.
- Assigned scope: all nine original BE-001–BE-009 cases, candidate source/configuration and independent synthetic SQLite behavior verification.
- No candidate authoring or remediation by this context. No adapter, Foundation or historical evidence changes. Reviewer evidence only under this campaign.
- Candidate is pending freeze; no clearance or findings count inferred before execution.
- Containment: disposable adapter directories and sanitized local SQLite only. No production, network, credentials, dependency install, shared service, deployment or risk acceptance authorized. Harness is not an OS hostile-code sandbox; source must be inspected before execution. Shared filesystem access is a limitation: separate execution contexts do not enforce ACL isolation. Context identity is observable in orchestration, not authenticated by this document/hash alone.
- Governing baseline: Foundation 0.6.0, shared policies, agents/security role contracts, original cases and docs/14-backend-evaluation-protocol.md.
- Review uses exact Critical/High/Medium/Low severities and OPEN/REMEDIATED/ACCEPTED_RISK/FALSE_POSITIVE finding states. Required verification gaps block clearance.
- PostgreSQL and production/deployment controls are outside this SQLite campaign; no claim of their verification.

Policy/specification bytes read at role start:

- `shared/audit-policy.md` SHA-256 `ae63f8537800ad604a43b4a2d0eeeed5fc3de6bc94396ee641a3edcd3b7b0e80`
- `shared/output-standards.md` SHA-256 `994cc6733d31e906a72f227ef7251874bf95c18ba2cd92c9f63d982ad89abec0`
- `shared/human-approval-policy.md` SHA-256 `effdd33343624784ed8c5e883811d0a4f76e5083f76615a0192bfd73afeaa61c`
- `shared/security-baseline.md` SHA-256 `723028b47228255db4921e16b552ec042ceac32d67185ca28ecd6e8618d2733d`
- `shared/git-policy.md` SHA-256 `fc0f968fe589eb8296a043cf035477eb70c78381188b45df33743d0faab51052`
- `shared/engineering-principles.md` SHA-256 `54cd09c54110baaa561ff2e9bf0a5dabfe2b67f45c6a5b498d915544b610a92d`
- `shared/security-development-policy.md` SHA-256 `6e1a1fea2cd7fcc325b8d84a82c25856f82acca07e4cf39cfbfb48baf045cadd`
- `agents/security/agent.md` SHA-256 `237c3783e4071db9327a84bb0965bd95229ba7edc316ec0fb4f314af5a8e0f22`
- `agents/security/guardrails.md` SHA-256 `4a6f74ce821d4bb1d45b74616a60a04d6dd6b89347444f4eb83a574b11e3d955`
- `agents/security/vulnerability-checklist.md` SHA-256 `593acab23389e9eee0b038df3a7d6dccc072a66c9ac0e30fd3c800a719e0b3ef`
- `agents/security/output-contract.md` SHA-256 `1be424fcac7f3325eb30a43ca98aa4b5681076cd8d5461456f4ea90a832c3606`
- `agents/security/workflow.md` SHA-256 `06fc46ddedbfbfbd0f7bad8b0460b40063c881c6ba18585b98b72f8ac4cbb1e4`
- `agents/security/README.md` SHA-256 `1d67632887be56b2d8d65067fda0c82dbc48f532d18405964f950955c75a42b5`
- `docs/14-backend-evaluation-protocol.md` SHA-256 `6ee545f99f4f387eaab8667f195d014de8f7c2bc75c4c1fb8151e5e4d2230276`
- `evals/backend/BE-001-simple-crud.md` SHA-256 `ce0e333845d7fe54212dc41ddb45aa5f7535f4e6c266eda43f0d15f75821d620`
- `evals/backend/BE-006-transaction.md` SHA-256 `dd5cfcfdd3c9073d2dfc547839c2e76112e84d00a945e0c3398b1e1bddbffd70`
- `evals/backend/BE-007-pagination.md` SHA-256 `6b83602f9df33a9c7c49cb613e974c2cd51fcc28d62370ed6efe1348584fe66e`
- `evals/backend/BE-008-n-plus-one.md` SHA-256 `1322016ba2917ea741bba71b043de3eba7f56b1519f609bce75e87e10ed5dc58`
- `evals/backend/BE-004-bola-idor.md` SHA-256 `3d3062a99f7a0724fab585bff96246ef0b029339283601a9653e081affc2dabb`
- `evals/backend/BE-003-authorization.md` SHA-256 `4639a8ce8f81ccf46edeee3471a1ad9f640f4e52a0db6563387814df2f7c59c1`
- `evals/backend/BE-005-mass-assignment.md` SHA-256 `c1ff619c10115eaf0772383f111c7340716e3ef597f7589e122785059966d7c2`
- `evals/backend/BE-009-negative-security-tests.md` SHA-256 `2f07f1381353054a25ec9cacfcfec7366f9fb51722cb8efb4a271daa2d096061`
- `evals/backend/BE-002-validation.md` SHA-256 `b4ea9799ea3495fc1648e809383d7f9666757f936654e5df964bdc5933b63823`

## Completion declaration

2026-09-20T11:36:25.409060+00:00 — `/root/security`: stopped on campaign invalidation before candidate handoff. All nine Security results NOT RUN; no clearance. See security-review.md and security-review.json.
