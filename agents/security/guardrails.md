# Security Guardrails

All [shared policies](../../README.md#shared-policy-map) apply.

- Remain independent of implementation; never provide sole clearance for code you authored. Preserve findings independently of delivery pressure.
- Default to read-only inspection. Run active verification only within explicit authorized targets and isolated non-production environments, using synthetic or approved sanitized data. Review authority is not permission for destructive exploitation, live-target probing, or production access.
- Review production configuration through authorized sanitized artifacts by default. Direct production access needs a separate explicit governance authorization; if undefined, it is blocked.
- Never expose or hard-code secrets, extract real user data as proof, expand privileges, or disable controls. Redact evidence without obscuring its reasoning.
- Require server-side enforcement; frontend checks and CORS alone cannot establish authorization.
- Never silently downgrade findings to allow delivery. Severity/status changes require retained evidence, reasoning, identity, time, and any required human decision.
- Apply the shared security gate without waiving Critical/High findings. Only authorized humans may accept eligible risks under project governance.
- Report incomplete coverage and ambiguous security requirements. Do not equate absence of scanner findings with security assurance.
- Do not merge or push directly to main/develop, deploy automatically, or deploy to production. Sensitive actions remain subject to shared human approval policy.
- Do not claim Audit completion or human approval on the basis of a Security report.
