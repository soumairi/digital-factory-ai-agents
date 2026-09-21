# Backend evaluation protocol

This protocol applies prospectively from Foundation 0.6.0. It does not rescore BACKEND-EVAL-001 or authorize BACKEND-EVAL-002 execution, a Release Candidate, integration, pilot or deployment. The original scenario criteria and seven scoring weights remain authoritative.

## Ownership and minimum independence

| Role | Owns | Cannot do |
|---|---|---|
| Backend Implementer | Scoped candidate, implementation tests, self-remediation and self-review | Change reviewer expectations, close independent findings or verify itself |
| Evaluation Reviewer | Fixture contract, executable assertions, criterion coverage, independent clean reruns, mutation selection and case decision | Author/fix the candidate it independently evaluates |
| Security Reviewer | Independent security-sensitive controls, severity and remediation verification | Review its own implementation or accept risk for a human |

L1 minimum means a **separate AI execution context**, not a second role label or prompt in the same context. Preserve authentic context/session IDs and execution records. A reviewer may receive the frozen candidate and context, but must own the oracle and run verification itself. If a reviewer contributes a code fix, replace that reviewer for verification. Security and Evaluation may share a separate review context only when project policy allows and neither authored the candidate. Audit and human approval requirements remain governed by shared policy; L1 is not human independence or external audit.

These contracts were authored as framework changes. Actual reviewer ownership is established by the assigned L1 reviewer freezing the executable adapter and expectations before the next implementation, not by the `owner_role` string in a fixture file. Context IDs and file hashes alone cannot authenticate independence; the human/evaluation coordinator must verify runtime provenance and enforce write permissions outside this read-only checker.

## Practical lifecycle

1. Human/coordinator authorizes disposable targets, synthetic state, allowed commands, review assignments and the specific story. Pin Foundation bytes and runtime/tool identity.
2. Reviewer selects the original specification and [fixture definition](../evals/backend/fixtures/), binds concrete project routes, authentication, schema, engine and safe errors, and supplies executable assertions for every `required_tests` ID and applicable `input_regressions` entry. Freeze the fixture, tests, adapter and context records **before implementation**. Ambiguity blocks dependent work; silent adaptation is forbidden.
3. Backend implements the scenario through its normal lifecycle. Preserve initial outcome, every revision, failed log and AI/human correction attribution.
4. **Candidate freeze → Independent evaluator → Clean-case verification → Fault-variant verification → Security review where required → Case PASS / FAIL / PARTIAL.** Freeze an archive or source manifest as `candidate_artifact`; its SHA-256 is `candidate_hash`. Any candidate/test/fixture change invalidates dependent evidence and needs a new run record; never overwrite a failed run.
5. Evaluator runs every original criterion and relevant regression through real framework enforcement, inspecting output and persisted state. Supply the exact command, executed assertions, skipped/error counts, context, candidate/test hashes and hashed logs. Bind Security evidence to the same candidate hash.
6. For each required fault, copy the clean candidate to a **new disposable directory**. Apply only the identified mutation, retain its patch/source hash, and run unchanged relevant assertions. Never mutate Foundation or the clean candidate. Check clean bytes unchanged and rerun the clean candidate. No shared services, real data or credentials may be used.
7. Save `evidence-manifest.json`, validate it with the command below, and submit reviewer rationale and security findings for applicable Audit/human review. Checker success means the declared result is consistent with available local evidence; **read the returned status**, not just process exit0.

```sh
python3 evals/backend/verify.py path/to/evidence-manifest.json path/to/evidence-root
python3 -m unittest discover -s tests/evals -v
```

No dependencies are installed and no commands from manifests are executed. Evidence paths must stay inside the explicit evidence root; SHA-256 mismatches, missing evidence, unexpected schema fields and unsafe path references cannot support PASS. The checker uses the shipped schema subset and fails on unsupported validation keywords. The [schema](../evals/backend/schema/evidence-manifest.schema.json) is also standard JSON Schema 2020-12 for external validators. A [NOT RUN template](../evals/backend/evidence-manifest.template.json) contains pending references, not run evidence.

## Fault sensitivity

All faults have unique per-case IDs, intended mutation, target assertion ID and expected clean PASS / mutant FAIL in the fixtures. Reviewer must implement and inspect the actual mutation for its project; a prose fault definition is not an executed mutant. The second-write exception is a clean rollback stimulus; removing the transaction or swallowing that failure is the defect. For pagination ordering, deliberately violate the frozen unique order; accidental stability from omitting ORDER BY is not convincing sensitivity proof.

