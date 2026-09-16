# Explicit dispatch/content inventory: no recursive copy of arbitrary files or secrets.
sources=(); destinations=()
add() { sources+=("$1"); destinations+=("$2"); }
add_group() {
    local src=$1 dst=$2 name
    shift 2
    for name in "$@"; do add "$src/$name" "$dst/$name"; done
}
configure_backend_laravel() {
    add VERSION foundation/VERSION
    add_group shared foundation/shared engineering-principles.md security-baseline.md security-development-policy.md git-policy.md human-approval-policy.md audit-policy.md output-standards.md
    add agents/backend/README.md foundation/backend/README.md
    add_group agents/backend/core foundation/backend/core agent.md responsibilities.md workflow.md guardrails.md definition-of-done.md output-contract.md
    add_group agents/backend/prompts foundation/backend/prompts analyze.md plan.md implement.md test.md self-review.md
    add_group agents/backend/stacks/laravel foundation/backend/laravel README.md architecture.md coding-rules.md security-rules.md testing-rules.md database-rules.md api-rules.md commands.md
    add_group agents/security foundation/security README.md agent.md workflow.md guardrails.md vulnerability-checklist.md output-contract.md
    add_group agents/audit foundation/audit README.md agent.md workflow.md guardrails.md evidence-policy.md audit-checklist.md audit-report-template.md
}

render_source() {
    local src=$1
    # Adjust only relative link destinations for the compact install layout.
    case "$src" in
        agents/backend/stacks/laravel/*)
            sed -e 's|](../../core/|](../core/|g' -e 's|](../../README.md)|](../README.md)|g' -e 's|](../../../../shared/|](../../shared/|g' "$source_root/$src" ;;
        agents/backend/core/*|agents/backend/prompts/*)
            sed -e 's|](../../../shared/|](../../shared/|g' -e 's|](../../../README.md#|](../../README.md#|g' "$source_root/$src" ;;
        agents/backend/README.md|agents/security/*|agents/audit/*)
            sed -e 's|](../../shared/|](../shared/|g' -e 's|](../../README.md#|](../README.md#|g' -e 's|](stacks/laravel/|](laravel/|g' "$source_root/$src" ;;
        *) cat "$source_root/$src" ;;
    esac
}

foundation_index() {
    printf '# Installed Foundation\n\nRead [Backend](backend/README.md), [Laravel](backend/laravel/README.md), [Security](security/README.md) and [Audit](audit/README.md).\n\n## Shared policy map\n\n'
    for policy in engineering-principles security-baseline security-development-policy git-policy human-approval-policy audit-policy output-standards; do
        printf -- '- [%s](shared/%s.md)\n' "$policy" "$policy"
    done
}

# Use platform SHA-256 tools without introducing a runtime dependency to bootstrap.
foundation_checksums() (
    cd -- "$1"
    local file
    if command -v sha256sum >/dev/null 2>&1; then
        hash_command=(sha256sum)
    elif command -v shasum >/dev/null 2>&1; then
        hash_command=(shasum -a 256)
    else
        printf 'Warning: no SHA-256 tool available; integrity checksums not generated.\n' >&2
        return 1
    fi
    find . -type f ! -path './checksums.sha256' -print0 |
        while IFS= read -r -d '' file; do "${hash_command[@]}" "$file" || exit 1; done |
        LC_ALL=C sort
)

# Validate each component, so a linked source directory cannot redirect reads.
check_source() {
    local rel=$1 current=$source_root part
    local -a components
    IFS=/ read -r -a components <<< "$rel"
    for part in "${components[@]}"; do
        current="$current/$part"
        [ ! -L "$current" ] || fail "Symbolic source is not allowed: $rel"
    done
    [ -f "$current" ] && [ -r "$current" ] || fail "Missing or unreadable source file: $rel"
}
