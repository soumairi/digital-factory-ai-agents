# Security context
Access matrix: anonymous/invalid credentials -> 401; authenticated non-admin -> 403; server-provisioned admin -> 200, all synthetic customers. Query parameters cannot grant privileges.
Authentication: existing web guard/user provider, Auth::onceBasic; no custom token scheme, no login/registration endpoint. Basic credentials are randomly generated in memory by tests and never reported. No network listener. Any future real HTTP use requires separately reviewed TLS/authentication design.
Input: only page (1..1000) and per_page (1..100), default 1/20; integer validation; unknown keys -> 422; arrays, hostile strings and protected fields rejected. JSON errors, debug false.
Resource controls: 60 requests/minute per loopback test client before authentication (also bounds password checks); maximum offset 99900, no unbounded response; stable ordering. Scale/production load testing excluded.
Output allowlist: id/name/email/created_at. Synthetic internal_notes must never appear. No full request or credentials in logs. Framework errors redacted with debug false. No security event sink claimed; denied statuses tested, deployment monitoring out of scope.
SQLite in-memory only, array cache/session/mail, sync queue unused; no outbound application integrations. No uploads/JWT/replay-sensitive writes/SSRF surface. Medium/Low findings require remediation or human disposition; no agent risk acceptance.
Independent review pending assignment. Production access prohibited.
