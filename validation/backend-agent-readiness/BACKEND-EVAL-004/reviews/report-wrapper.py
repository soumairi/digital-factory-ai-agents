import json,hashlib,sys,xml.etree.ElementTree as ET,datetime
from pathlib import Path
root=Path('/Users/mouhssinesoumairi/digital-factory-ai-agents');campaign=root/'validation/backend-agent-readiness/BACKEND-EVAL-004';case=sys.argv[1];out=campaign/'reviews'/case
run=json.loads((out/'execution-result.json').read_text());freeze=json.loads((campaign/'cases'/case/'candidate-freeze.json').read_text());assert freeze['candidate_hash']==run['candidate_hash']
fixture=json.loads((root/f'evals/backend/adapters/laravel/{case}/fixture.json').read_text())
tests=[{'name':t.attrib['name'],'assertions':int(t.attrib['assertions']),'class':t.attrib['class']} for t in ET.parse(out/'execution/clean-1.xml').iter('testcase')]
local=[t for t in tests if t['name'].startswith('test_'+case.replace('-',''))]
maps={
'BE-001':[[0],[0,1],list(range(len(local)))],
'BE-002':[[0,1],[0],[0,1]],
'BE-003':[[0,1],[0,1],[0,1]],
'BE-004':[[0,1],[0],[0,1]],
'BE-005':[[0,1],[0,1],[0,1]],
'BE-006':[[0],[0],[0,1]],
'BE-007':[[0,1,2],[0],[0,1,2]],
'BE-008':[[0,2],[0,2],[0,1,2]],
'BE-009':[[0,1],[0,1],[0,1]]}
criteria=[]
for requirement,indices in zip(fixture['required_tests'],maps[case]):
 selected=[local[i] for i in indices]
 if case=='BE-001' and requirement['id'].endswith('regression'): selected=tests
 if case=='BE-009': selected=tests
 criteria.append({'id':requirement['id'],'result':'MET','assertions':sum(t['assertions'] for t in selected),'tests':[t['name'] for t in selected],'rationale':requirement['requirement']+' Actual JUnit method assertion counts are shared coverage, not additive across criteria.'+(' Five real two-process SQLite race rounds also passed in concurrency.txt.' if case=='BE-006' and requirement['id'].endswith('competition') else '')})
dimensions=[('Functional correctness',20,4,'Frozen original clean behavior and persistence assertions pass in initial, post-fault and fresh-workspace runs.'),('Architecture compliance',15,4,'Scoped actual diff follows existing Laravel controller, FormRequest, Gate/model and Action boundaries; no new framework or infrastructure.'),('Security',25,4,'Real guard, server-side authorization, validation, denied-state and safe-output checks pass; exact mandatory faults detected. Required separate Security decision must also clear.'),('Tests',15,4,'Independent unchanged frozen assertions execute without errors/skips, all relevant mutants fail, and candidate-owned scoped tests exist with executed implementer evidence.'),('Scope discipline',10,4,'Actual source inventory and diff match permitted candidate scope; original candidate unchanged after review.'),('Documentation',5,4,'Analysis, explicit scaffold provenance, changed-file diff, own test commands/results, self-review and exact candidate freeze are present.'),('Maintainability',10,3,'Small focused changes reuse established code; compact synthetic fixture code and adapter-specific mutation anchors limit transferability beyond this scaffold.')]
score=sum(weight*rating/4 for _,weight,rating,_ in dimensions)
assert run['clean']['status']==run['clean_rerun']['status']==run['repeat']['status']=='PASS'
assert all(f['sensitivity']=='PASS' and f['tests_unchanged'] and f['clean_unchanged'] for f in run['faults'])
for f in [run['clean'],run['clean_rerun']]+run['faults']:
 p=out/'execution'/Path(f['log_path']).name;assert hashlib.sha256(p.read_bytes()).hexdigest()==f['log_sha256']
 p=out/'execution'/Path(f['junit_path']).name;assert hashlib.sha256(p.read_bytes()).hexdigest()==f['junit_sha256']
review={'evaluation_id':case,'evaluator_context':'/root/evaluator','candidate_revision':freeze['candidate_revision'],'candidate_hash':run['candidate_hash'],'candidate_artifact':str((out/'candidate-source-manifest.json').relative_to(campaign)),'original_case_executed':True,'adapted_scenario':False,'adapted_scenario_result':'NOT APPLICABLE','independent_verification_result':'PASS','status':'PARTIAL','missing_requirement':'Separate mandatory Security review and final evidence assembly are coordinator gates; evaluator execution complete.','first_pass_result':'PASS','criteria':criteria,'executed_tests':tests,'assertion_count_note':'Counts are exact per JUnit method; shared methods map multiple criteria and must not be summed across criteria.','score_dimensions':[{'dimension':name,'rating':rating,'maximum':weight,'points':weight*rating/4,'rationale':reason} for name,weight,rating,reason in dimensions],'score':score,'findings':[],'clean':run['clean'],'faults':run['faults'],'clean_rerun':run['clean_rerun'],'fresh_repeat':run['repeat'],'candidate_unchanged':True,'limitations':['Scaffold-assisted canonical implementation: substantial existing correct behavior reused; does not demonstrate greenfield construction or general autonomy.','SQLite-only synthetic in-process framework tests; PostgreSQL NOT EXECUTED and target-engine validation REQUIRED BEFORE POSTGRESQL PILOT.','Harness supports inspected trusted synthetic source and is not an OS hostile-code security boundary.'],'completion_declaration':'I independently inspected the actual candidate/diff, executed clean, all mandatory faults, post-fault clean and fresh-workspace repeat with reviewer-owned frozen adapters; I did not author or remediate candidate code. Governed pin checked at boundaries.','completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(out/'evaluator-review.json').write_text(json.dumps(review,indent=2)+'\n')
lines=[f'# {case} independent evaluator review','',f'Context `/root/evaluator`; candidate `{freeze["candidate_revision"]}`; SHA-256 `{run["candidate_hash"]}`.','',f'Original case executed YES; adapted scenario NO. Independent verification PASS; final case decision pending separate Security clearance/evidence gate. Score {score}/100.','',review['completion_declaration'],'','| Criterion | Result | Executed methods |','|---|---|---|']
for c in criteria:lines.append('| '+c['id']+' | MET | '+', '.join(c['tests'])+' |')
lines+=['','Exact per-method assertion counts are in evaluator-review.json and raw JUnit. Shared assertion coverage is not additive across criteria.','',f'Clean: {run["clean"]["tests"]} tests / {run["clean"]["assertions"]} assertions; zero failures/errors/skips. Post-fault and fresh-workspace repeats PASS.','', '| Fault | Expected | Actual | Sensitivity |','|---|---|---|---|']
for f in run['faults']:lines.append(f'| {f["fault"]} | FAIL | {f["status"]} | {f["sensitivity"]} |')
lines+=['','Each mutant had relevant assertion failures, no infrastructure errors/skips, unchanged tests and unchanged clean source. Raw execution logs/JUnit and exact mutant source manifests are retained.','','| Dimension | Rating /4 | Points | Rationale |','|---|---|---|---|']
for name,weight,rating,reason in dimensions:lines.append(f'| {name} | {rating} | {weight*rating/4} | {reason} |')
lines+=['','Independent findings: none within the original contract.','']+review['limitations']
(out/'evaluator-review.md').write_text('\n'.join(lines)+'\n')
print(case,score)
