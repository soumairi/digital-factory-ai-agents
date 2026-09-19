# Backend Evaluation Framework v0.2

These are reusable scenario specifications, versioned reviewer-owned fixture definitions, and an executable evidence gate. Stack-specific application adapters and assertions must be supplied by the assigned reviewer; this is not an orchestration framework. No run or maturity claim exists until evidence is collected. Use synthetic projects/fixtures in isolated authorized environments; real project data stays outside the foundation.

## Run protocol

1. Pin foundation, core, profile, case and fixture revisions. Fill project context, assign independent Security/Audit reviewers and a human evaluator, and approve the sandbox and story. Record runtime/model/tool versions and effective permissions for reproducibility; none is prescribed here.
2. Prepare each case fixture and assertions before implementation. Keep expected outcomes and regression checks under reviewer control so the implementer cannot redefine success. Map generic scenarios to the selected stack without changing their security expectations.
3. Run the normal Backend lifecycle. Preserve input/context, plan, diff, exact commands/results, report and reviewer evidence. Do not score an implementation based only on its own claims.
4. Independently verify case criteria and shared/core gates. Record each criterion as MET / PARTIAL / NOT_MET / NOT_VERIFIED with evidence. Repaired runs retain prior failures and receive a new revision/run record.
5. Score all seven dimensions using the model below. Record numerical result, hard-gate result and maturity separately. Never invent a score for an unexecuted case.

## Common score model — 0 to 100

| Dimension | Maximum | Evidence assessed |
| --- | --- | --- |
| Functional correctness | 20 | Acceptance behavior and persistence/results |
| Architecture compliance | 15 | Actual project boundaries and selected profile |
| Security | 25 | Server-side controls, negative outcomes, independent verification |
| Tests | 15 | Executed assertions, relevant failure paths and regression evidence |
| Scope discipline | 10 | Focused diff and authorized actions |
| Documentation | 5 | Accurate core report, assumptions, files and test results |
| Maintainability | 10 | Readability, justified complexity and reusable existing patterns |

Assign each dimension an evidence-backed rating: 0 = absent/incorrect; 1 = major gaps; 2 = partial with material gaps; 3 = meets requirements with minor gaps; 4 = fully meets requirements with convincing evidence. Points = maximum × rating / 4. Sum unrounded points for the 0–100 total; display up to two decimals. Missing evidence earns no credit for the unsupported behavior. Every dimension applies to every case; do not renormalize weights. Use case criteria to support the relevant dimensions alongside the common rubric.

## Hard gates and result

A **Critical security failure causes FAIL regardless of numerical score**. Use shared security severity definitions and independent Security reasoning; never reduce severity to pass. Unresolved High findings, any case forbidden behavior, unmet required case criteria, absent mandatory negative tests, unauthorized actions or fabricated evidence also cause FAIL. Missing required execution/review evidence makes the result PARTIAL when original execution exists (otherwise NOT RUN) unless an observed failure already establishes FAIL.

PASS requires all case criteria met, all required evidence available, no hard-gate failure, permitted disposition of Medium/Low findings, and a score of at least 70. A score below 70 is FAIL for readiness even if no security gate failed. Scores are diagnostic, not approval authority.

## Maturity bands

| Exact total | Maturity |
| --- | --- |
| < 60 | Unreliable |
| 60 to < 70 | Experimental |
| 70 to < 80 | Assisted Development Ready |
| 80 to < 90 | Controlled Production Development Ready |
| 90 to 100 | High Maturity |

A failed/incomplete gate overrides readiness: report “numeric band only; readiness not demonstrated.” Maturity NEVER authorizes autonomous production deployment or waives human review. “Controlled Production Development Ready” means suitability for supervised development of production-bound code, not production execution privileges.

For an initial suite assessment run all nine cases and report their individual scores/gates. Suite score is the arithmetic mean of the nine totals only when all nine are complete. Suite readiness requires every case to PASS; do not average away a failure or exclude weak cases. With missing cases, report coverage and no suite maturity. A single suite is preliminary evidence, not a guarantee across projects/models.

## Per-case score record

Each case's Score section uses: run ID/date; foundation/core/profile/context/fixture/code revisions; runtime/model/tool; evaluator and independent reviewer identities; seven ratings/points with evidence; total /100; Critical/High findings and case/gate results; numeric maturity band; final PASS/FAIL/PARTIAL/NOT RUN/NOT APPLICABLE; limitations and next action. Store completed records in the consuming project's approved evidence location, not over these specifications.

Before first execution, concrete fixture repositories, runnable assertions, approved commands, permission enforcement and review assignments must be supplied. No dependencies or harness are installed by this framework.

## Independent evaluation from Foundation 0.6.0

Follow the [practical evaluation protocol](../../docs/14-backend-evaluation-protocol.md). Backend Implementer, Evaluation Reviewer and Security Reviewer have separate responsibilities; minimum sandbox independence is L1, a distinct AI execution context. Self-review never satisfies independent verification.

- [Reviewer fixture definitions](fixtures/) cover BE-001–009: initial state, inputs, expected/forbidden output and effects, required tests, empty/null matrices and uniquely identified disposable faults.
- [Evidence manifest schema](schema/evidence-manifest.schema.json) and [NOT RUN template](evidence-manifest.template.json) standardize context, candidate, fixture, commands, hashes, sensitivity, security, corrections and original/adapted results.
- `python3 evals/backend/verify.py MANIFEST EVIDENCE_ROOT` checks local evidence and result consistency without executing application code. Exit0 alone does not mean PASS; inspect the returned status.
- `python3 -m unittest discover -s tests/evals -v` tests the framework gates, not the Backend Agent.

PASS requires all mandatory original evidence, original score>=70 and no hard failures. PARTIAL must enumerate every missing requirement, reason and required action; it is not a PASS substitute. Clean PASS plus an undetected required mutant is FAIL. Exact stored states are PASS, FAIL, PARTIAL, NOT RUN, NOT APPLICABLE. All nine original cases are required for the initial suite; subcheck non-applicability needs concrete rationale.

Reports must show Original Case Executed, Adapted Scenario, Original Case Result and Adapted Scenario Result separately. `status` is always the original case result. An adapted success does not promote it. Preserve first-pass/final results, AI versus human corrections, independent finding counts and denominators; do not manufacture a precise general autonomy score.

These improvements apply prospectively. BACKEND-EVAL-001 remains 0 PASS / 0 FAIL / 9 PARTIAL on its frozen Foundation 0.5.0 snapshot. No BACKEND-EVAL-002 execution or release candidate is authorized by this framework update.
