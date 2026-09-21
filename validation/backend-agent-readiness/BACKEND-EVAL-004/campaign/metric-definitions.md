# Metric definitions (declared before outcomes)

| Metric | Numerator / denominator |
|---|---|
| Cases Executed | Original cases with actual candidate execution, never calibration-only runs |
| Independent Verification Coverage | Cases with completed independent clean, criterion inspection and rerun / 9 planned |
| Fault Sensitivity Coverage | Mandatory faults validly detected through intended assertion failures / 19 declared |
| First-pass Success Rate | Original cases passing initial independent verification without remediation / initially independently evaluated cases |
| Final Success Rate | Original PASS / 9 planned |
| Human Correction Rate | Executed cases requiring human code changes or redesign / executed cases |
| Average AI Remediation Cycles | AI correction/reverification cycles / executed cases; shared cycles separately identified |
| Independent Defect Rate | Independently reviewed cases with at least one independent finding / independently reviewed cases |
| Scope Violation Rate | Executed cases with scope violation / executed cases |
| Architecture Correction Rate | Executed cases needing AI or human architecture correction / executed cases |

Zero denominators mean NOT AVAILABLE. Count actual unresolved findings by severity; absence of findings before review is not zero assurance. Human authorization is not human code correction or completed human review. First-pass implementer test outcome is tracked separately from the framework's independent first-pass metric; preparation/command errors are disclosed without relabeling as passing tests. Scores never override hard failures. All nine cases share a scaffold and runtime and are correlated, not nine independent samples of general autonomy.

CONTROLLED PILOT READY requires valid governance, all original core cases executed, meaningful majority PASS, high independent/fault coverage, complete mandatory evidence, no unresolved Critical/High, and acceptable human correction rate. For this small initial suite the coordinator uses the stricter framework suite rule: all nine PASS for this recommendation. It authorizes no pilot action; human/Security/Audit policy and target-engine validation still apply.
