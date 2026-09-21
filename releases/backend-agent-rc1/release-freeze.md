# RC1 release freeze

Foundation 0.6.1 remains unchanged. [release-freeze.json](release-freeze.json) records the campaign-pinned governed inventory SHA-256, Backend Core and Laravel profile references, adapter manifest reference, campaign reference, release manifest hash, all release/template/document hashes and historical evidence hashes. Paths are repository-relative; hashes are SHA-256 of exact file bytes. The freeze JSON excludes itself to avoid a circular hash; [release-freeze.sha256](release-freeze.sha256) pins it separately. Preserve that checksum externally when approving the release commit. Hashes detect drift; they do not authenticate approvers.

Verification: compare every recorded path/hash, check the freeze JSON against its sidecar, and run `python3 -B evals/backend/freeze.py check --expected-sha256 41948468644c73d9791729354b3abb2e63bc04fc8d25812d96ac22ea0296af92`. Missing/extra release artifacts or mismatched inputs block use. Historical outcomes must not be rewritten.

No silent edits after this freeze. Any material change requires RC2 or a new Foundation version; Foundation changes require their applicable versioning/revalidation process. Pilot-specific copies of templates may be filled in the consuming project without changing this release.

Suggested tag only, after human review and committing this exact verified package:

```sh
git tag -a backend-agent-rc1 <reviewed-release-commit> -m "Backend Agent RC1 — Foundation 0.6.1 — controlled pilot only"
```

Replace the placeholder with the commit containing the verified package, not the pre-packaging source commit. No tag was created or pushed. This freeze is not project authorization, human code acceptance, Audit clearance or production authorization.
