# Security Detailed Report

## Scope, identity and independence

| Item | Evidence |
|---|---|
| Review | RUN-002-US-BE-001-SEC-B-R2-01 |
| Recorded UTC | 2026-09-19T13:42:21.596149+00:00 |
| Reviewer | Security Agent B, current fresh conversation, local tool identity /root |
| Assignment | User attachment 95bb709b-4319-4a83-bd59-5d632540dbab/pasted-text.txt explicitly assigns NEW independent Security context |
| Story/run | US-BE-001 / RUN-002-US-BE-001 |
| Candidate/hash | R2-01 / b6f595c35d5deda6702771823f0d2bccc382bf250554fc9ba23df18fc301ee65 |
| Foundation | Installed 0.5.0 security contract/workflow/guardrails/checklist/output contract, shared security baseline/development policy, installed project security context |
| Source baseline | 256b048234e6b40e06a2fff70d2e15c884ed482e |
| Environment | /private/tmp/digital-factory-run002-zct1ohhz/app; PHP 8.3.33; Laravel 13.24.0 |
| Write boundary | Only security review artifacts under this run's security/; no implementation, Backend, revision, process or Audit edits |

Independence **VALID**: this conversation has no implementation authorship or participation. Backend's implementation-request.txt, analysis.md and candidate pointer identify a separate NEW Backend conversation. Both conversations use the context-local name /root; that name is not a globally unique session identifier. The historical /root/run002_backend_session_a was a preflight acknowledgment, not proof it implemented R2-01. Separation rests on the explicit fresh-context assignments, distinct conversation history and authorship records, not renaming a role. No globally unique platform session identifier was exposed; none is invented. This report records B's activation without altering frozen preflight history. Application files remained read-only to the reviewer; approved tests generated only disposable runtime logs/cache and in-memory fixtures.

Scope is the 13-file customer-list change plus relevant framework, routes, configuration and tests. The preflight context's NOT YET IMPLEMENTED text describes its creation phase; current source/tests determine actual behavior. Exclusions: production, real data/credentials, network listeners, remediation, deployment and Audit Review.

## Methodology and revision binding

Independently hashed artifact-sha256.txt: exact requested hash. Verified all 139 manifest records and all 28 input/process digest records. Compared all 122 snapshot files with live sandbox source before execution: zero mismatches. Inspected actual implementation.diff, changed-file inventory, controller, request, middleware, resource, models, Gate/limiter, migrations, API/bootstrap/CORS, auth/filesystem configuration, lockfile, PHPUnit tests and safe launcher. Backend summaries and earlier failed attempts were considered evidence, not authoritative conclusions. Existing tests were independently rerun after inspecting their setup and resource effects; no tests or source were altered.

Framework SessionGuard::onceBasic always calls once/credential validation and throws the same UnauthorizedHttpException on failed attempts. Existing storage GET/HEAD and PUT routes also appear in preflight inventory; inspected vendor ServeFile/ReceiveFile enforce relative signatures for private disk and upload flag separation. Empty route middleware does not make these unsigned public access. No new signed-link generator exists in this story; comprehensive storage feature testing is outside this change. Vendor code is existing offline-installed runtime, not included in frozen source; clean reinstall/supply-chain verification is not claimed.

## Access matrix

| Actor/action | Expected | Observed evidence |
|---|---|---|
| Missing/wrong/unknown Basic credentials; GET collection | 401, no customer data | All credential tests passed; missing credentials no customer query |
| Prior valid request followed by missing credentials | 401 | Explicit regression test passed |
| Authenticated non-admin, including role spoof | 403 before customer query | Test passes; persisted admin flag remains false |
| Server-provisioned admin; valid query | 200, bounded four-field rows | Schema/default/second/max/empty-page tests pass |
| Admin with owner/tenant/id/include/role or invalid pagination | 422; no customer mutation | Hostile and validation datasets pass; row equality checked |
| Any client beyond test-process IP allowance | 429 before auth/DB | 61st request test passes; zero DB queries |
| Customer POST | 405; no customer creation | Method test passes |
| Owner vs non-owner / cross-tenant | N/A | Approved administrator-only global collection has no owner/tenant model |

HEAD shares the same route middleware by route/source inspection; a separate HEAD behavioral test was not run.

## Checklist

VERIFIED means the stated scoped evidence, not an exhaustive guarantee. NOT_VERIFIED entries below explicitly limit assurance; none is silently counted as a passing production control.

