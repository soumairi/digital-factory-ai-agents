# Architecture
Observed Laravel 13 skeleton: bootstrap/app.php registers routes; AppServiceProvider is the project provider; User uses standard Eloquent authentication and guarded attributes. No API route, customer domain, third-party authentication or repository pattern exists.
Planned boundary: routes/api.php -> throttle -> stateless framework Basic authentication -> FormRequest/Gate -> thin list controller -> Eloquent -> explicit JsonResource.
Customer has no tenant or owner: all records are administrator-only synthetic fixtures. There are no writes, relationships, external calls or multi-step transactions on this endpoint. Stable ascending ID ordering.

# Security context
Access matrix: anonymous/invalid credentials -> 401; authenticated non-admin -> 403; server-provisioned admin -> 200, all synthetic customers. Query parameters cannot grant privileges.
Authentication: existing web guard/user provider, Auth::onceBasic; no custom token scheme, no login/registration endpoint. Basic credentials are randomly generated in memory by tests and never reported. No network listener. Any future real HTTP use requires separately reviewed TLS/authentication design.
Input: only page (1..1000) and per_page (1..100), default 1/20; integer validation; unknown keys -> 422; arrays, hostile strings and protected fields rejected. JSON errors, debug false.
Resource controls: 60 requests/minute per loopback test client before authentication (also bounds password checks); maximum offset 99900, no unbounded response; stable ordering. Scale/production load testing excluded.
Output allowlist: id/name/email/created_at. Synthetic internal_notes must never appear. No full request or credentials in logs. Framework errors redacted with debug false. No security event sink claimed; denied statuses tested, deployment monitoring out of scope.
SQLite in-memory only, array cache/session/mail, sync queue unused; no outbound application integrations. No uploads/JWT/replay-sensitive writes/SSRF surface. Medium/Low findings require remediation or human disposition; no agent risk acceptance.
Independent review pending assignment. Production access prohibited.

## Analysis and AC mapping
AC1 route/controller; AC2-3 framework credentials + Gate; AC4-5 bounded stable paginate; AC6-7 selected columns + Resource; AC8-9 strict FormRequest; AC10 feature tests; AC11 core checklist/self-review + separate reviewers; AC12 env-cleared :memory: runner.
Risks: credential brute force (pre-auth throttle), role tampering (trusted DB flag and reject unknown keys), BOLA/list enumeration (admin gate; no tenant domain), mass assignment (no writes), SQL injection (no raw query or client sort), leakage (resource allowlist and debug false), resource abuse (page/per_page bounds), safe errors (JSON).
Files: bootstrap/app.php, routes/api.php, AppServiceProvider, User cast, authentication middleware, request/controller/resource/Customer, additive migration, feature tests, isolated runner/phpunit settings. No additional dependencies.
Plan: implement these minimal components, run synthetic credential/role/input/pagination/schema/throttle tests, retain first results, self-review full diff, obtain independent Security/Audit or explicitly block clearance, score only evidenced adaptations.