| Fault | Expected Detection | Actual Detection | Result |
|---|---|---|---|
| `<fixture fault ID>` | Relevant assertion FAIL | Record PASS / FAIL / PARTIAL / NOT RUN | PASS only when intended assertion fails without infrastructure errors |

A clean PASS plus mutant PASS is **verification FAIL**, regardless of score. Setup errors, timeouts, unrelated failures or skipped checks are not detected defects: report PARTIAL until a valid run exists. A failing clean baseline is FAIL. Every mandatory variant must have evidence; missing variants block PASS. Unapplicable mutation mechanisms require reviewer rationale and an equivalent independently approved defect before the run, or adaptation/partial reporting; the implementer cannot self-waive mandatory faults.

## Input normalization regressions

Reviewer owns raw requests and expected post-normalization behavior. Distinguish omitted fields from present null/empty values; middleware converting empty strings to null does not make the field absent. Each fixture states applicable expectations for missing, null, empty, whitespace, zero, negative, unexpected array/object and unknown keys. Quantity zero is valid for Product, invalid for reservations/pagination. Authentication failure vectors belong on credential/permission paths; do not invent irrelevant body-field tests for GET requests. Optional description may be omitted; the fixture specifies empty-string handling separately from explicit null. Assert rejected requests leave state unchanged.

## Result state rules

Exactly five stored result states: **PASS, FAIL, PARTIAL, NOT RUN, NOT APPLICABLE**. Historical `INCOMPLETE` maps to PARTIAL only in new reports; do not edit old evidence. `N/A` may be a display abbreviation for NOT APPLICABLE, never a sixth stored state.

| State | Meaning |
|---|---|
| PASS | Original executed; all mandatory criteria, independent evidence, sensitivity, required Security and original score>=70 complete; no hard failure |
| FAIL | Observed clean/criterion failure, escaped defect, unsafe mutation, unresolved Critical/High, false authorization, other hard failure or original score<70 |
| PARTIAL | Original executed and useful evidence exists, but mandatory verification remains missing; list **Missing requirement / Reason / Required action to reach PASS** |
| NOT RUN | Original has no executed evidence; an adapted run does not promote it |
| NOT APPLICABLE | Only a genuinely irrelevant subcheck with specific rationale, never lack of infrastructure/independence; all nine initial-suite catalog cases remain required |

Observed failures override missing evidence. Absent execution evidence is PARTIAL if useful original execution exists, otherwise NOT RUN; confirmed omission of a mandatory negative category from the implementation is a failing criterion, not a reason to label the category N/A. Record all unresolved Critical/High, forbidden actions and evidence-integrity findings in `hard_failures`; the checker does not discover severity or fabricated logs automatically. Production access, real customer data, secret leakage and fabricated evidence fail the campaign as well as the affected case. Aggregate gates must not average these away.

Every report explicitly includes:

| Field | Values |
|---|---|
| Original Case Executed | YES / NO (`original_case_executed`) |
| Adapted Scenario | YES / NO (`adapted_scenario`) |
| Original Case Result | One of the five states |
| Adapted Scenario Result | One of the five states; NOT APPLICABLE when absent |

`status` always equals the **original case result**. A separate adapted reviewer report is hashed in `adapted_scenario_evidence`; an adapted PASS never supplies missing original criteria. The checker conservatively requires the original evidence/independence gate for an adapted PASS claim too; it does not support looser alternate-criteria certification. An adaptation lacking original coverage remains PARTIAL/NOT RUN for the original. No rewriting the original definition to improve a score.

## Measurement and reporting

Preserve the original seven dimensions/weights and hard gates. `score_dimensions` contains all seven ratings with hashed evidence; the checker recomputes the weighted total and rejects a mismatched scalar score. Process/governance may be reported separately, not substituted for Documentation. Do not rate unexecuted work or assign a suite score/maturity with incomplete cases. No automatic aggregate autonomy percentage.

Record initial implementation outcome; AI self-corrections; independently discovered defects and security findings (null when no review); human code changes; AI versus human architecture corrections; remediation cycles; scope and process violations. Human code corrections or human redesign count as intervention. AI self-remediation does not. Record shared fixes once at campaign level and identify affected cases instead of summing them into independent iterations.

