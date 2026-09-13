# Output Contract

Follow [shared output standards](../../../shared/output-standards.md). Produce a concise technical report with the sections below; explicitly write `none` when an applicable section has no entries.

## 1. Story and governing context

Identify the approved story and approval reference, acceptance criteria, foundation release, backend definition version, applicable stack profile (or none), and project context/architecture sources and revisions.

## 2. Outcome and implementation

Summarize behavior delivered, map acceptance criteria to implementation and tests, and explain key design decisions and compatibility/data impacts. List every created, modified, deleted, or renamed file with its purpose. Distinguish task changes from pre-existing unrelated changes.

## 3. Assumptions and ambiguity

List all assumptions, their evidence or validation status, unresolved requirements, security ambiguity, and the work each blocks. Do not hide assumptions in implementation details.

## 4. Security assessment

Include one entry for each security topic in the Definition of Done: topic, `addressed` / `not applicable` / `unresolved`, rationale, implementation reference, and verification evidence. Reference reused controls explicitly. Report findings, remediation, residual risks, and independent Security/Audit review status and references. Do not imply self-review provides independent clearance.

## 5. Tests and checks

List exact commands/checks actually executed, environment and artifact revision, pass/fail results and counts when available, and relevant evidence references. Separately list tests not run, reasons, and consequences. Cover all six negative-test categories with automated test references/results or justified non-applicability. Never invent execution evidence or include credentials in commands or logs.

## 6. Self-review and handoff

State self-review scope, findings and resolutions, Definition of Done gaps, required approvals, and remaining human decisions. Use one status:

- **Ready for human review:** all Definition of Done gates met; human acceptance pending.
- **Incomplete:** work or required evidence remains; list what remains.
- **Blocked:** a missing decision, authorization, access, or required review prevents progression; identify the dependency and owner if known.

Incomplete or blocked work may still be handed over for discussion, but must not be presented as Done. End at human review; do not merge or deploy.
