# Definition of Done

Done means the backend implementation meets the gates below and is ready for human review. It does not mean merged, deployed, or accepted by a human.

## Functional and engineering gates

- Approved story and acceptance criteria are referenced and mapped to implementation and passing tests.
- Project context and existing architecture were inspected; conventions are supported by evidence rather than assumptions.
- Changes are minimal, focused, maintainable, and limited to the story. Relevant interfaces, compatibility effects, and data changes are documented.
- Assumptions and ambiguities are reported. No unresolved requirement or security ambiguity remains that affects correctness or safety.
- Required tests and checks passed against the reported revision. Missing, skipped, blocked, or failing required checks mean the work is not Done.
- Final diff self-review is complete; findings are resolved and affected checks rerun.
- Required independent review findings and clearance are recorded under shared policies. Pending required clearance prevents a Done claim; human acceptance remains a separate final decision.
- The technical report satisfies the output contract.

## Security-by-Default gate

For **every backend story or API change**, assess **every row** below. Record `addressed`, `not applicable`, or `unresolved`, with rationale and evidence references. An applicable control requires implementation and verification evidence, including verified existing controls when reused. `Not applicable` requires a concrete story-specific reason; omission is not a decision. Any unresolved security ambiguity blocks affected work and a Done claim.

Security must never rely only on frontend validation. Enforce relevant checks on the server, including alternate entry points and background operations affected by the change.

| Required consideration | Evidence to examine or provide |
| --- | --- |
| Authentication | Whether identity is required and enforced; explicit rationale for public operations. |
| Authorization | Server-side permission checks for each operation and entry point. |
| BOLA / IDOR | Object-level checks resist substituting identifiers in reads, writes, lists, and nested resources. |
| Object ownership | Trusted ownership/tenant boundaries enforced independently of caller-supplied fields. |
| Roles and permissions | Allowed and denied actions defined; no unintended privilege escalation. |
| Strict server-side input/schema validation | Types, shapes, allowed fields, ranges, sizes, and invalid/unknown-field handling defined. |
| Mass assignment | Writable fields explicitly constrained; protected fields cannot be assigned through bulk binding. |
| Injection | Untrusted data handled safely at query, command, template, and other interpreter boundaries. |
| Parameter tampering | Client-controlled identifiers, prices, state, and other security-relevant values checked against trusted rules. |
| JWT/token security | If used, verification, permitted algorithms, relevant claims, expiry, and lifecycle/revocation behavior follow approved requirements; tokens are not leaked. |
| Password/credential security | If used, approved storage, verification, reset, and rotation mechanisms; no plaintext storage or disclosure. |
| Rate limiting | Relevant request and operation limits have defined scope and verified enforcement. |
| CORS | Browser cross-origin policy is intentional, restricted as required, and safe with credentials; it is not an authorization control. |
| File uploads | If accepted, validate size, type/content, naming, storage/access, and processing boundaries. |
| Data integrity | Business invariants, constraints, concurrency, and invalid state transitions are protected. |
| Transactions | Atomicity and rollback requirements are defined for related writes and partial failures. |
| Safe serialization | Response fields are explicitly controlled, including nested objects and role-dependent output. |
| Sensitive data exposure | Responses, logs, traces, caches, and errors avoid unnecessary sensitive data. |
| Secure error handling | Predictable failures without secrets, internal traces, or unintended information disclosure. |
| Security logging | Relevant security events are traceable with appropriate redaction and access controls. |
| Least privilege | Database, service, filesystem, and external integration privileges match the operation. |
| Resource limits | Bound payloads, execution time, expensive processing, memory, and external calls as relevant. |
| Pagination | Collection responses have bounded, validated pagination and preserve access boundaries. |
| SSRF | If outbound destinations are influenced by input, validate destinations and redirects against approved network boundaries. |
| Replay attacks | Sensitive repeatable operations have defined replay, nonce, or idempotency protections as appropriate. |
| Brute force | Credential and other guessable-value flows have appropriate attempt controls. |
| Abuse scenarios | Consider enumeration, automation, privilege misuse, and business-logic abuse beyond the happy path. |

## Automated negative-test gate

Assess all six categories for every story. Applicable categories require automated tests that execute and pass; prose review or manual checks alone are insufficient. A category may be `not applicable` only with a specific rationale, such as an intentionally public operation with no identity requirement. Missing test infrastructure or execution access is a blocker, not a reason for non-applicability.

| Category | Required negative behavior to verify when applicable |
| --- | --- |
| Unauthenticated access | Missing, invalid, or expired credentials cannot access protected behavior. |
| Unauthorized access | Authenticated callers lacking permission are denied. |
| Ownership boundaries | Another owner or tenant cannot read, mutate, or enumerate protected objects by changing identifiers. |
| Invalid inputs | Wrong types, missing fields, unexpected fields, and out-of-range values are handled by the defined server schema. |
| Malicious inputs | Relevant injection payloads, hostile uploads/URLs, or oversized payloads are rejected or safely handled. |
| Sensitive field manipulation | Attempts to modify owner, tenant, role, privilege, or other protected fields cannot change protected state. |

Verify observable outcomes, absence of unauthorized side effects, and absence of sensitive response data, not merely status codes. Record test references, execution commands, results, and coverage gaps in the technical report. Use safe test fixtures and authorized environments.
