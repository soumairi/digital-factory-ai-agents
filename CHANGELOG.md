# Changelog

## 0.3.0 — 2026-09-13

### Added

- Independent Security Agent Foundation v0.1 with systematic review workflow, 38-area vulnerability checklist, guardrails, and finding/report contract.
- Independent Audit Agent Foundation v0.1 with evidence policy, traceability checklist, workflow, guardrails, and standard report template.

### Changed

- Shared security development policy now assigns Backend, Security, Audit, and human responsibilities and defines finding severity/status governance.
- **Incompatible policy tightening:** every backend story, API endpoint, or backend change requires independent Security review; unresolved Critical/High findings block approval even if marked ACCEPTED_RISK. Medium/Low dispositions require defined project governance and authorized human risk decisions where applicable.
- Root documentation describes all three foundations; removed obsolete Security/Audit directory placeholders.

No executable agents, runtime enforcement, project/stack-specific rules, or dependencies were added. Human review and release processes remain required; this change does not itself certify independent review or approval.

## 0.2.0 — 2026-09-13

### Added

- Backend Agent Foundation v0.1: technology-agnostic role contract, responsibilities, lifecycle, guardrails, Definition of Done, and technical output contract.
- Reusable analyze, plan, implement, test, and self-review prompts.
- Security-by-Default applicability evidence and automated negative-test gates.
- README-only placeholders for Laravel, Django, FastAPI, and Node stack profiles.

### Changed

- Root documentation now describes the implemented backend definition and reserved future scope.
- Removed backend directory placeholders where substantive content now preserves the directories.

The backend role tightens inherited boundaries to prohibit direct merges/pushes to `develop`, automatic deployments, and production access without separate governance authorization. Shared policies are unchanged. No executable agents, implemented stack profiles, frameworks, or dependencies were introduced.

## 0.1.0 — 2026-09-13

### Added

- Initial repository structure and reserved directories, retained with `.gitkeep` files.
- Foundation, stack profile, and project context inheritance model.
- Shared engineering, security, development, Git, human approval, audit, and output policies.
- Explicit placeholders for unresolved governance decisions.

This release contains no executable agents, stack or project rules, orchestration framework, or dependencies.
