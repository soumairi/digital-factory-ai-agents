# 9. Update the foundation safely

The installed snapshot’s `.ai/foundation/VERSION` is the authoritative technical version record. It does not encode team approval. A **tag** names a Git revision for a release; a version written in a file does not prove that a corresponding tag has been published. Record the immutable source commit/digest in project-context.md. For initialized projects, use the [local Foundation updater](12-update-project-foundation.md).

```text
Project experience → Identify lesson → Is it reusable?
    No → Keep it in project context
    Yes → Remove project details/secrets → Foundation PR
        → Review → Evaluations → New version + CHANGELOG
        → Human-controlled tag/release → Explicit project adoption
```

A Pull Request (PR) is a proposed change for review. Explain the original problem in generic terms, expected behavior, risks and evaluation evidence. Preserve independent Security/Audit review when controls are affected. The maintainer follows the defined release process; agents do not merge directly or publish implicitly. See [Git policy](../shared/git-policy.md).

## Version numbers in plain language

The [root version policy](../README.md#versioning-and-evolution) governs releases. In `major.minor.patch`, patch means compatible correction, minor means compatible addition, and major means incompatible change. During `0.x`, incompatible changes increment the minor number and are called out explicitly.

Examples, not promised releases: `0.1.0` is an early baseline; `0.1.1` could correct wording compatibly; `0.2.0` could add a role or introduce a documented pre-1.0 incompatibility; `1.0.0` marks a deliberately established stable contract. A higher number alone does not prove better evaluation results.

## Project adoption checklist

1. Read the candidate changelog and policy/core/profile/template differences.
2. Keep the old pinned snapshot and completed project context intact while evaluating the candidate separately.
3. Check additions, conflicts and exceptions against the candidate rule versions; do not automatically carry exceptions forward.
4. Run applicable foundation cases and project regressions with revision-bound evidence. Reassess runtime behavior if tools/models changed too.
5. Obtain human adoption approval through a project PR updating the snapshot/reference and context source record together.
6. Preserve prior evidence and snapshot for an explicit rollback if needed. Review template updates field by field; never overwrite filled project context with a fresh template.

Do not track a moving main branch as the active foundation. Project-specific rules remain local, so a global update does not replace them. If new controls conflict with local behavior, report and resolve the conflict before dependent work; do not silently weaken them to complete an upgrade.
