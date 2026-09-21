# Context provenance

Coordinator-verified execution separation. No claim of cryptographic independence, human independence or external audit.

| Role | Authentic execution context | Assigned evaluations | Scope and permissions |
|---|---|---|---|
| Coordinator | /root | BE-001–009 | Read inputs; freeze inventories; write campaign/aggregate reports; verify evidence and integrity. No candidate implementation or independent technical self-approval. |
| Backend Implementer | /root/implementer | BE-001–009 | Read public requirements/binding; write candidate and owned tests; execute local self-tests; freeze revisions. Cannot access hidden reviewer tests or approve cases. |
| Independent Evaluator | /root/evaluator | BE-001–009 | Adopt immutable reviewer bundle; execute clean and fault runs; record decisions. Cannot author or remediate candidate. |
| Security Reviewer | /root/security | BE-001–009 | Inspect frozen candidate and security behavior; classify findings. Cannot remediate candidate or approve its own code. |

Coordinator start declaration: separate child contexts were created using collaboration.spawn_agent, each with fork_turns=none and role-specific instructions. They inherit tools but not parent conversation. Scope is this campaign only. Runtime context labels come from the collaboration tool, not invented UUIDs. Agent model identity is inherited Codex; exact underlying build is not exposed and is not guessed.

All contexts share filesystem access. Role separation is coordinator-assigned and monitored, not OS-enforced per-agent ACL separation. Host workspace-write restrictions, reviewed synthetic source, sanitized environment and disposable resources reduce risk but the adapter is not a hostile-code jail. No externally supplied unreviewed executable code is authorized. Hidden reviewer files are instruction-restricted, not inaccessible to the implementer at the filesystem layer. Completion declarations are recorded by each context and consolidated at campaign completion.

## Completion declaration

Coordinator `/root` stopped dependent execution after the evaluator confirmed a transient added adapter bytecode file. Campaign INVALID; no candidate implementation or case execution. Implementer completion: implementation/context.md. Evaluator completion: reviews/evaluator-context.json and withdrawn adoption record. Security completion: reviews/security-context.md; all candidate reviews NOT RUN. Coordinator assembled summary, detailed report, readiness assessment and machine results; final original tracked byte integrity verified. No Audit clearance or human acceptance is asserted. No dedicated branch was created because implementation never began; reports remain uncommitted on the preexisting branch, with historical tracked files untouched.