| Area | Outcome | Evidence / rationale |
|---|---|---|
| Authentication | VERIFIED | AuthenticateCustomerList.php: onceBasic with existing web guard; four negative/credential lifecycle tests passed. |
| Authorization | VERIFIED | AppServiceProvider.php Gate requires boolean is_admin; ListCustomersRequest::authorize precedes query; non-admin test passed. |
| Object-level authorization | VERIFIED | Approved access is whole collection for administrators only. No customer owner/tenant fields; tenant/owner subdivisions N/A, not an omitted requirement. |
| BOLA / IDOR | VERIFIED | Non-admin denied without customer queries; owner_id, tenant_id and id tampering rejected; unchanged customer row asserted. |
| Privilege escalation | VERIFIED | User fillable excludes is_admin; migration default false; mass assignment and role spoof tests passed. |
| Endpoint exposure | VERIFIED | New GET/HEAD api/customers has throttle/auth; POST 405. Existing /, /up and signed storage routes inventoried; see scope note below. |
| Server-side input validation | VERIFIED | ListCustomersRequest rules and after hook bound string shape/ranges, unknown keys and body. 20 validation cases passed. |
| API schema validation | VERIFIED | Exact customer id/name/email/created_at keys and types tested; generic 422; schema enforced in resource and selected columns. |
| Injection | VERIFIED | Fixed Eloquent columns/order; integer pagination; SQL/script input rejected. No application shell/template interpolation of query input. |
| Parameter tampering | VERIFIED | 10 hostile/protected datasets cover role, is_admin, owner, tenant, id, sort, include, token and hostile values. |
| Mass assignment | VERIFIED | Customer guarded [*]; User fillable excludes privilege; endpoint has no model update path. |
| JWT/token security | NOT_APPLICABLE | No JWT/bearer issuance or verification in customer endpoint; arbitrary token input rejected. |
| Password and credential handling | VERIFIED | User hashed cast; framework provider verifies password. Test credentials/key randomly generated in memory; no recovery/login endpoints added. Transport remains unverified. |
| Rate limiting | VERIFIED | 60/min/IP before auth: 61st request 429, Retry-After, no DB query. Only single-process array-cache behavior verified. |
| Abuse protection | VERIFIED | Limiter, authorization before customer query and strict page caps verified; distributed/concurrent capacity unverified. |
| CORS | VERIFIED | Empty allowed origins/headers, credentials false; hostile Origin gets no allow-origin/credentials headers. CORS is not the authorization boundary. |
| Secrets and environment variables | VERIFIED | Changed source has no embedded real credential; wrapper generates ephemeral key, clears environment, refuses env files/cached config. No real credential files accessed; no comprehensive secret-scanner claim. |
| Sensitive-data exposure | VERIFIED | CustomerResource and SELECT independently allowlist four fields; private marker, internal_notes, user fields excluded; no-store verified. |
| Logs | VERIFIED | Two fixed warning calls; exact log spy arguments passed without query or credentials. No arbitrary client input interpolated in application denial messages. |
| Secure error handling | VERIFIED | 401/403/405/422/429 tests pass; API JSON, debug false; no reflected invalid field names. Arbitrary infrastructure failure injection not performed. |
| File-upload security | NOT_APPLICABLE | Story adds no upload. Pre-existing signed storage upload route inspected separately; no unsigned application upload or URL issuance added. |
| Database access | VERIFIED | Fixed ORM read query; memory-only SQLite independently inspected; invalid/unauthorized requests issue no customer SELECT. |
| Least privilege | VERIFIED | Collection access denied by default; select only required fields; sandbox isolated DB. Production DB/OS grants NOT_VERIFIED. |
| Query/resource limits | VERIFIED | page<=1000, size<=100, offset<=99900, stable ID order, two customer queries; total count cost and HTTP size/concurrency limits unverified at production scale. |
| Data integrity | VERIFIED | GET has no customer mutations; hostile inputs preserve row and privilege; POST unavailable. Framework password rehash on successful auth is possible, not a customer business mutation. |
| Transactional consistency | NOT_APPLICABLE | No multi-step business writes in list operation; rollback migration not executed. |
| Logging | VERIFIED | Authentication and authorization denial events generated. Identity/IP correlation and protected retention NOT_VERIFIED; no production logging claim. |
| Monitoring | NOT_VERIFIED | No deployment/detection service in sandbox scope; production verification requirement, not evidence of exploitable failure. |
| Auditability | NOT_VERIFIED | Fixed denial events do not attribute individual actors; production attribution/access/retention need verification. No process Audit performed. |
| Dependency security | NOT_VERIFIED | composer.json/lock unchanged by candidate; 77 runtime and 33 development packages inventoried, no http source URLs. No current vulnerability database scan or clean reinstall; no vulnerability-free assertion. |
| HTTPS/TLS | NOT_VERIFIED | Internal kernel tests only; no listener or real credentials. Production authentication/transport must be independently verified. |
| Production security configuration | NOT_VERIFIED | No production target authorized. Effective sandbox debug false and memory/array resources verified; cannot certify deployment defaults. |
| SSRF | NOT_APPLICABLE | No input-controlled URL, outbound integration, fetch or redirect in changed endpoint. |
| Replay | NOT_APPLICABLE | Read-only customer operation; no transaction nonce/idempotency requirement. Reusable Basic credentials require secure future transport. |
| Brute force | VERIFIED | Pre-auth limiter bounds credential attempts in test process; proxy/distributed protection excluded from this verdict. |
| Information leakage | VERIFIED | Generic error bodies and explicit customer fields checked; no query/stack details in tested errors; arbitrary exception and timing side channels not exhaustively tested. |
| Enumeration | VERIFIED | Unknown user and wrong password both denied via same framework Basic failure; unauthorized collection inaccessible. Fine-grained timing analysis not performed. |
| Abuse scenarios | VERIFIED | Combined non-admin role spoof, protected identifiers, malicious pagination, oversized pagination and repeated requests tested; no unauthorized customer state changes. |

