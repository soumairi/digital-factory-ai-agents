# Independent Security Review — US-BE-001

## Scope, assignment and identity

Reviewer: **Security Agent B**, assigned by the user in this new independent execution context on 2026-09-17. This reviewer did not implement the application, package the candidate, author Backend evidence, or remediate any code. The assignment and observed authorship separation establish VALID independence; no external signed session attestation is claimed.

Reviewed revision: **`78fa5b87b156c1201525d3b097fe68f3c46b9d62fe829dd7087dfa80d8b56695`**, the SHA-256 of `revision/artifact-sha256.txt`, **not a Git commit**. The containing foundation repository HEAD (`adbea9fab587c5d12dfa25f6ff25240482e3fcbf`) is not the application revision.

Scope: GET /api/customers and its implicit HEAD behavior, authentication middleware, FormRequest/Gate, models, serializer, provider, route/bootstrap configuration, migrations, tests and dependency lock. Domain: disposable synthetic fixtures, administrator-global customer visibility, in-process requests, SQLite memory database. No owner or tenant domain exists. This review does not certify unrelated owner/tenant evaluation fixtures, production readiness, or real HTTP transport.

Foundation 0.5.0; Security Agent Foundation v0.1; Laravel 13.32.0. Governing policy bytes are part of the 77-file candidate inventory. The workspace has no `.ai/` directory; the requested `.ai/foundation/security/*`, shared baseline/development policies, and project context were read directly from the verified archive, not substituted with current repository policies. Also reviewed frozen architecture, commands, overrides, human-approval policy and output standards.

## Integrity and reconstruction

| Check | Independent observation |
|---|---|
| Package manifest digest | PASS; `package-sha256.digest` matches manifest bytes |
| Package references | PASS; all 27 manifest entries match |
| Candidate identity | PASS; inventory hash equals candidate ID |
| Archived source | PASS; all 77 entries match inventory |
| Original sandbox | PASS; all 77 entries match before and after execution |
| Executed candidate copy | PASS; all 77 entries still match after execution |
| Changed-file inventory | 14 files; reviewed implementation and stored baseline diff |
| Supplemental runtime | Current sandbox vendor/scaffold files copied byte-for-byte, separately hashed in `runtime-provenance.json` |
| Dependency consistency | All 110 installed package versions match the frozen lockfile |

The archive provides sufficient exact source to inspect this candidate uniquely. Its deliberate omission of dependencies and scaffold configuration does not make the candidate identity ambiguous. Execution uses supplemental runtime evidence with separate provenance; the reports do not pretend these files were attested at the original Backend test time. The package is tamper-evident, not signed or immutable.

Only files under this Security directory were written. No application implementation, original sandbox, Backend report, policy or frozen package was edited. The temporary runtime copy was removed after verification; its provenance manifest, test results and reviewer test source remain. The inherited handoff README remains unchanged as historical packaging evidence.

## Evidence and methodology

Read `input/story.md`, all acceptance criteria and frozen project security context; all three Backend handoff reports; the source archive, inventory, changed-files list, implementation diff and package verification records. Backend's PASS statements were treated as claims. Their source tests and relevant actual application source were inspected before independently executing them.

Directly inspected the complete candidate PHP source/configuration/tests, composer manifest and locked dependency metadata. Read supplemental `config/auth.php`, `config/logging.php` and the framework Basic authentication/password-check implementation. The configured web guard uses Eloquent User; `onceBasic()` derives credentials from the request and checks them on each attempt; password validation uses the configured hasher. No application-specific authentication algorithm was introduced.

Evidence files in this directory:

| File | Purpose |
|---|---|
| `integrity-verification.json` | Final package, source and copy integrity results, reviewer identity and UTC timestamp |
| `runtime-provenance.json` | SHA-256 inventory of supplemental runtime files and source location |
| `independent-tests.txt`, `independent-junit.xml` | Independent execution of the 35 frozen tests |
| `SecurityBoundaryTest.php` | Five additional reviewer-authored verification tests, not application code |
| `boundary-tests.txt`, `boundary-junit.xml` | Independent additional test results |
| `dependency-audit.json`, `dependency-audit-stderr.txt` | Initial restricted-network attempt; lookup failed, not a clean scan |
| `dependency-audit-retry.json`, `dependency-audit-retry-stderr.txt` | Successful advisory lookup; no advisories or abandoned packages |

