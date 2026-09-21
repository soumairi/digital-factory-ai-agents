# Known limitations

1. PostgreSQL not validated; target-engine validation is required before any PostgreSQL pilot, including database-sensitive stories.
2. Results apply only to the tested Laravel/SQLite scope; other stacks are not validated.
3. External containment is required for untrusted code; the runner is not a security sandbox.
4. Shared scaffold and fixed mutation anchors limit generalization beyond tested cases.
5. Production TLS/transport was not validated by this sandbox campaign.
6. Production monitoring was not validated.
7. Distributed rate limiting was not validated.
8. Human oversight remains mandatory; campaign human code review and Audit were not completed.
9. Reviewer separation is supported by recorded execution provenance, not cryptographic authentication; boundary hashes cannot exclude transient restored changes.
