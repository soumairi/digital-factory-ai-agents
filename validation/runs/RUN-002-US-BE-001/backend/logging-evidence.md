# Logging evidence — Backend self-check only

| Topic | Result | Evidence / Limitation |
|---|---|---|
| Authentication failures | PASS | AuthenticateCustomerList logs fixed customers.authentication_denied; missing/invalid tests exercise real guard; exact-argument spy verifies event. |
| Authorization failures | PASS | ListCustomersRequest logs fixed customers.authorization_denied before 403; spy verifies event. |
| Passwords not logged | PASS | No request/credential arguments at either logging call; spy checks exact arity/arguments; synthetic passwords generated in memory and never reported. |
| Tokens not logged | PASS | Synthetic token marker absent from local log; arbitrary query values never included. |
| Secrets not logged | PASS | Synthetic secret marker absent; wrapper app key stays in process environment, no configuration dump. |
| Sensitive payloads not logged | PASS | Internal-notes marker and synthetic admin email absent from log; only fixed denial messages observed. No customer/request payload logged. |
| Local sink inspection | PASS | logging-scan.json: 192 authentication + 3 authorization events across executed attempts; only fixed denial lines. Counts are cumulative, not final-suite-only. Raw log deliberately not copied into evidence. |
| Sandbox monitoring limitation | WARNING | Local single-file sink; no user/IP correlation, collection service, alerts, retention/access-control or cross-process monitoring verified. |
| Production monitoring not claimed | WARNING | No production access, monitoring validation or assurance. Independent Security review pending. |

Evidence: CustomerListTest::test_denial_logs_have_no_request_or_credentials, test-output.txt, implementation middleware/request, and logging-scan.json. Checks establish the tested denial paths only; no universal claim about every framework exception or production infrastructure.
