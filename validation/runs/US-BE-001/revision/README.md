# Frozen candidate identity

| Record | Value |
| --- | --- |
| Candidate ID | `78fa5b87b156c1201525d3b097fe68f3c46b9d62fe829dd7087dfa80d8b56695` |
| Meaning | SHA-256 of the original artifact-sha256.txt bytes; not a Git commit |
| Foundation / framework | 0.5.0 / Laravel 13.32.0 |
| Original sandbox | `/private/tmp/digital-factory-laravel-agent-sandbox-phWIwZ/app` |
| Preserved candidate | [candidate.tar.gz](candidate.tar.gz), 77 previously hashed files |
| Changes | [changed-files.json](changed-files.json), 14 files |
| Diff | [implementation.diff](implementation.diff), byte-identical to existing evidence |

All original inventory entries were verified against the sandbox before copying. The diff was regenerated **in memory for comparison only** from the existing baseline and candidate and matches byte-for-byte. No implementation or test was regenerated or executed.

The archive preserves only the original inventory's files: application/test sources, lockfile, project context and governing policy documents. It is a compact review snapshot, not a complete runnable Laravel installation; dependencies, unlisted scaffold configuration, databases, logs, .env and credentials are excluded. The full original sandbox remains available read-only for inspection. Do not assume the original inventory covers every dependency or configuration file; additional review inputs require separate provenance.

To verify from the repository root:

```sh
shasum -a 256 -c validation/runs/US-BE-001/revision/package-sha256.txt
```

The manifest covers this package's initial files and the referenced existing evidence. Its own digest is in [package-sha256.digest](package-sha256.digest). After extracting the source archive into a review-only location, verify its files against artifact-sha256.txt before inspection. Do not edit the original sandbox or this frozen candidate. No archive executable bit is granted.

Freeze model: read-only file modes plus SHA-256 verification provide a tamper-evident local snapshot; this is not a signed attestation or write-once storage. Reviewers must verify hashes, never silently refresh them. New Security/Audit outputs are separate and are not included in the initial package manifest. If remediation changes application code, it needs a separately authorized new candidate ID and new tests; this package remains historical.

The original test report and JUnit identify the sandbox and test files. All current inventory hashes and JUnit test-function line references match this candidate. This establishes consistency with the preserved run evidence, not a retrospective cryptographic attestation captured by PHPUnit at execution time. No independent test rerun is claimed.
