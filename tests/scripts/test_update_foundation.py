"""Temporary fixtures only; inject OS failures without production test switches."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch

root = Path(sys.argv[1])
count = 0


def ok(label):
    global count
    count += 1
    print('PASS', label)


def snapshot(path):
    return {str(p.relative_to(path)): (p.stat().st_mode, p.read_bytes() if p.is_file() else None)
            for p in path.rglob('*')}


with tempfile.TemporaryDirectory(prefix='df-update-tests-') as directory:
    work = Path(directory)
    source = work / 'source'
    source.mkdir()
    for name in ('scripts', 'shared', 'agents', 'project-template'):
        shutil.copytree(root / name, source / name)
    (source / 'VERSION').write_text('0.1.0\n')
    (source / 'CHANGELOG.md').write_text('Fixture changes\n')
    project = work / 'project with spaces'
    project.mkdir()
    # A FIFO .env makes an accidental content read hang; timeout detects it.
    os.mkfifo(project / '.env')
    init = source / 'scripts/init-project-agent.sh'
    update = source / 'scripts/update-project-foundation.sh'
    subprocess.run([str(init), 'backend', 'laravel', '.'], cwd=project, check=True, stdout=subprocess.DEVNULL, timeout=30)
    ai = project / '.ai'
    manifest_path = ai / 'agent-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    assert 'foundation_version' not in manifest
    assert not (ai / 'project/FOUNDATION_VERSION').exists()
    manifest['future'] = 'preserve \"quoted\" unicode é'
    manifest['count'] = 42
    manifest['nothing'] = None
    # Simulate the older initializer, including a deliberately stale duplicate.
    manifest['foundation_version'] = '99.0.0'
    (ai / 'project/FOUNDATION_VERSION').write_text('old project-owned value\n')
    manifest_path.write_text(json.dumps(manifest))
    (ai / 'project/project-context.md').write_bytes(b'CUSTOM PROJECT\x00\xff\n')
    context = snapshot(ai / 'project')

    def run(*args, success=True):
        result = subprocess.run([str(update), '.', *args], cwd=project, capture_output=True, text=True, timeout=30)
        assert (result.returncode == 0) == success, result.stdout + result.stderr
        return result.stdout + result.stderr

    assert 'Installed Foundation: 0.1.0' in run()
    ok('fresh installation detected; same version no-op')
    (source / 'VERSION').write_text('0.2.0\n')
    before = snapshot(ai)
    preview = run('--dry-run')
    assert snapshot(ai) == before
    assert 'would create' in preview and 'PRESERVED / NOT MODIFIED' in preview
    print('\nDEMONSTRATION --dry-run:\n' + preview)
    ok('dry-run changes no files or directory entries')
    output = run()
    print('DEMONSTRATION update:\n' + output)
    ok('upgrade succeeds with spaces and dot from another working directory')
    assert snapshot(ai / 'project') == context
    ok('all project bytes and modes preserved, including customized context and legacy version file')
    assert (ai / 'foundation/VERSION').read_text() == '0.2.0\n'
    ok('Foundation VERSION updated')
    current = json.loads(manifest_path.read_text())
    assert 'foundation_version' not in current
    assert current == {k: v for k, v in manifest.items() if k != 'foundation_version'}
    ok('legacy version removed; unknown scalar fields preserved')
    backups = list((ai / 'backups').iterdir())
    assert len(backups) == 1 and (backups[0] / 'VERSION').read_text() == '0.1.0\n'
    assert not (backups[0] / 'project').exists()
    ok('complete previous Foundation backup only')
    for name in ('backend/core/agent.md', 'backend/laravel/README.md', 'security/agent.md', 'audit/agent.md', 'backend/prompts/analyze.md'):
        assert (ai / 'foundation' / name).is_file()
        ok('expected content: ' + name)
    before = snapshot(ai)
    assert 'already up to date' in run()
    assert snapshot(ai) == before
    ok('second update is an immutable no-op')
    edited = ai / 'foundation/backend/core/agent.md'
    edited.write_text('LOCAL EDIT\n')
    before = snapshot(ai)
    detection = run(success=False)
    assert 'Local modifications were detected' in detection and 'backend/core/agent.md' in detection
    assert snapshot(ai) == before
    print('DEMONSTRATION local modification detection:\n' + detection)
    ok('local edits detected and block update without writes')
    forced = run('--force')
    assert any((p / 'backend/core/agent.md').read_text() == 'LOCAL EDIT\n' for p in (ai / 'backups').iterdir())
    assert snapshot(ai / 'project') == context
    print('DEMONSTRATION force:\n' + forced)
    ok('force reinstall retains edited backup and project bytes')
    saved_manifest = manifest_path.read_bytes()
    for label, value in [('invalid JSON', b'{'), ('nested metadata', saved_manifest.replace(b'{', b'{\"nested\": {\"a\": 1},', 1)), ('escaped key', saved_manifest.replace(b'foundation\"', b'foundati\\u006fn\"')), ('trailing comma', saved_manifest.rstrip()[:-1] + b',}'), ('unsupported stack', saved_manifest.replace(b'laravel', b'django')), ('wrong foundation', saved_manifest.replace(b'digital-factory-ai-agents', b'other')), ('duplicate fields', b'{"agent":1,"agent":2}'), ('invalid role', saved_manifest.replace(b'"security_agent": true', b'"security_agent": false'))]:
        manifest_path.write_bytes(value)
        before = snapshot(ai)
        run('--force', success=False)
        assert snapshot(ai) == before
        ok(label + ' rejected without writes')
    manifest_path.write_bytes(saved_manifest)
    installed_file = ai / 'foundation/VERSION'
    saved_version = installed_file.read_bytes()
    for value in (None, b'not-a-version\n'):
        if value is None:
            installed_file.unlink()
        else:
            installed_file.write_bytes(value)
        before = snapshot(ai)
        run('--force', success=False)
        assert snapshot(ai) == before
        installed_file.write_bytes(saved_version)
    ok('missing or invalid authoritative VERSION never falls back to legacy metadata')
    manifest_path.unlink()
    before = snapshot(ai)
    run(success=False)
    assert snapshot(ai) == before
    ok('missing manifest safely rejected')
    manifest_path.write_bytes(saved_manifest)
    os.rename(ai / 'project', work / 'saved-project')
    before = snapshot(ai)
    run(success=False)
    assert snapshot(ai) == before
    os.rename(work / 'saved-project', ai / 'project')
    ok('missing project layer safely rejected')
    required = source / 'agents/security/agent.md'
    saved = required.read_bytes()
    required.unlink()
    before = snapshot(ai)
    run('--force', success=False)
    assert snapshot(ai) == before
    required.write_bytes(saved)
    ok('source preflight failure leaves installation unchanged')
    for name in ('foundation', 'project', 'backups'):
        os.rename(ai / name, work / ('saved-' + name))
        (ai / name).symlink_to(work / ('saved-' + name), target_is_directory=True)
        run('--force', success=False)
        (ai / name).unlink()
        os.rename(work / ('saved-' + name), ai / name)
        ok('symlink rejected: ' + name)
    for target in ('/', ''):
        result = subprocess.run([str(update), target], capture_output=True, timeout=30)
        assert result.returncode != 0
    ok('dangerous targets rejected')
    (ai / 'foundation/checksums.sha256').unlink()
    assert 'NOT verified' in run('--force')
    assert (ai / 'foundation/checksums.sha256').is_file()
    ok('legacy installation upgrades with warning and new checksums')
    (source / 'VERSION').write_text('0.1.0\n')
    assert 'Downgrade refused' in run(success=False)
    run('--force')
    ok('downgrade needs force')
    (source / 'VERSION').write_text('0.3.0\n')
    # Inject filesystem failures using a test-only mv wrapper, never production hooks.
    failure_bin = work / 'failure-bin'
    failure_bin.mkdir()
    real_mv = shutil.which('mv')
    wrapper = failure_bin / 'mv'
    wrapper.write_text("""#!/bin/bash
