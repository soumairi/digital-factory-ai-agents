# Evaluation governed inventory (Foundation 0.6.1)

## Previous model and classification

Before 0.6.1, Laravel `runner.check_assets()` recursively hashed every file beneath `evals/backend/adapters/laravel/`, except the checksum inventory itself, and compared the exact path/hash map with `checksums.json`. A new Python bytecode file therefore failed the comparison. That check did not cover the original specifications, outer verifier/schema or Foundation policy; campaigns separately recorded tracked-file inventories. BACKEND-EVAL-003 used that historical model and remains INVALID. Restoring its directory did not cure the recorded event.

| Class | Contents | Freeze treatment |
|---|---|---|
| Governed assets | Original evaluation specifications, Laravel code/calibration scaffolding, fixtures, reviewer tests, verification scripts, fault definitions, manifests, expected results, schema, freeze code, framework tests, Backend Core/Laravel profile, Security/Audit/shared policies, version and evaluation/versioning documentation | Explicit path, asset type, SHA-256 and Foundation reference in `evals/backend/governed-inventory.json` |
| Generated evidence | Candidate snapshots, test/JUnit output, reviews and campaign reports in authorized `validation/` locations or disposable workspaces | Outside governed input roots; independently hashed by evidence manifests, never silently incorporated into the asset snapshot |
| Ephemeral runtime artifacts | Narrow cache/output exceptions below | Not governed; may be created without changing the snapshot or its digest |

The exact governed directories and individual policy files are declared in `evals/backend/freeze.py` (`DIRECTORIES`, `FILES`). Every current non-ephemeral file in those scopes is individually listed. Root VERSION, README, CHANGELOG, the protocol and this policy are governed. The inventory does not hash itself; the coordinator pins its SHA-256 externally before campaign implementation. The Foundation reference applies to every entry; adapter/fixture versions remain explicitly recorded in the governed adapter manifests. Candidate/runtime/dependency integrity checks are separate and unchanged.

## Narrow exceptions and prohibited additions

Only `.pyc` files, `.DS_Store`, `.coverage`, known pytest cache data names (`CACHEDIR.TAG`, `.gitignore`, `nodeids`, `lastfailed`, `stepwise` inside `.pytest_cache`), and `.log`/`.txt` output beneath a `tmp` path component are ignored. An empty `__pycache__` directory has no asset bytes; normal `.pyc` contents are ignored. Symlinks are prohibited even when their names look ephemeral.

There is no blanket exclusion of `__pycache__/`, `.pytest_cache/`, `coverage/`, `tmp/`, logs, hidden files or extensions other than the ones listed. Python, shell, PHP, JSON, Markdown, YAML, TOML, INI and XML files are never excluded by directory name. For example, `tmp/fixture.json`, `__pycache__/hidden.py`, and `.pytest_cache/README.md` are prohibited undeclared additions. Put ordinary coverage reports, XML/JUnit and other generated reports outside governed roots. Runtime exceptions never permit a declared governed asset to bypass validation; inconsistent inventory entries fail closed.

An unlisted non-ephemeral file within a declared governed scope is a prohibited artifact: validation fails until a reviewed, prospective inventory update occurs. An unrelated file outside those scopes does not modify the frozen snapshot. Future execution must not import/run new code from outside declared governed assets (apart from separately pinned candidate/dependency artifacts). An inventory entry deletion, missing file, changed bytes or type/reference, unsafe path, symlink or new governed file fails validation.

## Validation and lifecycle

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B evals/backend/freeze.py check
python3 -B evals/backend/freeze.py check --expected-sha256 PINNED_INVENTORY_SHA256
python3 -B evals/backend/adapters/laravel/runner.py check-freeze
```

The runner now returns the governed inventory digest and pins it in disposable workspace state. Clean/fault verification compares that digest to the original workspace pin as well as checking all governed asset bytes. A coordinator must also preserve an external campaign pin before implementation; it must not accept an in-campaign rebuild as a new baseline. Run checks at campaign boundaries and before/after verification. Rewriting both files and inventory cannot bypass an existing digest pin. Hashes alone do not authenticate review or detect a transient malicious mutation restored between checks; use read-only mounts/permissions where available. Cleanup is never evidence that no governed mutation occurred.

`python3 -B evals/backend/freeze.py build` is a maintainer operation for reviewed framework changes outside active campaigns, not recovery from a campaign violation. `checksums.json` remains a governed adapter-only compatibility inventory; the new declared inventory is authoritative for campaign freeze validation. Neither inventory is auto-refreshed by check/setup/verify/fault execution. Review any inventory diff with its source diff. Current adapter verification hashes and compatibility checksums are refreshed for this framework patch; prior independent review records remain pinned to their original bytes and do not certify the changed runner.

Use `python3 -B` or set `PYTHONDONTWRITEBYTECODE=1` **before** starting Python, including unit-test discovery and imports. Shell adapter entrypoints already use `-B`; the runner's sanitized subprocess environment also disables bytecode. Python imports loaded by the freeze bridge disable bytecode. Tolerance for incidental runtime artifacts is the correctness guarantee; prevention is additional hygiene, not a cleanup-based guarantee.

## Version and historical boundary

0.6.1 is a compatible governance correction under the repository patch-version policy: case criteria, oracle assertions, fault semantics and candidate/evidence result schema are unchanged. The new inventory has schema version 1; consumers that manually inspect the old raw adapter digest must adopt the new campaign digest and policy prospectively. No historical campaign/evidence is migrated or rescored. BACKEND-EVAL-001, 002 and INVALID 003 are preserved. Framework tests are not a Backend campaign, calibration run, Release Candidate, pilot or deployment. A future campaign still requires explicit authorization and reviewer adoption of the new freeze.
