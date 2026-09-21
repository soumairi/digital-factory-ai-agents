# Context provenance
Coordinator-verified execution separation. No cryptographic independence claim.

| Role | Authentic tool context ID | Scope | Permissions | Evaluations |
|---|---|---|---|---|
| Coordinator | /root | Pin inputs; assign contexts; assemble evidence and decision | Write new campaign only; read source/history | BE-001–009 |
| Backend Implementer | /root/implementer | Analyze, implement, test, self-review, freeze | Write candidate snapshots and own campaign evidence; no reviewer approvals | BE-001–009 |
| Independent Evaluator | /root/evaluator | Own frozen adapter; inspect/run clean and faults; score | Read frozen candidates; write disposable mutants and reviews; no remediation | BE-001–009 |
| Security Reviewer | /root/security | Inspect exact candidates, controls, evidence and severity | Read candidates; write security reports; no code changes | BE-001–009 |

Coordinator start declaration: separate contexts launched via collaboration.spawn_agent; tasks explicitly partition authorship and review. Shared filesystem privileges are broader than role assignments; separation is coordinator-verified, not OS access-control isolation. Each agent preserves its start/completion declaration. Completion and evidence references will be recorded at campaign closure. Human user authorized the campaign; no human code review or audit completion is implied.

## Completion declaration

Coordinator /root completed campaign assembly and verified separate agent start/adoption/handoff/completion records at 2026-09-21T09:20:57.127956+00:00. Implementer completed all nine candidates with one pre-freeze BE-001 self-remediation (campaign/implementer-context.md). Evaluator independently executed all nine cases, all 19 faults and strict evidence gates, then issued reviews/evaluator-completion.json and reviews/aggregate-evaluator-approval.json. Security completed all nine exact-hash reviews in reviews/security-BE-001.json through security-BE-009.json; declaration in reviews/security-context.md. No review context authored candidate corrections. All candidate, governed and historical integrity checks passed. This is coordinator-verified execution separation, not cryptographic independence, human review, external audit or general autonomy. No Release Candidate, real pilot or deployment performed.
