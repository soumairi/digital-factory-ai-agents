# Validated scope

RC1 CONTROLLED PILOT READY — Backend Agent, Foundation 0.6.1, Laravel.

BACKEND-EVAL-004 validated nine original cases covering Laravel backend implementation, server-side validation, authentication/authorization, BOLA/IDOR controls, mass-assignment protections, transaction integrity, pagination/resource bounding, query/N+1 behavior and negative security tests. Separate Security reviews covered all nine candidate hashes. An independent evaluator checked clean behavior and detected all 19 mandatory faults (100% fault sensitivity).

Database: **SQLite validated**. PostgreSQL: **NOT VALIDATED / NOT EXECUTED**. Other stacks: **NOT VALIDATED**. These claims describe tested behaviors, not exhaustive assurance of every Laravel application.

Approved scope is limited to Backend Agent work on Laravel in controlled pilot environments, human-reviewed development workflows, disposable/non-production validation environments, repositories explicitly initialized with the approved Foundation, and required Security/Audit gates.

Excluded: autonomous production changes, production deployment, production secrets, production database writes, unsupervised merge, cloud administration, unreviewed migrations, autonomous incident response and non-Laravel stacks without separate validation. Project authorization is still required; this release neither starts nor approves an individual pilot.

See [campaign details](../../validation/backend-agent-readiness/BACKEND-EVAL-004/detailed/evaluation-detailed-report.md) and [limitations](known-limitations.md).
