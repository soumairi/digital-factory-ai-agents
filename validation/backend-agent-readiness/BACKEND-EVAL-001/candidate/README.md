# Retained disposable candidate

`final/` is source evidence, not a Release Candidate. No vendor dependencies, runtime databases, logs, test passwords or application keys are committed. `source-sha256.json` binds all retained source bytes; `candidate-revision.txt` is SHA-256 of the sorted compact JSON source manifest. `vendor-sha256.json` pins the pre-existing local dependency tree; composer.lock is included, but no package install or lock-to-vendor security audit is claimed.

`initial/` contains the pre-remediation app/routes/tests/preflight overlay. Unchanged base files are in the immutable repository archive `validation/runs/RUN-002-US-BE-001/revision/source` at the campaign Foundation Git revision. `initial-sha256.json` binds the overlay. `implementation.diff` and `changes.json` enumerate final changes relative to that base. Source fixes occurred only in /private/tmp; these copies are review artifacts.

Independent replay: run `python3 campaign/replay.py /path/to/existing/vendor` from the campaign root. The script checks source/vendor hashes, copies into a new disposable /private/tmp directory, and executes the retained full tests and concurrency check with the allowlisted wrapper. Exact PHP path is recorded in runtime.json; a different binary/runtime must be a separately identified replay. No automatic dependencies are installed.

Faults are not in clean source. The eight `evidence/fault-*.patch` files, mutated file hashes, exact filtered commands and logs identify each change. Independent evaluators should own fault selection; replay of same-author patches alone does not fulfill the original BE-009 independence requirement. Assertions frozen before implementation still match the final CampaignTest.php checksum.
