# Security Development Policy

## Lines of responsibility

- **First line — Backend Agent:** builds with Security-by-Default and owns implementation, tests, and self-review.
- **Second line — Security Agent:** performs independent technical security review of every backend story, API endpoint, or backend change, including independent remediation verification.
- **Audit — Audit Agent:** verifies evidence and traceability that engineering, security, and governance policies were followed; it does not duplicate technical vulnerability assessment.
- **Human:** remains the final authority for approval and risk acceptance within shared policy constraints.

The implementing agent must not be the only agent validating security or compliance. Security reviewers must be separate from implementation authorship; Audit must be separate from authorship of the implementation and review/governance evidence it audits. A role-label change is not independence. Record reviewer identity and assignment; missing required independence blocks clearance. If a reviewer contributes a fix, assign another independent reviewer to validate that work.

Backend evidence → independent Security review → Audit evidence/traceability review → human decision. Remediation returns to Security for verification, then Audit checks updated evidence. Agents cannot turn their reports into human approval.

## Secure development responsibilities

- Identify relevant assets, trust boundaries, entry points, and misuse risks before making security-sensitive changes.
- Apply input validation, appropriate authorization, safe error handling, and data minimization wherever relevant.
- Never hard-code credentials or log secrets. Use established, reviewed cryptographic mechanisms rather than custom cryptography.
- Introduce dependencies only when justified; review their source, maintenance, license compatibility, and known vulnerabilities using the consuming project's approved process.
- Verify changed behavior and relevant failure paths. Select security checks appropriate to the impact, such as secret detection, dependency analysis, static analysis, or targeted tests.
- Report which checks ran, their results, and any coverage gaps. Do not claim security assurance from checks that were not performed.
- Route every backend story, API endpoint, or backend change to independent Security review before human integration approval. Other security-sensitive changes also require independent Security review. Controls must be server-side; frontend validation alone is insufficient.
- Block progression of affected work when material security findings remain unresolved. Agents cannot accept security risk on behalf of humans.
- Record remediation and obtain independent verification of security finding closure.

## Security gate and finding governance

A story must NOT be approved while unresolved **Critical** or **High** findings exist. These findings require independently verified remediation or evidence-supported false-positive resolution. ACCEPTED_RISK does not resolve a vulnerability or clear this gate. Humans remain the final authority within this constraint, not an exception to it.

**Medium** and **Low** findings require documented disposition under project governance: remediation, justified false-positive resolution, or authorized human risk acceptance where permitted. If that governance or required evidence is undefined, approval remains blocked. Agents cannot accept risk. Incomplete required verification or security ambiguity prevents security clearance independently of finding counts.

Use these qualitative severity baselines, recording impact, reach, exposure, exploit prerequisites and uncertainty:

| Severity | Baseline |
| --- | --- |
| Critical | Plausible broad or catastrophic compromise of sensitive assets or privileged control with severe consequences. |
| High | Plausible substantial unauthorized access, modification, privilege gain or service compromise. |
| Medium | Material but more constrained impact or exploitation requiring significant conditions. |
| Low | Limited impact or a defense-in-depth weakness with a supported risk explanation. |

Projects may refine criteria without weakening the gate. Never silently downgrade issues to allow delivery. Preserve original severity/status and each change's rationale, evidence, reviewer identity, and time. Delivery pressure is not severity evidence.

Security finding statuses are exactly:

- **OPEN:** newly identified, unresolved, proposed fix awaiting verification, or reopened after regression/expired acceptance.
- **REMEDIATED:** independent Security verification demonstrates the recorded verification criteria pass on the identified revision.
- **ACCEPTED_RISK:** an authorized human has explicitly accepted the residual risk under permitted project governance. Record authority, rationale, scope, conditions, expiry/review trigger, and decision reference. This is not remediation and cannot clear Critical/High blockers.
- **FALSE_POSITIVE:** independent Security review establishes with evidence that the claimed vulnerability does not apply; retain the original finding and reasoning.

New findings begin OPEN. Status changes require the evidence above; proposed or implementation-only closure is insufficient. Reopen findings when contrary evidence, regressions, expired acceptance, or changed scope invalidate disposition. Security records technical dispositions; Audit verifies their evidence and governance without altering technical findings.

## Further definition

- **TBD:** Named human risk acceptance authorities and project-specific disposition/expiry rules.
- **TBD:** Minimum check requirements by change risk and evidence required for risk acceptance.
- **Project layer responsibility:** Select concrete tools and commands without weakening this baseline.

Until risk acceptance authority and criteria are defined, unresolved material findings remain blocking. Absolute prohibitions in shared policies cannot be waived by risk acceptance.
