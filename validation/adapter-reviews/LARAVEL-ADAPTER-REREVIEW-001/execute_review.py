"""Independent targeted re-review; no campaign execution or asset edits."""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,shutil,tempfile
from pathlib import Path
repo=Path(__file__).resolve().parents[3];assets=repo/'evals/backend/adapters/laravel';out=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runner',assets/'runner.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
freeze={'before':r.check_assets()}
with tempfile.TemporaryDirectory(dir='/private/tmp',prefix='rereview-freeze-') as tmp:
 copy=Path(tmp)/'assets';shutil.copytree(assets,copy);r.ASSETS=copy
 freeze['copy_baseline']=r.check_assets()
 owned=copy/'BE-004/tests/BE004Test.php';original=owned.read_bytes()
 for mode in ['modify','remove','add']:
  if mode=='modify':owned.write_bytes(original+b'\n// independent disposable tamper probe\n')
  elif mode=='remove':owned.unlink()
  else:(copy/'independent-review.json').write_text('{}')
  try:r.check_assets();freeze[mode]='FAIL'
  except ValueError as exc:freeze[mode]={'status':'PASS','rejection':str(exc)}
  if mode in ['modify','remove']:owned.write_bytes(original)
  else:(copy/'independent-review.json').unlink()
 r.ASSETS=assets
freeze['after_external_output']=r.check_assets();(out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
results=[]
for case in ['BE-004','BE-007','BE-008']:
 record={'evaluation_id':case};root=None
 try:
  root=r.setup(case,'/private/tmp/backend-eval-001-0v7ydh55/app/vendor','/opt/homebrew/opt/php@8.3/bin/php')
  clean=r.verify(root,case);record['clean']=clean;assert clean['status']=='PASS'
  record['faults']=[]
  for fault in json.loads((assets/case/'fixture.json').read_text())['fault_variants']:
   result=r.fault(root,case,fault['id']);record['faults'].append(result);print(case,fault['id'],result['status'],result['sensitivity'],flush=True);assert result['sensitivity']=='PASS'
  record['clean_rerun']=r.verify(root,case);assert record['clean_rerun']['status']=='PASS'
  shutil.copytree(root/'evidence',out/'execution'/case/'first');r.cleanup(root,case);assert not root.exists();root=None
  root=r.setup(case,'/private/tmp/backend-eval-001-0v7ydh55/app/vendor','/opt/homebrew/opt/php@8.3/bin/php');record['repeat']=r.verify(root,case)
  shutil.copytree(root/'evidence',out/'execution'/case/'repeat')
  assert record['repeat']['status']=='PASS' and record['repeat']['assertions']==clean['assertions'] and record['repeat']['candidate_hash']==clean['candidate_hash']
  r.cleanup(root,case);assert not root.exists();root=None;record['cleanup']='PASS';record['status']='APPROVED'
 except Exception as exc:record['status']='INCOMPLETE';record['error']=repr(exc)
 finally:
  if root is not None and root.exists():
   shutil.copytree(root/'evidence',out/'execution'/case/'failure',dirs_exist_ok=True);r.cleanup(root,case)
  results.append(record);(out/'execution-results.json').write_text(json.dumps(results,indent=2)+'\n');print(case,record['status'],flush=True)
if any(x['status']!='APPROVED' for x in results):sys.exit(1)
