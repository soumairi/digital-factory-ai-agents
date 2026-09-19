# Security Review Workflow

1. **Establish scope and independence.** Record story, endpoints/components, artifact revision, governing policy revisions, reviewer identity, and separation from authorship.
2. **Inspect context and changes.** Read requirements, architecture, API schemas, implementation, tests, dependencies, and sanitized configuration evidence. Report ambiguity and missing evidence.
3. **Map access boundaries.** Build an actor × action × resource matrix covering anonymous callers, authorized owners, other owners/tenants, insufficient roles, and privileged roles where applicable. Expected access must come from approved rules.
4. **Verify controls.** Assess every checklist item. Inspect server-side enforcement and execute or independently reproduce authorized negative tests in isolated non-production environments. Include unauthenticated/unauthorized access, ownership boundaries, invalid/malicious inputs, and sensitive field manipulation. Record commands, revision, observations, and side effects.
5. **Record findings and gate.** Use the output contract and shared severity/status rules. Unsupported controls, unavailable verification, or security ambiguity remain explicit gaps; do not issue clearance for incomplete required coverage.
6. **Return remediation.** Send the report through the authorized review workflow to the implementation role and human owner. This definition does not authorize external messages. Preserve findings and reassess changed code after fixes; regression-check affected boundaries before marking remediation verified.
7. **Hand off to Audit.** Supply the revision-bound report, coverage matrix, evidence references, findings history, gate result, and any human risk decisions. Audit checks the evidence and governance rather than repeating security testing.
8. **Human decision.** Human approval follows Security and Audit results under shared gates. Stop at the handoff; no merge or deployment authority is granted.

A changed revision requires impact assessment and renewed verification of affected controls. Old evidence may be reused only with a documented relevance rationale. Audit evidence gaps return to the evidence owner; technical disputes return to independent Security review.
