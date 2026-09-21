"""Read-only campaign integrity audit with externally pinned governed inventory."""
from pathlib import Path
import json,hashlib,importlib.util,datetime,subprocess
C=Path(__file__).resolve().parents[1];R=C.parents[2]
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
f=load('freeze',R/'evals/backend/freeze.py');runner=load('runner',R/'evals/backend/adapters/laravel/runner.py')
pin=read(C/'campaign/freeze.json')['inventory_sha256'];assert f.validate(R,pin)==pin
history=read(C/'campaign/historical-sha256.json');hist_errors=[n for n,h in history.items() if not (R/n).is_file() or digest(R/n)!=h]
assert not hist_errors,hist_errors
checks=[]
for n in range(1,10):
 e=f'BE-{n:03}';case=C/'cases'/e;freeze=read(case/'candidate-freeze.json');src=runner.inventory(case/'candidate',source=True);manifest=read(case/'candidate-source-manifest.json')
 assert src==manifest and runner.tree_hash(src)==freeze['candidate_hash']==digest(case/'candidate-source-manifest.json')
 ex=read(C/'reviews'/e/'execution-result.json');assert ex['candidate_hash']==freeze['candidate_hash'] and ex['candidate_unchanged']
 for label,obj,base in [('clean',ex['clean'],C/'reviews'/e/'execution'),('rerun',ex['clean_rerun'],C/'reviews'/e/'execution'),('repeat',ex['repeat'],C/'reviews'/e/'repeat')]+[(x['fault'],x,C/'reviews'/e/'execution') for x in ex['faults']]:
  assert digest(base/Path(obj['log_path']).name)==obj['log_sha256']
  assert digest(base/Path(obj['junit_path']).name)==obj['junit_sha256']
  if obj.get('concurrency'):assert digest(base/'concurrency.txt')==obj['concurrency']['log_sha256']
 checks.append({'evaluation_id':e,'candidate_hash':freeze['candidate_hash'],'candidate_source':'PASS','raw_log_junit_hashes':'PASS','faults':len(ex['faults'])})
status=subprocess.run(['git','status','--short'],cwd=R,capture_output=True,text=True,check=True).stdout
assert all('validation/backend-agent-readiness/BACKEND-EVAL-004/' in line for line in status.splitlines()),status
out={'status':'PASS','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'governed_assets':283,'governed_inventory_sha256':pin,'governed_assets_check':'PASS','historical_files':len(history),'historical_mismatches':hist_errors,'candidate_checks':checks,'working_tree_status':status,'limitations':'Boundary hash checks and coordinator provenance do not prove cryptographic independence or exclude transient restored mutations.'}
(C/'final/integrity-verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','governed_assets':283,'historical_files':len(history),'candidates':len(checks)}))
