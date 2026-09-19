# Version consistency before framework edits

| Item | Version |
|---|---|
| Repository current VERSION at task start | 0.5.0 |
| Run #2 Foundation | 0.5.0; baseline adbea9fab587c5d12dfa25f6ff25240482e3fcbf |
| Evaluation Campaign Foundation | 0.5.0; baseline 2fcae8e04c7c68f7fceb556739c9d852adc23989 |
| Repository after this update | 0.6.0 |

Before any modification, all 94 campaign-frozen Foundation file hashes matched the current repository. `git diff adbea9f..HEAD -- agents shared workflows VERSION CHANGELOG.md` was empty. The campaign therefore did not accidentally run an older Foundation than the repository supplied. The revision IDs differ because validation evidence/preparation was committed, not because the policies/version changed.

CHANGELOG.md records filesystem bootstrap under Unreleased while VERSION remained 0.5.0. Run #2 evidence contains process preflight, authorization and separated execution-context records. No tracked change or explicit version decision labelled “Prompt 9.2” or “Process Hardening” was located. These facts do not establish an intentional Foundation-policy hardening release held at 0.5.0; that provenance is unconfirmed. No such intent is invented and no historical snapshot is rewritten.

The new 0.6.0 increment is justified by reusable reviewer contracts, versioned manifest schema and executable gate checks—not improved scores. Original criteria/weights and shared policies stay unchanged. The shipped legacy project-template/FOUNDATION_VERSION is aligned to the new template release; script-managed installed-version authority remains .ai/foundation/VERSION. Installed project manifests are not edited.

Historical BACKEND-EVAL-001 remains 0 PASS / 0 FAIL / 9 PARTIAL. Its hashes continue to attest the old frozen bytes; a historical checker comparing that snapshot to today's changed Foundation would naturally differ. No retroactive validator run, campaign execution, Release Candidate or pilot is performed.
