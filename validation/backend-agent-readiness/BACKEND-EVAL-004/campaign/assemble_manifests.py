"""Assemble evidence references; never execute candidate code or alter governed inputs."""
from pathlib import Path
import json,hashlib,importlib.util
C=Path(__file__).resolve().parents[1]
R=C.parents[2]
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def ref(p):return {'path':str(p.relative_to(C)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
spec=importlib.util.spec_from_file_location('gate',R/'evals/backend/verify.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
adapters={x['evaluation_id']:x for x in read(C/'campaign/adapter-manifest.json')['adapters']}
for n in range(1,10):
 eid=f'BE-{n:03}';case=C/'cases'/eid;review=C/'reviews'/eid
 required=[case/'candidate-freeze.json',review/'evaluator-review.json',C/'reviews'/f'security-{eid}.json']
 if not all(p.exists() for p in required):continue
 f,ev,sec=map(read,required);ex=read(review/'execution-result.json');fixture=read(R/'evals/backend/fixtures'/f'{eid}.json')
 m=read(R/'evals/backend/evidence-manifest.template.json')
 m.update(campaign_id='BACKEND-EVAL-004',evaluation_id=eid,foundation_version='0.6.1',foundation_snapshot=ref(C/'campaign/governed-inventory.json'),candidate_revision=f['candidate_revision'],candidate_hash=f['candidate_hash'],candidate_artifact=ref(case/'candidate-source-manifest.json'),fixture_version=fixture['fixture_version'],fixture_hash=hashlib.sha256((R/'evals/backend/fixtures'/f'{eid}.json').read_bytes()).hexdigest())
 m['implementer_context']={'id':'/root/implementer','role':'Backend Implementer','execution_record':ref(C/'campaign/implementer-context.md')}
 m['reviewer_context']={'id':'/root/evaluator','role':'Evaluation Reviewer','execution_record':ref(C/'reviews/evaluator-start.md')}
 m['security_context']={'id':'/root/security','role':'Security Reviewer','execution_record':ref(C/'reviews/security-context.md')}
 a=ref(review/'assertions-manifest.json')
 m['fixture_freeze']={'owner_context':'/root/evaluator','before_implementation':True,'assertions_hash':a['sha256'],'record':ref(C/'reviews/evaluator-adoption.json'),'assertions_artifact':a}
 m['tests_executed']=[];m['criteria']=[]
 for criterion in ev['criteria']:
  m['tests_executed'].append({'id':criterion['id'],'result':{'MET':'PASS','NOT_MET':'FAIL','NOT_VERIFIED':'PARTIAL'}.get(criterion['result'],criterion['result']),'assertions':criterion['assertions'],'errors':ex['clean']['errors'],'skipped':ex['clean']['skipped'],'command':ex['clean']['command'],'context_id':'/root/evaluator','candidate_hash':f['candidate_hash'],'tests_hash':a['sha256'],'evidence':ref(review/'evaluator-review.json')})
  m['criteria'].append({'id':criterion['id'],'result':{'MET':'PASS','NOT_MET':'FAIL','NOT_VERIFIED':'PARTIAL'}.get(criterion['result'],criterion['result']),'evidence':ref(review/'evaluator-review.json')})
 m['fault_variants']=[]
 for fault in ex['faults']:
  fid=fault['fault'];target=next(x['target_test'] for x in fixture['fault_variants'] if x['id']==fid)
  artifact=ref(review/f'{fid}-source-manifest.json')
  assert artifact['sha256']==fault['mutant_source_hash']
  m['fault_variants'].append({'id':fid,'expected_detection':'FAIL','actual_detection':fault['status'],'result':fault['sensitivity'],'assertion_failures':fault['failures'],'errors':fault['errors'],'context_id':'/root/evaluator','candidate_hash':f['candidate_hash'],'mutant_hash':artifact['sha256'],'tests_hash':a['sha256'],'disposable_copy':True,'clean_unchanged':fault['clean_unchanged'],'evidence':ref(review/'execution'/f'{fid}-result.json'),'mutant_artifact':artifact,'detected_test_ids':[target] if fault['sensitivity']=='PASS' else []})
 m.update(test_result=ex['clean']['status'],clean_rerun=ex['clean_rerun']['status'],clean_rerun_evidence=ref(review/'execution/clean-result.json'),security_review_required=True,security_review_result=sec['status'],security_evidence=ref(C/'reviews'/f'security-{eid}.json'),security_candidate_hash=sec['candidate_hash'],human_correction=f['human_correction'],remediation_cycles=f['ai_remediation_cycles'],original_case_executed=True,adapted_scenario=False,adapted_scenario_result='NOT APPLICABLE',score=ev['score'])
 m['metrics']={'initial_implementation_outcome':f['first_pass_result'],'ai_self_corrections':f['ai_remediation_cycles'],'independent_reviewer_findings':len(ev['findings']),'security_findings':len(sec['findings']),'human_code_corrections':int(f['human_correction']),'architecture_corrections':{'ai':int(f['architecture_correction']),'human':0},'scope_violations':int(f['scope_violation']),'process_violations':0}
 m['score_dimensions']=[{'dimension':d['dimension'],'rating':d['rating'],'evidence':ref(review/'evaluator-review.json')} for d in ev['score_dimensions']]
 m['hard_failures']=ev.get('hard_failures',[])+sec.get('hard_failures',[])
 m['status']=m['original_case_result']=ev['independent_verification_result'] if sec['status']=='PASS' else 'FAIL'
 checked=gate.verify(m,C)
 write(case/'framework-manifest.json',m);write(case/'framework-verification.json',checked)
 extended=dict(m,adapter_version=adapters[eid]['adapter_version'],evaluator_context=m['reviewer_context'],security_context_if_required=m['security_context'],clean_verification=ex['clean']['status'],first_pass_result=f['first_pass_result'],ai_remediation_cycles=f['ai_remediation_cycles'],architecture_correction=f['architecture_correction'],scope_violation=f['scope_violation'],changed_files=f['changed_files'],implementation_diff=ref(case/'implementation.diff'),framework_manifest=ref(case/'framework-manifest.json'),framework_validation=checked,initial_independent_verification=ex['clean']['status'])
 write(case/'evidence-manifest.json',extended)
 print(eid,checked['status'])