| Metric | Definition and denominator |
|---|---|
| First-pass success rate | Original cases passing initial independent verification without remediation / original cases initially evaluated |
| Final success rate | Original PASS cases / all planned applicable original cases; also display executed coverage and each state count |
| Human correction rate | Cases requiring human code change or redesign / executed original cases; disclose whether human review occurred |
| Average AI remediation cycles | AI correction/reverification cycles / executed original cases; identify shared cycles separately |
| Independent defect rate | Independently reviewed original cases with >=1 independent finding / independently reviewed original cases; show finding counts/severity separately |

Zero denominators mean NOT AVAILABLE, not 0%. Separate original/adapted denominators; no independence is implied by zero findings. Any Assisted Autonomy band is an explicitly conservative qualitative description of tested scope with sample/correlation limitations, not general Backend autonomy. Do not derive it solely from acceptance-criteria completion.

## Framework limits and handoff

The versioned definitions now have a [canonical Laravel executable adapter bundle](../evals/backend/adapters/laravel/REVIEW.md). Its frozen tests and mutations must be adopted by the assigned independent reviewer before candidate implementation. Alternate stacks/project interfaces still require separate bindings. Real reviewer assignment, sandbox permission enforcement and authenticated context provenance remain prerequisites for the next campaign. Framework unit tests exercise gate logic with synthetic files only; they are not BACKEND-EVAL-002 and do not independently verify any Backend implementation. Shared Security/Audit and human integration approval remain required. This update creates no Release Candidate and starts no pilot.

## Using the frozen Laravel adapters

Evaluation Specification → Frozen Reviewer Adapter → Backend Candidate → Independent Verification → Fault Sensitivity → Security Review if required → PASS / FAIL / PARTIAL.

Use evals/backend/adapters/laravel/manifest.json for version/fixture/verification hashes and READY/INCOMPLETE executability status. `runner.py check-freeze` checks the full checksums.json inventory. Follow each case README for setup.sh, verify.sh, every fault and cleanup.sh. Setup copies only approved code into a fresh disposable path; it never overwrites the supplied candidate. Pass the actual implementation using `--candidate`; omitting it selects the calibration application and cannot produce Backend evaluation evidence.

Reviewer must preserve raw logs/JUnit, map assertion IDs to criteria, and fill the campaign evidence-manifest.json with actual contexts and results. The adapter's result JSON is execution evidence, not a substitute for independent Security or campaign scoring. BE-009 requires candidate-owned six-category assertions and checks their failure on mutants as well as reviewer failures. Exact mutation binding mismatch is INCOMPLETE and needs a new preapproved binding, not a skipped-as-passing fault.

The optional BE-006 PostgreSQL probe uses a new private Unix-socket cluster, never an existing service. PostgreSQL validation is NOT EXECUTED where server tooling is absent; SQLite adapter readiness remains separate. Review the handoff's containment limits before running any candidate: this harness is not a hostile-code security sandbox. All calibration/build checks belong to adapter development, not BACKEND-EVAL-001/002/003. Original historical outcomes remain unchanged and Foundation version stays0.6.0.

### Review-output location and remediation status

Store independent Laravel review reports at `validation/adapter-reviews/<REVIEW-ID>/independent-review.md` and `independent-review.json`, outside the frozen executable bundle. Every adapter-owned file remains in the exact inventory; do not exempt arbitrary report filenames or re-freeze reviewer output. Preserve prior review bytes and decisions when relocating reports. The original Laravel review is archived at `validation/adapter-reviews/LARAVEL-2026-09-19-001/` (see its relocation README).

BE-004/007/008 adapter and fixture1.0.1 remediate IR-001/002; external report placement addresses IR-003. READY FOR RE-REVIEW records implementation/calibration readiness only. A separate independent execution context must review the modified oracles, new fault sensitivity and the published freeze before approval. No historical outcome, campaign authorization or Foundation version changes as a result of this remediation.

## Prospective freeze correction — Foundation 0.6.1

The [governed inventory policy](evaluation-freeze.md) supersedes the arbitrary-directory/checksums freeze mechanics above for future campaigns. Pin `evals/backend/governed-inventory.json` before implementation; `runner.py check-freeze` validates the declared assets and returns this inventory's digest. Only documented ephemeral files are excluded; source, fixtures, verification/fault code, manifests, expected results and Foundation evaluation rules remain governed. Generated evidence belongs outside governed roots. Use `PYTHONDONTWRITEBYTECODE=1` or `python3 -B`. Never rebuild an inventory to cure an active campaign mutation. This prospective correction does not change INVALID BACKEND-EVAL-003 or any earlier campaign.