Execution arrangement: create an unchanged copy of the archived candidate under `security/verification-runtime`; copy only vendor, omitted config, resources, providers and artisan from the original sandbox, with per-file hashes. Do not copy `.env`, database, logs, Git, or existing bootstrap caches. Create empty local storage and bootstrap cache directories. Use a cleared environment, explicit PHP 8.3, memory SQLite, array cache/session/mail and local temporary directories. No listener, worker or external application integration ran. Only additive migrations ran against fresh memory databases. Reviewer tests generate credentials in memory; reports contain none.

Commands actually executed (paths abbreviated to directory-relative form; same flags and isolation):

```sh
# From verification-runtime; shell PWD points to this Security-owned copy.
env -i PATH=/opt/homebrew/opt/php@8.3/bin:/usr/bin:/bin TMPDIR="$PWD/tmp" \
 APP_ENV=testing APP_DEBUG=false APP_URL=http://localhost \
 DB_CONNECTION=sqlite DB_DATABASE=:memory: DB_URL= CACHE_STORE=array \
 SESSION_DRIVER=array QUEUE_CONNECTION=sync MAIL_MAILER=array \
 /opt/homebrew/opt/php@8.3/bin/php -d sys_temp_dir="$PWD/tmp" \
 vendor/bin/phpunit --do-not-cache-result --log-junit ../independent-junit.xml

# Additional test execution used the same cleared environment, from repository root.
# S denotes validation/runs/US-BE-001/security in the path arguments below.
/opt/homebrew/opt/php@8.3/bin/php -d sys_temp_dir="$PWD/$S/verification-runtime/tmp" \
 "$S/verification-runtime/vendor/bin/phpunit" -c "$S/verification-runtime/phpunit.xml" \
 --do-not-cache-result --log-junit "$S/boundary-junit.xml" "$S/SecurityBoundaryTest.php"

# Successful advisory retry, from verification-runtime; public registry access.
env -i PATH=/opt/homebrew/opt/php@8.3/bin:/usr/bin:/bin TMPDIR="$PWD/tmp" \
 COMPOSER_HOME="$PWD/tmp/composer" COMPOSER_CACHE_DIR="$PWD/tmp/composer-cache" \
 /opt/homebrew/opt/php@8.3/bin/php -d sys_temp_dir="$PWD/tmp" \
 '/Users/mouhssinesoumairi/Library/Application Support/Herd/bin/composer' \
 --no-plugins --no-scripts audit --locked --format=json
```

Hash verification used Python `hashlib.sha256`, `tarfile` reads and byte comparisons for each manifest entry. The initial Composer attempt could not resolve repo.packagist.org and reported an unwritable default temp directory. A network-authorized retry with an explicit Security-local temp directory exited 0. No dependency update/install, Composer hook or plugin was executed.

## Access matrix and independent negative verification

| Actor / operation | Expected | Observed |
|---|---|---|
| Anonymous GET or invalid credentials | 401, no customer data | PASS |
| Authenticated ordinary user GET | 403, no records or counts | PASS |
| Ordinary user with role/owner/tenant query spoofing | 403, no elevation or data | PASS; role remains false, customer count unchanged |
| Administrator GET | 200, global synthetic list, four public fields | PASS |
| Administrator invalid/hostile/protected parameters | 422, no state changes | PASS across 20 frozen cases |
| Anonymous / ordinary / admin HEAD | 401 / 403 / 200 | PASS in additional test |
| Admin POST / PUT / PATCH / DELETE | 405, no mutation | PASS; customer snapshot and ordinary role unchanged |
| Repeated anonymous attempts | First 60 denied at auth; 61st throttled | PASS |
| Rotating X-Forwarded-For / Forwarded headers | Cannot bypass loopback limit | PASS; 61st request 429 |
| Ordinary user sends admin flag in GET JSON body | 403, no elevation | PASS |
| Admin GET body supplies oversized page size or tenant field | 422 | PASS |
| Forced synthetic database-event exception | 500 JSON, no internal exception marker or trace | PASS |
| Owner/non-owner and cross-tenant actors | Not applicable to defined global-admin domain | No tenant-isolation claim |

Existing tests: **35 / 437 assertions**, zero failures/errors/skips. Additional tests: **5 / 97 assertions**, zero failures/errors/skips. PHP 8.3.33 / PHPUnit 12.5.35. The additional exception test injects a test-only listener; it does not modify application source or weaken authentication. Its internal marker is synthetic. The independent rerun establishes present behavior on the verified candidate copy, not a retrospective attestation of Backend's original run.

