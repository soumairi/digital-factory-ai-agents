# Execution plan

1. Freeze all tracked input bytes and verify Foundation 0.6.0 and independent adapter approvals.
2. Independent evaluator adopts the frozen original-case adapters and hands public interface bindings to the separate implementer before implementation.
3. Implementer reads applicable rules, analyzes, builds only synthetic required behavior and owned tests, runs/self-reviews, records corrections and freezes uniquely named per-case candidates.
4. Evaluator checks candidate hash, runs clean verification, every mandatory fault in separate copies, and clean rerun. It preserves raw logs, JUnit, exact commands and mutation evidence. Security independently inspects the same hash and relevant behavior.
5. Reviewer records seven original scoring dimensions, case decisions and canonical evidence manifests. Coordinator validates manifests, original/adapted distinctions, metrics denominators, input integrity and required reports.
6. Report recommendation without forcing readiness. No release/pilot/deployment follows.

SQLite is the approved engine. Do not obtain PostgreSQL or defer SQLite for it. Missing execution/review evidence is not a pass; observed failures override incompleteness. No numerical score overrides hard failures. Shared implementation corrections are counted once as events and mapped to affected cases.