for arg in "$@"; do
    case "$arg" in
        */.foundation-stage-*/foundation)
            case "$FAILURE" in replacement|rollback) exit 99 ;; signal) kill -TERM "$PPID"; exit 99 ;; esac ;;
        */.foundation-stage-*/agent-manifest.json)
            [ "$FAILURE" != manifest ] || exit 99 ;;
        */.foundation-stage-*/restore)
            [ "$FAILURE" != rollback ] || exit 99 ;;
    esac
done
exec "$REAL_MV" "$@"
""")
    wrapper.chmod(0o755)
    for failure in ('replacement', 'manifest', 'signal'):
        # Legacy metadata removal remains part of the transaction.
        legacy_manifest = json.loads(manifest_path.read_text())
        legacy_manifest['foundation_version'] = 'stale legacy reference'
        manifest_path.write_text(json.dumps(legacy_manifest))
        previous = snapshot(ai / 'foundation')
        metadata = manifest_path.read_bytes()
        with patch.dict(os.environ, {'PATH': str(failure_bin) + os.pathsep + os.environ['PATH'], 'REAL_MV': real_mv, 'FAILURE': failure}):
            diagnostics = run(success=False)
        assert 'Previous Foundation restored.' in diagnostics
        assert snapshot(ai / 'foundation') == previous
        assert manifest_path.read_bytes() == metadata
        assert snapshot(ai / 'project') == context
        ok(failure + ' failure restores previous Foundation/version and preserves manifest/project')
    previous = snapshot(ai / 'foundation')
    with patch.dict(os.environ, {'PATH': str(failure_bin) + os.pathsep + os.environ['PATH'], 'REAL_MV': real_mv, 'FAILURE': 'rollback'}):
        diagnostics = run(success=False)
    assert 'Automatic rollback could not be completed.' in diagnostics
    assert 'Manual recovery required from:' in diagnostics
    stages = list(ai.glob('.foundation-stage-*'))
    assert stages and (stages[0] / 'restore').is_dir()
    os.rename(stages[0] / 'restore', ai / 'foundation')
    shutil.rmtree(stages[0])
    assert snapshot(ai / 'foundation') == previous
    ok('failed rollback explicitly reports recovery and retains recoverable bytes')
    for kind in ('added', 'missing', 'malformed'):
        file = ai / 'foundation/audit/agent.md'
        saved = file.read_bytes()
        checksum_path = ai / 'foundation/checksums.sha256'
        saved_checksums = checksum_path.read_bytes()
        if kind == 'added':
            (ai / 'foundation/extra.md').write_text('extra')
        elif kind == 'missing':
            file.unlink()
        else:
            checksum_path.write_text('0' * 64 + '  ./../../.env\n')
        before = snapshot(ai)
        run(success=False)
        assert snapshot(ai) == before
        if kind == 'added':
            (ai / 'foundation/extra.md').unlink()
        elif kind == 'missing':
            file.write_bytes(saved)
        checksum_path.write_bytes(saved_checksums)
        ok(kind + ' checksum discrepancy rejected without writes or unsafe path reads')
    os.mkfifo(ai / 'foundation/.env')
    assert 'Refusing .env' in run('--force', success=False)
    (ai / 'foundation/.env').unlink()
    ok('Foundation .env rejected by name without opening contents')
    # Unexpected application/network/Git commands fail immediately if invoked.
    bin_dir = work / 'bin'
    bin_dir.mkdir()
    for command in ('git', 'php', 'composer', 'artisan', 'mysql', 'psql', 'curl', 'wget', 'ssh', 'docker', 'node', 'python', 'python3', 'jq'):
        path = bin_dir / command
        path.write_text('#!/bin/sh\necho forbidden-command >&2\nexit 99\n')
        path.chmod(0o755)
    with patch.dict(os.environ, {'PATH': str(bin_dir) + os.pathsep + os.environ['PATH']}):
        run()
    limited_bin = work / 'unix-only-bin'
    limited_bin.mkdir()
    for command in ('bash', 'cat', 'dirname', 'find', 'sort', 'awk', 'diff', 'date', 'mktemp', 'mkdir', 'sed', 'cp', 'mv', 'rm', 'chmod'):
        (limited_bin / command).symlink_to(shutil.which(command))
    hash_tool = 'sha256sum' if shutil.which('sha256sum') else 'shasum'
    (limited_bin / hash_tool).symlink_to(shutil.which(hash_tool))
    isolated = work / 'unix only project'
    isolated.mkdir()
    isolated_env = dict(os.environ, PATH=str(limited_bin))
    assert shutil.which('python3', path=str(limited_bin)) is None
    assert shutil.which('jq', path=str(limited_bin)) is None
    demonstration = subprocess.run([str(init), 'backend', 'laravel', str(isolated)], env=isolated_env, capture_output=True, text=True, timeout=30)
    assert demonstration.returncode == 0, demonstration.stderr
    ok('initialization succeeds with Python/Node/PHP/Composer/jq absent from PATH')
    isolated_context = snapshot(isolated / '.ai/project')
    isolated_manifest = (isolated / '.ai/agent-manifest.json').read_bytes()
    (source / 'VERSION').write_text('0.4.0\n')
    demonstration = subprocess.run([str(update), str(isolated)], env=isolated_env, capture_output=True, text=True, timeout=30)
    assert demonstration.returncode == 0, demonstration.stderr
    print('DEMONSTRATION update with Unix-only PATH (no Python/jq):\n' + demonstration.stdout)
    assert (isolated / '.ai/foundation/VERSION').read_text() == '0.4.0\n'
    assert snapshot(isolated / '.ai/project') == isolated_context
    assert (isolated / '.ai/agent-manifest.json').read_bytes() == isolated_manifest
    assert 'foundation_version' not in json.loads((isolated / '.ai/agent-manifest.json').read_text())
    ok('update succeeds with Python/Node/PHP/Composer/jq absent; project preserved')
    (limited_bin / hash_tool).unlink()
    before = snapshot(isolated / '.ai')
    no_hash = subprocess.run([str(update), str(isolated), '--force'], env=isolated_env, capture_output=True, text=True, timeout=30)
    assert no_hash.returncode != 0 and 'SHA-256' in no_hash.stderr
    assert snapshot(isolated / '.ai') == before
    ok('missing SHA utility fails before any modification')
    for command in ('sha256sum', 'shasum'):
        stub = limited_bin / command
        stub.write_text('#!/bin/bash\nexit 99\n')
        stub.chmod(0o755)
    failed_hash = subprocess.run([str(update), str(isolated), '--force'], env=isolated_env, capture_output=True, text=True, timeout=30)
    assert failed_hash.returncode != 0
    assert snapshot(isolated / '.ai') == before
    ok('checksum command failure cannot silently bypass verification')
    assert (project / '.env').is_fifo()
    ok('unreadable FIFO .env untouched; no application/Git/network/database commands invoked')
    print('\nDEMONSTRATION resulting .ai/ tree:')
    for path in sorted(ai.rglob('*')):
        print('  ' + str(path.relative_to(project)) + ('/' if path.is_dir() else ''))
    print('\nProject layer byte-for-byte preserved:', snapshot(ai / 'project') == context)
    print('Final Foundation version:', (ai / 'foundation/VERSION').read_text().strip())
print('\n' + str(count) + ' update checks passed. All fixtures were temporary and cleaned up.')
