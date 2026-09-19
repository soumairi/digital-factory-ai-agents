import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,importlib.util,shutil,time
import argparse
parser=argparse.ArgumentParser(description='Calibrate frozen Laravel adapters; not a Backend evaluation campaign.')
parser.add_argument('--vendor',required=True)
parser.add_argument('--php',default='/opt/homebrew/opt/php@8.3/bin/php')
parser.add_argument('--output',required=True,type=Path)
args=parser.parse_args()
a=Path(__file__).resolve().parent;r=a.parents[3];out=args.output.resolve()
if out.exists():raise SystemExit('Refusing to overwrite prior calibration evidence')
if out.is_relative_to(a) or out.is_relative_to(r/'validation/backend-agent-readiness'):raise SystemExit('Evidence cannot modify frozen assets or historical campaigns')
out.mkdir(parents=True)
spec=importlib.util.spec_from_file_location('runner',a/'runner.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
vendor=args.vendor;php=args.php;results=[]
for id in runner.IDS:
 record={'evaluation_id':id,'started_at':time.time(),'setup':'INCOMPLETE','clean':'INCOMPLETE','faults':[],'cleanup':'INCOMPLETE','repeatable':'INCOMPLETE','status':'INCOMPLETE'}
 root=None;repeat=None
 try:
  root=runner.setup(id,vendor,php);record['setup']='PASS';record['workspace']=str(root)
  clean=runner.verify(root,id);record['clean']=clean['status'];record['clean_evidence']=clean
  if clean['status']=='PASS':
   f=json.loads((a/id/'fixture.json').read_text())
   for fault in f['fault_variants']:
    res=runner.fault(root,id,fault['id']);record['faults'].append(res);print(id,fault['id'],res['sensitivity'],flush=True)
   # Rerun clean after every variant has been isolated and removed.
   restored=runner.verify(root,id);record['clean_restored']=restored['status']
  dest=out/id;dest.mkdir(exist_ok=True);shutil.copytree(root/'evidence',dest/'first',dirs_exist_ok=True)
  state=json.loads((root/runner.MARKER).read_text());record['candidate_hash']=state['candidate_hash'];record['freeze_hash']=state['adapter_freeze']
  record['cleanup']=runner.cleanup(root,id)['cleanup'];record['cleanup_absence_confirmed']=not root.exists();root=None
  repeat=runner.setup(id,vendor,php);res=runner.verify(repeat,id)
  shutil.copytree(repeat/'evidence',dest/'repeat',dirs_exist_ok=True)
  record['repeat_evidence']=res;record['repeatable']='PASS' if res['status']=='PASS' and res['assertions']==clean['assertions'] and res['candidate_hash']==clean['candidate_hash'] else 'FAIL'
  runner.cleanup(repeat,id);repeat=None
  fault_count=len(json.loads((a/id/'fixture.json').read_text())['fault_variants'])
  record['status']='READY' if all(record[k]=='PASS' for k in ['setup','clean','cleanup','repeatable']) and record.get('clean_restored')=='PASS' and len(record['faults'])==fault_count and all(f['sensitivity']=='PASS' for f in record['faults']) else 'INCOMPLETE'
 except Exception as exc:
  record['error']=str(exc);print('ERROR',id,repr(exc),flush=True)
 finally:
  for path in [root,repeat]:
   if path is not None and path.exists():
    dest=out/id;dest.mkdir(exist_ok=True)
    if (path/'evidence').exists():shutil.copytree(path/'evidence',dest/'failure',dirs_exist_ok=True)
    runner.cleanup(path,id)
  results.append(record);(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
  print(id,record['status'],'clean',record['clean'],'repeat',record['repeatable'],flush=True)
print('READY',sum(x['status']=='READY' for x in results),'of',len(results),flush=True)

if any(x["status"]!="READY" for x in results):raise SystemExit(1)