## Complete vulnerability checklist

VERIFIED means supported by inspected source and/or the stated execution within the sandbox boundary; it is not a claim of exhaustive exploitation resistance. All source references below are candidate-relative unless marked supplemental. `T` = `tests/Feature/ListCustomersTest.php`; `B` = retained `SecurityBoundaryTest.php`.

| Review area | Outcome | Evidence and boundary |
|---|---|---|
| Authentication | VERIFIED | `routes/api.php:7-8`, middleware `:14-23`; T:71-82; real framework credentials, generic 401 |
| Authorization | VERIFIED | provider `:27`, request `:12-19`; T:84-90,159-168; B HEAD/body cases |
| Object-level authorization | VERIFIED | Frozen architecture grants only administrators all synthetic customers; ordinary actors cannot list records/counts; T:84-90. Owner/tenant subcases not applicable |
| BOLA / IDOR | VERIFIED | No customer-ID route or relationship resolver; owner/tenant substitutions rejected, unauthorized list denied; T:84-90,111-129 |
| Privilege escalation | VERIFIED | Trusted boolean Gate; default false migration `:12`; User fillable excludes is_admin; T:84-90,153-157; B body spoofing |
| Endpoint exposure | VERIFIED | Route/bootstrap inventory: GET/HEAD customers; scaffold `/`, `/up`; no customer writes, registration or admin/debug endpoint; B verifies all write methods |
| Server-side input validation | VERIFIED | Request `:22-36`: integer/range and unknown-key allowlist; T:111-129; B GET-body ambiguity checked |
| API schema validation | VERIFIED | Controller `:14-20`, Resource `:10-17`; T:59-68 confirms exact four keys; metadata only authorized |
| Injection | VERIFIED | Eloquent fixed columns/order and validated integer casts, no raw SQL/command/template concatenation; T hostile SQL/sort cases |
| Parameter tampering | VERIFIED | Query/body protected fields and bounds rejected; T:84-90,111-129; B body tests |
| Mass assignment | VERIFIED | No write path; User allowlist, Customer guarded all; T:153-157; protected role unchanged |
| JWT/token security | NOT_APPLICABLE | No token scheme on this operation |
| Password and credential handling | VERIFIED | User hashed cast; supplemental EloquentUserProvider uses hasher check; generated test credentials; no recovery/rotation endpoint added. Test bcrypt rounds are fixture settings |
| Rate limiting | VERIFIED | Provider `:28`, route order throttle before Basic; T:132-138; B header-spoof attempts. Array cache verified only within the in-process fixture |
| Abuse protection | VERIFIED | Authentication cost limited per loopback client, bounded page/size; T throttling and bounds; no distributed service claim |
| CORS | VERIFIED | `config/cors.php`: empty origin allowlist, GET only, credentials false; T:147-150; not relied on for authorization |
| Secrets and environment variables | VERIFIED | Inspected changed source and test runner; random fixture credentials, no source credential values; cleared execution environment, no `.env` copied. No external secret inventory claim |
| Sensitive-data exposure | VERIFIED | Selected columns plus explicit Resource; T:59-68,182-192 excludes internal marker/column and password; denied callers receive no data/meta |
| Logs | VERIFIED | Middleware logs constant endpoint; denied authorization logs numeric user ID/endpoint; T:159-179 checks redaction. No request body, credential or arbitrary query logged by these events |
| Secure error handling | VERIFIED | Bootstrap JSON callback, test debug false; 401/403/422/429/405 checks; B forced 500 excludes internal marker/trace |
| File-upload security | NOT_APPLICABLE | No upload/storage/processing operation |
| Database access | VERIFIED | Selected-column Eloquent read and count; guarded model; memory SQLite setup checks; T:182-192 observes two customer queries, no N+1 |
| Least privilege | VERIFIED | Isolated synthetic memory DB, no inherited credentials or integrations; all execution writes confined to Security copy; no production service/database permissions claim |
| Query/resource limits | VERIFIED | Page 1..1000, size 1..100, offset <=99900; T pagination/throttle/query checks. Exact count remains dataset-dependent; concurrency/scale outside sandbox scope |
| Data integrity | VERIFIED | Read-only controller; T compares full customer snapshots on hostile inputs; B all write methods preserve snapshot and role |
| Transactional consistency | NOT_APPLICABLE | No multi-step writes or transactional business operation; stable traversal tested on static fixtures, not concurrent-snapshot semantics |
| Logging | VERIFIED | Authentication/authorization denial events independently captured; authorization includes actor ID. Local sink inspected. Operational retention/access administration excluded from in-process scope |
| Monitoring | NOT_APPLICABLE | Frozen scope explicitly excludes deployment monitoring; no deployed service, alert path or operational monitor to certify |
| Auditability | VERIFIED | Denied authorization has actor ID and fixed operation; authentication failure has fixed endpoint, without identity disclosure. Tests verify these limited technical events; production attribution/retention not claimed |
| Dependency security | VERIFIED | Frozen lock reviewed; 110 installed versions match; independent Composer audit 2026-09-17 returned empty advisories/abandoned lists. No new story dependency; point-in-time known-advisory coverage only |
| HTTPS/TLS | NOT_APPLICABLE | No network listener; in-process fixture cannot expose Basic credentials in transit. Real HTTP use requires separate TLS/authentication review |
| Production security configuration | NOT_APPLICABLE | No production target or release clearance. Testing debug false and env isolation verified; supplemental runtime config not a production attestation |
| SSRF | NOT_APPLICABLE | No URL input, outbound call or redirect-fetch boundary |
| Replay | NOT_APPLICABLE | Repeated read is intended; no sensitive write, transaction or nonce contract |
| Brute force | VERIFIED | Pre-authentication limiter exercised; forwarded-header rotation ineffective in fixture; distributed guessing and real server deployment excluded |
| Information leakage | VERIFIED | Generic auth errors, no denied records/counts, strict output fields; B internal 500 marker absent; no timing-side-channel guarantee |
| Enumeration | VERIFIED | Ordinary/anonymous callers cannot enumerate customer existence/counts; admin enumeration expressly permitted by access matrix |
| Abuse scenarios | VERIFIED | Combined role/tenant spoofing, malicious pagination, GET body tampering, method alternatives and forwarded-header throttle attempts executed; persistent fixture state assertions passed |

