# Campaign scope

| Item | Decision |
|---|---|
| Campaign | BACKEND-EVAL-001 |
| Goal | Backend Agent controlled-pilot readiness assessment |
| Scope | Laravel Backend Agent; nine original repository specifications |
| Authorization | User campaign request in campaign/user-request.txt; disposable fixtures, synthetic data, local tests and fault variants explicitly authorized |
| Allowed | Disposable local sandbox; in-memory SQLite; synthetic fixtures; safe read-only inspection |
| Out of scope | Production deployment/access, cloud administration, real data/credentials, frontend, DevOps automation, autonomous merge/operation |
| Human owner | Requesting user; no new human acceptance is claimed |
| Author/evaluator | Codex primary session; same-author checks are self-review, not independent review |
| Independent reviewer | Unassigned; required independent evidence will remain NOT_VERIFIED |

The user relaxes per-case full Security/Audit cycles, but does not waive criteria requiring independent evidence. Missing independent verification maps Foundation INCOMPLETE to campaign PARTIAL, never PASS. BE-009 requires evaluator-controlled faults; same-author fault experiments are explicitly adapted evidence only. No release candidate, pilot or deployment follows this campaign.
