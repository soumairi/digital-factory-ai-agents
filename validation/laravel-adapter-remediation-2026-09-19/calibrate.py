"""Targeted adapter calibration only; not independent approval or a campaign."""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,shutil
from pathlib import Path
repo=Path(__file__).resolve().parents[2];assets=repo/'evals/backend/adapters/laravel';output=Path(__file__).resolve().parent/'execution';output.mkdir()
spec=importlib.util.spec_from_file_location('runner',assets/'runner.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
results=[]
for case in ['BE-004','BE-007','BE-008']:
 record={'evaluation_id':case,'status':'INCOMPLETE'};root=None
 try:
  root=r.setup(case,'/private/tmp/backend-eval-001-0v7ydh55/app/vendor','/opt/homebrew/opt/php@8.3/bin/php');record['setup']='PASS';clean=r.verify(root,case);record['clean']=clean;assert clean['status']=='PASS',clean
  record['faults']=[]
  for fault in json.loads((assets/case/'fixture.json').read_text())['fault_variants']:
   result=r.fault(root,case,fault['id']);record['faults'].append(result);print(case,fault['id'],result['sensitivity'],flush=True);assert result['sensitivity']=='PASS',result
  record['clean_rerun']=r.verify(root,case);assert record['clean_rerun']['status']=='PASS'
  shutil.copytree(root/'evidence',output/case/'first');record['cleanup']=r.cleanup(root,case);assert not root.exists();root=None
  root=r.setup(case,'/private/tmp/backend-eval-001-0v7ydh55/app/vendor','/opt/homebrew/opt/php@8.3/bin/php');repeat=r.verify(root,case);record['repeat']=repeat;shutil.copytree(root/'evidence',output/case/'repeat')
  assert repeat['status']=='PASS' and repeat['assertions']==clean['assertions'] and repeat['candidate_hash']==clean['candidate_hash']
  record['repeatability']='PASS';record['repeat_cleanup']=r.cleanup(root,case);assert not root.exists();root=None;record['status']='READY FOR RE-REVIEW'
 except Exception as exc:
  record['error']=str(exc);print(case,'ERROR',str(exc),flush=True)
 finally:
  if root is not None and root.exists():
   shutil.copytree(root/'evidence',output/case/'failure',dirs_exist_ok=True);r.cleanup(root,case)
  results.append(record);(output/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(case,record['status'],flush=True)
if any(x['status']!='READY FOR RE-REVIEW' for x in results):sys.exit(1)
