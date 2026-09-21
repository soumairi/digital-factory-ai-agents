# Self-Review and Report

Apply the [Backend Agent contract](../core/agent.md), all linked core documents, and shared policies. Inspect the final diff and validation evidence against the approved story, actual project context, plan, guardrails, and every gate in the [Definition of Done](../core/definition-of-done.md).

Check scope, maintainability, acceptance criteria, all security topics, and all six negative-test categories. Identify hidden assumptions, unresolved security ambiguity, unrelated modifications, secrets, unsafe error/serialization behavior, and missing test evidence. Fix in-scope findings and rerun affected tests; report blocked or out-of-scope findings explicitly.

Produce the complete [technical report](../core/output-contract.md), including all modified files, all assumptions, tests actually executed and results, security applicability evidence, gaps, and required review/approval status. Self-review does not replace independent Security/Audit review or human acceptance. Select Ready for human review, Incomplete, or Blocked according to the contract, then stop for human review. Do not merge or deploy.
