import sys
sys.dont_write_bytecode=True
import importlib.util,json,shutil,tempfile
from pathlib import Path
repo=Path('/Users/mouhssinesoumairi/digital-factory-ai-agents');a=repo/'evals/backend/adapters/laravel';out=repo/'validation/laravel-independent-review-2026-09-19/owner-update-probe-2';out.mkdir()
spec=importlib.util.spec_from_file_location('runner',a/'runner.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
results=[]
for case,old,new in [
 ('BE-004',"if($r->isMethod('PATCH')) $q->update(EvalInput::fields($r,['title'=>'required|string|max:100']));", "if($r->isMethod('PATCH')) EvalInput::fields($r,['title'=>'required|string|max:100']);")]:
 root=r.setup(case,'/private/tmp/backend-eval-001-0v7ydh55/app/vendor','/opt/homebrew/opt/php@8.3/bin/php');variant=None
 try:
  clean=r.verify(root,case);assert clean['status']=='PASS'
  variant=Path(tempfile.mkdtemp(prefix='laravel-adapter-',dir='/private/tmp'));shutil.copytree(root/'app',variant/'app');(variant/'evidence').mkdir()
  state=json.loads((root/r.MARKER).read_text());state['root']=str(variant);(variant/r.MARKER).write_text(json.dumps(state))
  p=variant/'app/app/Http/Controllers/EvalController.php';text=p.read_text();assert text.count(old)==2;head,tail=text.split('public function document(Request $r,int $id)',1);assert tail.count(old)==1;p.write_text(head+'public function document(Request $r,int $id)'+tail.replace(old,new))
  res=r.execute(variant,state,'owner-update-noop','INDEPENDENT-owner-update-noop');res['patch']={'path':'app/Http/Controllers/EvalController.php','old':old,'new':new};res['tests_unchanged']=r.inventory(variant/'app/reviewer')==r.inventory(root/'app/reviewer');res['clean_restored']=r.verify(root,case)['status'];res['evaluation_id']=case
  dest=out/case;shutil.copytree(variant/'evidence',dest);(dest/'result.json').write_text(json.dumps(res,indent=2));results.append(res);print(case,'owner update no-op variant',res['status'],flush=True)
 finally:
  if variant:r.cleanup(variant,case)
  r.cleanup(root,case)
(out/'results.json').write_text(json.dumps(results,indent=2))
# Test report-placement behavior on a disposable bundle, leaving repository freeze untouched.
with tempfile.TemporaryDirectory(prefix='independent-freeze-',dir='/private/tmp') as name:
 clone=Path(name)/'bundle';shutil.copytree(a,clone);r.ASSETS=clone
 assert r.check_assets()
 (clone/'independent-review.md').write_text('Separate reviewer report\n')
 try:r.check_assets();result={'unexpected_pass':True}
 except ValueError as e:result={'status':'CONFIRMED','error':str(e)}
 (out/'report-placement.json').write_text(json.dumps(result,indent=2));print(result,flush=True)
