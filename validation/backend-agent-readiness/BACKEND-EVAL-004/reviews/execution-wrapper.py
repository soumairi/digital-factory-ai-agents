import importlib.util,json,sys,shutil,subprocess,datetime
from pathlib import Path
ROOT=Path('/Users/mouhssinesoumairi/digital-factory-ai-agents')
OWN=Path(__file__).parent
OUT=ROOT/'validation/backend-agent-readiness/BACKEND-EVAL-004/reviews'
PIN='41948468644c73d9791729354b3abb2e63bc04fc8d25812d96ac22ea0296af92'
spec=importlib.util.spec_from_file_location('review_runner',OWN/'evals/backend/adapters/laravel/runner.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
def boundary():
 assert r.check_assets()==PIN
 subprocess.run(['python3','-B',str(ROOT/'evals/backend/freeze.py'),'check','--expected-sha256',PIN],check=True,capture_output=True)
def compact(path,data): path.write_text(json.dumps(data,sort_keys=True,separators=(',',':')))
case=sys.argv[1];candidate=Path(sys.argv[2]);out=OUT/case;out.mkdir(exist_ok=True)
boundary();before=r.inventory(candidate,source=True);compact(out/'candidate-source-manifest.json',before)
original=r.execute
def capture(root,state,label,fault=None):
 if fault:
  compact(out/(fault+'-source-manifest.json'),r.inventory(root/'app',source=True))
  targets=json.loads((r.ASSETS/case/'faults'/(fault+'.json')).read_text())['changes']
  for change in targets:
   p=out/'mutants'/fault/change['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/'app'/change['path'],p)
 return original(root,state,label,fault)
r.execute=capture
root=r.setup(case,'/private/tmp/backend-eval-001-0v7ydh55/app/vendor','/opt/homebrew/opt/php@8.3/bin/php',str(candidate))
state=json.loads((root/r.MARKER).read_text());(out/'workspace-state.json').write_text(json.dumps(state,indent=2)+'\n')
compact(out/'assertions-manifest.json',r.inventory(root/'app/reviewer'))
result={'evaluation_id':case,'candidate_source':str(candidate),'candidate_hash':r.tree_hash(before),'context_id':'/root/evaluator','started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'clean':None,'faults':[]}
try:
 result['clean']=r.verify(str(root),case)
 shutil.copyfile(root/'evidence/clean-result.json',out/'initial-clean-result.json')
 if result['clean']['status']=='PASS':
  for f in json.loads((r.ASSETS/case/'fixture.json').read_text())['fault_variants']:
   boundary();result['faults'].append(r.fault(str(root),case,f['id']));print(case,f['id'],result['faults'][-1]['sensitivity'],flush=True)
  result['clean_rerun']=r.verify(str(root),case)
 boundary();assert r.inventory(candidate,source=True)==before
 result['candidate_unchanged']=True
finally:
 shutil.copytree(root/'evidence',out/'execution',dirs_exist_ok=True)
 result['completed_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 (out/'execution-result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'case':case,'clean':result['clean']['status'] if result['clean'] else None,'faults':len(result['faults'])}),flush=True)
 # Retain clean workspace until review finalized; evidence is copied above.
if result['clean'] and result['clean']['status']=='PASS':
 repeat=r.setup(case,'/private/tmp/backend-eval-001-0v7ydh55/app/vendor','/opt/homebrew/opt/php@8.3/bin/php',str(candidate))
 result['repeat']=r.verify(str(repeat),case)
 shutil.copytree(repeat/'evidence',out/'repeat',dirs_exist_ok=True)
 result['repeat_cleanup']=r.cleanup(str(repeat),case)
result['cleanup']=r.cleanup(str(root),case)
boundary();assert r.inventory(candidate,source=True)==before
(out/'execution-result.json').write_text(json.dumps(result,indent=2)+'\n')
