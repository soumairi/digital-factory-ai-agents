"""Record independently inspected security conclusions, checking source/log provenance."""
from pathlib import Path
import json,hashlib,datetime,sys,xml.etree.ElementTree as ET
base=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
case=sys.argv[1]; assessment=sys.argv[2]
c=base/'cases'/case; r=base/'reviews'/case
freeze=json.loads((c/'candidate-freeze.json').read_text()); ev=json.loads((r/'execution-result.json').read_text())
manifest={}
for p in sorted((c/'candidate').rglob('*')):
    assert not p.is_symlink()
    rel=p.relative_to(c/'candidate')
    if not p.is_file() or rel.parts[0] in {'vendor','storage','reviewer'} or rel.parts[:2]==('bootstrap','cache') or p.name.startswith('.phpunit'): continue
    manifest[str(rel)]=sha(p)
h=hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert h==freeze['candidate_hash']==ev['candidate_hash']
assert manifest==json.loads((c/'candidate-source-manifest.json').read_text())
checked=[]; names=[]
for key in ['clean','clean_rerun','repeat']:
    run=ev[key]; assert run['status']=='PASS' and run['candidate_hash']==h and run['errors']==run['skipped']==run['failures']==0
    folder=r/('repeat' if key=='repeat' else 'execution')
    for field,hashfield in [('log_path','log_sha256'),('junit_path','junit_sha256')]:
        p=folder/Path(run[field]).name; assert sha(p)==run[hashfield]; checked.append(str(p.relative_to(base)))
    if key=='clean': names=[x.attrib['name'] for x in ET.parse(folder/Path(run['junit_path']).name).iter('testcase')]
for fault in ev['faults']:
    assert fault['sensitivity']=='PASS' and fault['status']=='FAIL' and fault['errors']==fault['skipped']==0 and fault['failures']>0 and fault['clean_candidate_hash']==h
    for field,hf in [('log_path','log_sha256'),('junit_path','junit_sha256')]:
        p=r/'execution'/Path(fault[field]).name; assert sha(p)==fault[hf]; checked.append(str(p.relative_to(base)))
inspected=['app/Http/Controllers/EvalController.php','app/Http/Requests/EvalInput.php','app/Http/Middleware/EvalAuthenticate.php','routes/api.php','app/Providers/AppServiceProvider.php']+freeze['changed_files']
inspected += {'BE-005':['app/Models/EvalProfile.php'],'BE-006':['app/Actions/EvalReserve.php'],'BE-008':['app/Models/EvalArticle.php'],'BE-009':['app/Models/EvalProfile.php']}.get(case,[])
inspected=list(dict.fromkeys(inspected))
result={'campaign_id':'BACKEND-EVAL-004','evaluation_id':case,'reviewer_context':'/root/security','role':'Security Reviewer','candidate_revision':freeze['candidate_revision'],'candidate_hash':h,'source_hash_verified':True,'security_review_required':True,'status':'PASS','security_review_result':'PASS','assessment':assessment,'inspected_paths':inspected,'executed_test_names':names,'independent_evaluator_context':ev['context_id'],'evidence_paths':checked,'clean_tests':ev['clean']['tests'],'clean_assertions':ev['clean']['assertions'],'faults':[{'id':f['fault'],'status':f['status'],'sensitivity':f['sensitivity'],'failed_tests':f['failed_tests']} for f in ev['faults']],'findings':[],'unresolved_severities':{'Critical':0,'High':0,'Medium':0,'Low':0},'limitations':['Approved synthetic local SQLite case only; not hostile-code containment or production assurance.','Canonical scaffold and fault bindings reused; no claim of unconstrained greenfield capability.','No external dependency vulnerability service or broad penetration test performed.','PostgreSQL NOT EXECUTED; target-engine validation REQUIRED BEFORE POSTGRESQL PILOT.','Human integration approval and Audit remain separate policy gates; this review does not provide either.'],'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_declaration':'Read-only actual source/diff and independent executed evidence inspected; source and evidence hashes independently checked. No code modification or remediation authorship.'}
p=base/'reviews'/('security-'+case)
p.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
p.with_suffix('.md').write_text(f"# {case} independent Security review\n\nReviewer: `/root/security`. Result: **PASS** for the declared synthetic SQLite case.\nCandidate: `{freeze['candidate_revision']}`; SHA-256 `{h}` independently recomputed from actual source.\n\n{assessment}\n\nInspected actual candidate paths: "+', '.join('`'+x+'`' for x in inspected)+f". Implementation diff and frozen original adapter assertions inspected.\n\nIndependent `/root/evaluator` evidence: {ev['clean']['tests']} clean tests, {ev['clean']['assertions']} assertions; zero errors/skips/failures. Post-fault clean and fresh-workspace repeat PASS. "+str(len(ev['faults']))+" declared mutants fail relevant assertions with no infrastructure errors/skips. All cited log/JUnit bytes hash-checked; details and paths in companion JSON.\n\nUnresolved findings: Critical 0; High 0; Medium 0; Low 0. No risk accepted by reviewer.\n\nLimitations: "+' '.join(result['limitations'])+'\n\nCompletion: '+result['completion_declaration']+' UTC '+result['completed_at']+'\n')
print(case,h,'Security PASS')