Pagination checks also covered default size 20, min 1, max 100, three-page traversal of 250 fixtures without duplicates and empty page 1000. This does not establish snapshot consistency under concurrent external writes or a production query-time bound.

## Findings and gate

**No confirmed Critical, High, Medium or Low security findings.** `findings.json` therefore contains an empty findings array; no finding was downgraded, closed or accepted as risk. There is no remediation history to invent.

**Security Gate: PASS**, corresponding to Foundation **ELIGIBLE FOR HUMAN REVIEW**, for this candidate and the defined sandbox only. No required in-scope technical verification remains unavailable. The absence of production/tenant assurances is an explicit domain exclusion, not an unverified control being labelled successful.

The frozen context says no security event sink is claimed, while final source emits denial events and the supplemental default logging configuration routes to local storage. Independent tests confirm actual redacted events. This stale description is retained and disclosed; it is not used to dismiss the code, claim deployed monitoring, or manufacture a vulnerability. Audit should evaluate the evidence inconsistency and the previously disclosed process sequencing separately.

## Limitations and handoff

- The frozen candidate includes only 77 inventoried files. Supplemental runtime hashes establish what this review used today, not what Backend executed historically; matching installed versions is not cryptographic attestation of every upstream dependency's distribution bytes.
- Package integrity relies on local SHA-256 manifests, without an external signer or immutable storage. Independence rests on the explicit new-context assignment and this review's authorship record.
- In-process PHP tests do not validate web-server Basic header forwarding, HTTPS, persistent rate limiting across processes, proxy deployments, operational log retention/alerts, production DB privileges or production-scale concurrency. Any such use changes the review scope and requires new evidence.
- Dependency advisory results are time-sensitive and cover known registry advisories, not undisclosed vulnerabilities. The first failed lookup is retained separately so it cannot be mistaken for a successful scan.
- No source mutation/sensitivity campaign was run because application changes were prohibited. Additional negative tests independently challenged controls without altering implementation.
- No live or production data, services or resources were used. No code remediation, external report delivery, merge, deployment, Audit completion or human approval occurred.

Required actions: independent Audit review of evidence/traceability, then final human acceptance. Before changing the candidate or expanding to real HTTP/deployment use, obtain renewed Security verification of affected boundaries. **READY FOR INDEPENDENT AUDIT REVIEW.**
