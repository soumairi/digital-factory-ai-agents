# Stop and rollback

Immediately STOP affected work on any Critical security issue, unresolved High issue, production access outside authorization, real secret exposure, real customer data exposure, Foundation drift, adapter/evaluator drift, missing human authorization, missing evidence, candidate hash mismatch, Security/Audit independence failure, or destructive operation outside scope.

Preserve the failing state and evidence, restrict further execution, and notify the named human owner through the project's approved process. Do not continue on a newly generated baseline.

The authorized human-led rollback process must:

1. Restore the recorded repository baseline without erasing incident evidence.
2. Revoke temporary credentials through the authorized credential owner.
3. Remove temporary sandbox resources within approved cleanup scope.
4. Preserve logs, candidate hashes, findings and approval records.
5. Document the incident, impact, containment and recovery checks.
6. Require human review before resuming, plus independent Security/Audit clearance where applicable.

Destructive rollback, credential changes and shared-environment changes require specific authorization under [Human approval policy](../../shared/human-approval-policy.md). A stop criterion does not grant those permissions. Material changes to the frozen release require RC2 or a new Foundation version.
