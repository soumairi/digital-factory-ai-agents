# 10. Team workflow and accountability

| Participant | Responsibility |
| --- | --- |
| Developer | Prepare stories/context, use agents, inspect diffs and review generated code and test evidence. |
| Tech Lead | Validate architecture and important changes under project governance. |
| Security | Independently assess technical controls/findings, verify fixes and advise authorized humans on eligible risk decisions. |
| Repository Maintainer | Review foundation changes and coordinate approved version/tag releases. |
| Project Team | Maintain accurate project context, permissions, commands and explicit foundation adoption. |
| Audit | Verify evidence, traceability, reviewer independence and governance. |
| AI Agent | Assist authorized execution and reporting; never own final human accountability. |

The Security role is not restricted to “significant” stories: the shared policy requires independent Security review for every backend story, endpoint or change. Named approval and risk authorities must be assigned; a job title alone is not an approval record.

## A practical daily loop

Agree on a small story and acceptance criteria. Give the Backend Agent pinned instructions and current context. Review its assumptions and plan, approve sensitive actions when required, and inspect the resulting diff and tests. Route the revision and evidence through [Security and Audit](06-security-and-audit-workflow.md), then human review. Keep the PR, findings, approvals and execution results connected to the story.

Record discovered problems without expanding scope silently. Keep project-specific fixes local; propose sanitized reusable lessons through the [foundation update process](09-update-foundation.md). Include a regression/evaluation case that would catch the original problem. No contribution should contain production secrets or confidential project data.

## Remaining setup decisions

Teams still need named reviewers/approval authorities, an approved runtime and enforced permissions, a safe fixture project, runnable evaluation assertions, evidence storage/retention rules and a release owner/process where the shared policies leave these TBD. Tool-specific loading/permission setup must be verified locally; this provider-neutral guide does not certify it. No real agent evaluation or independent compliance clearance is implied by reading these documents.