## Independent tests and reproduction

Working directory for all application commands: `/private/tmp/digital-factory-run002-zct1ohhz/app`.

| Command/check actually run | Result |
|---|---|
| Python SHA-256 verification of manifest and context | 139 + 28 records match exact candidate |
| Python byte comparison snapshot to sandbox | 122 files match before execution |
| `/usr/bin/python3 preflight/run.py test` | Exit 0; PHPUnit 12.5.33; 48 tests, 467 assertions; 13.909 seconds; no skipped tests reported |
| `/usr/bin/python3 preflight/run.py inspect` | Exit 0; debug false, no cached config, SQLite :memory:, blank DB URL/file, empty schema; array cache/session/mail, sync queue, single local log |
| `/usr/bin/python3 preflight/run.py routes` | Exit 0; customer GET/HEAD with throttle then authentication; existing scaffold routes inventoried |

Reproduction: after matching the candidate bytes and reviewing launcher/tests, run the three commands above. Tests initialize fresh in-memory schema using inspected migration up methods and synthetic users/customers. No destructive reset trait, down migration, seed, server, worker, external request or real credential is used. Authentication tests use actual password verification, not actingAs bypasses. Assertions inspect response schema, customer query absence and persisted state, beyond HTTP status alone. Backend's formatter result is reported evidence only; this reviewer did not rerun formatting because no code changed.

## SECURITY FINDINGS

No actual scoped vulnerability demonstrated; no SEC identifiers issued. Critical 0; High 0; Medium 0; Low 0. This is not proof of absence of all vulnerabilities. No finding was downgraded, remediated, accepted or closed, and no human risk acceptance was inferred.

## SANDBOX / PRODUCTION LIMITATIONS

| Limitation | Classification | Impact and verification criteria |
|---|---|---|
| Array-cache IP throttling | Sandbox limitation + production verification requirement | Counter is process-local; does not prove even cross-request persistence across fresh workers, much less distributed protection. Verify shared counters, trusted proxy handling, concurrent limits and distributed credential abuse before deployment. |
| Production authentication transport | Production verification requirement | No real HTTP/TLS exercised. Verify deployed authentication design, TLS enforcement, credential forwarding/redaction, password policy and reusable-credential exposure. Test hash cost is intentionally reduced only in isolated tests. |
| Production monitoring | Production verification requirement | Local fixed denial events provide no actor correlation/alert pipeline. Verify useful privacy-preserving attribution, alert delivery, protected access and retention. |
| Dependency advisory coverage | Review limitation | Unchanged lockfile and local framework code inspected; no online advisory scan or reproducible clean install. Run an approved current dependency/security scan before broader assurance; retain tool/version/time/results. |
| Scale and deployment hardening | Production verification requirement | No load, concurrency, request-envelope limits, production grants, proxy/host policy or deployment config validation. Verify bounded operational cost, least privilege, debug-off and safe failure logging against intended environment. |

The three Backend warnings are not automatically findings: no production deployment, real credential transport, distributed service or monitoring requirement was part of the authorized sandbox implementation. Missing production evidence is NOT_VERIFIED, not a claimed implemented control. No external advisory search was used and no current CVE status is asserted.

## Gate, remediation requirements and handoff

**Security Gate: PASS for this exact R2-01 sandbox candidate only**, equivalent to Foundation **ELIGIBLE FOR HUMAN REVIEW**. Scoped source, access boundaries and required negative behavior were inspected and independently tested; there are no demonstrated unresolved findings requiring remediation. Current external vulnerability intelligence and production controls remain outside this bounded assurance, explicitly unverified above.

Required next actions: preserve frozen candidate and obtain independent Audit plus human decision; complete production verification requirements before any real deployment; rerun independent affected-control review for any implementation change or newly substantiated vulnerability. No remediation performed, no messages sent externally, no Audit Review performed, no human approval claimed. PASS does not automatically transfer to a changed hash.

Final preservation check: all 139 candidate manifest records, 28 context digests and 122 live source files still match after test execution and report creation. Findings JSON parsed successfully.
