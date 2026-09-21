#!/usr/bin/env python3
"""Reviewer adapter runner. Approved synthetic PHP code only, not a hostile-code jail."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parent
IDS = [f'BE-{i:03}' for i in range(1, 10)]
MARKER = '.laravel-adapter-workspace.json'
RUNTIME_DIRS = {'vendor', 'storage', 'reviewer'}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inventory(root, source=False):
    result = {}
    for p in sorted(Path(root).rglob('*')):
        rel = p.relative_to(root)
        if p.is_symlink():
            raise ValueError('Symlink not allowed: ' + str(rel))
        if not p.is_file():
            continue
        if source and (rel.parts[0] in RUNTIME_DIRS or rel.parts[:2] == ('bootstrap', 'cache') or p.name.startswith('.phpunit')):
            continue
        result[str(rel)] = digest(p)
    return result


def tree_hash(values):
    return hashlib.sha256(json.dumps(values, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def check_assets():
    # The campaign pins this inventory digest; runtime cache is not a governed asset.
    import importlib.util
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('evaluation_freeze', ASSETS.parents[1] / 'freeze.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate(ASSETS.parents[3])


def workspace(value, evaluation=None):
    p = Path(value)
    if p.is_symlink() or p.resolve() != p.absolute():
        raise ValueError('Workspace must be a canonical non-symlink path')
    if p.parent != Path('/private/tmp') or not p.name.startswith('laravel-adapter-'):
        raise ValueError('Not an owned disposable workspace')
    state = json.loads((p / MARKER).read_text())
    if state['root'] != str(p) or state['created_by'] != 'laravel-reviewer-adapter-1.0.0':
        raise ValueError('Invalid workspace marker')
    if evaluation and state['evaluation_id'] != evaluation:
        raise ValueError('Wrong evaluation workspace')
    return p, state


def environment(root):
    # Never inherit database endpoints, proxies, tokens, HOME configuration or ini.
    return {'PATH':'/usr/bin:/bin', 'HOME':str(root), 'TMPDIR':str(root),
            'PYTHONDONTWRITEBYTECODE':'1',
            'APP_ENV':'testing', 'APP_DEBUG':'false', 'APP_URL':'http://localhost',
            'APP_KEY':'base64:'+base64.b64encode(b'0'*32).decode(),
            'DB_CONNECTION':'sqlite', 'DB_DATABASE':':memory:', 'DB_URL':'',
            'CACHE_STORE':'array', 'SESSION_DRIVER':'array', 'MAIL_MAILER':'array',
            'QUEUE_CONNECTION':'sync', 'QUEUE_FAILED_DRIVER':'null', 'BROADCAST_CONNECTION':'null',
            'FILESYSTEM_DISK':'local', 'LOG_CHANNEL':'single', 'LOG_LEVEL':'warning',
            'BCRYPT_ROUNDS':'4', 'PULSE_ENABLED':'false', 'TELESCOPE_ENABLED':'false',
            'NIGHTWATCH_ENABLED':'false'}


def setup(evaluation, vendor, php, candidate=None):
    freeze = check_assets()
    source = Path(candidate).resolve() if candidate else ASSETS/'calibration/application'
    vendor = Path(vendor).resolve()
    # Copies only; no application code is executed during setup.
    src = inventory(source, source=True)
    vendor_manifest = inventory(vendor)
    if any((source/p).exists() for p in ['.env','.env.testing','bootstrap/cache/config.php']):
        raise ValueError('Unreviewed env/cached configuration prohibited')
    lock = digest(source/'composer.lock')
    if lock != digest(ASSETS/'calibration/application/composer.lock'):
        raise ValueError('Unsupported dependency lock; independent binding required')
    # Match actual dependency bytes used in adapter validation, not merely a caller lock label.
    if vendor_manifest != json.loads((ASSETS/'common/vendor-sha256.json').read_text()):
        raise ValueError('Vendor bytes differ from pinned calibration runtime')
    baseline = inventory(ASSETS/'calibration/application',source=True)
    changed = sorted(k for k in set(src)|set(baseline) if src.get(k)!=baseline.get(k))
    permitted = ('app/Actions/','app/Http/','app/Models/','tests/')
    exact = {'routes/api.php','app/Providers/AppServiceProvider.php'}
    if any(k not in exact and not k.startswith(permitted) for k in changed):
        raise ValueError('Candidate exceeds frozen application scope; reviewer rebind required')
    if not (source/'artisan').is_file() or not (vendor/'autoload.php').is_file():
        raise ValueError('Laravel application/vendor missing')
    root = Path(tempfile.mkdtemp(prefix='laravel-adapter-', dir='/private/tmp'))
    try:
        app = root/'app'
        shutil.copytree(source, app, ignore=shutil.ignore_patterns('vendor','storage','.env','.env.testing','.phpunit*','reviewer'))
        for cache in (app/'bootstrap/cache').glob('*.php'):
            cache.unlink()
        shutil.copytree(vendor, app/'vendor')
        for d in ['storage/app/private','storage/framework/cache/data','storage/framework/sessions','storage/framework/views','storage/logs','bootstrap/cache']:
            (app/d).mkdir(parents=True, exist_ok=True)
        shutil.copytree(ASSETS/'common', app/'reviewer/common')
        selected = [evaluation] if evaluation != 'BE-009' else ['BE-001','BE-002','BE-005','BE-009']
        for case in selected:
            shutil.copytree(ASSETS/case/'tests', app/'reviewer'/case/'tests')
        paths = [f'<directory>{case}/tests</directory>' for case in selected]
        if evaluation == 'BE-001':
            paths.append('<directory>../tests</directory>')
        if evaluation == 'BE-009':
            if not (app/'tests/Feature/BackendNegativeTest.php').is_file():
                raise ValueError('BE009 requires candidate-owned BackendNegativeTest.php; reviewer suite cannot substitute')
            paths.append('<file>../tests/Feature/BackendNegativeTest.php</file>')
        (app/'reviewer/phpunit.xml').write_text('<?xml version="1.0"?><phpunit bootstrap="../vendor/autoload.php" colors="false" cacheResult="false"><testsuites><testsuite name="Reviewer-'+evaluation+'">'+''.join(paths)+'</testsuite></testsuites></phpunit>')
        (root/'evidence').mkdir()
        baseline = inventory(app, source=True)
        state = {'created_by':'laravel-reviewer-adapter-1.0.0','root':str(root),
                 'evaluation_id':evaluation,'adapter_freeze':freeze,'php':str(Path(php).resolve()),
                 'candidate_source':str(source),'candidate_hash':tree_hash(baseline),
                 'source_files':baseline,'reviewer_files':inventory(app/'reviewer'),'changed_files':changed,'calibration_only':candidate is None,'created_at':time.time()}
        (root/MARKER).write_text(json.dumps(state,indent=2)+'\n')
        return root
    except Exception:
        shutil.rmtree(root)
        raise


def execute(root, state, label, fault=None):
    app = root/'app'
    env = environment(root)
    junit = root/'evidence'/f'{label}.xml'
    command = [state['php'],'-n','-d','allow_url_fopen=0','-d','ffi.enable=0',
               'vendor/bin/phpunit','-c','reviewer/phpunit.xml','--colors=never','--log-junit',str(junit)]
    start = time.time()
    process = subprocess.run(command,cwd=app,env=env,capture_output=True,text=True,timeout=120)
    log = root/'evidence'/f'{label}.txt';log.write_text(process.stdout+process.stderr)
    result = {'command':command,'cwd':str(app),'exit_code':process.returncode,
              'log_sha256':digest(log),'elapsed_seconds':time.time()-start,
              'candidate_hash':tree_hash(inventory(app,source=True)), 'fault':fault,
              'log_path':str(log.relative_to(root)), 'junit_path':str(junit.relative_to(root)),
              'adapter_freeze':state.get('adapter_freeze'), 'calibration_only':state.get('calibration_only',False),
              'candidate_source':state.get('candidate_source'),
              'tests':0,'assertions':0,'failures':0,'errors':0,'skipped':0,'failed_tests':[],
              'candidate_negative_tests':[],'candidate_negative_failures':[]}
    if not junit.exists():
        result['status']='INCOMPLETE';return result
    xml=ET.parse(junit).getroot();suite=xml.find('testsuite')
    for key in ['tests','assertions','failures','errors','skipped']:
        result[key]=int(suite.attrib.get(key,0))
    for test in xml.iter('testcase'):
        if test.find('failure') is not None:
            result['failed_tests'].append(test.attrib.get('name',''))
        if test.attrib.get('class','').endswith('BackendNegativeTest'):
            result['candidate_negative_tests'].append(test.attrib['name'])
            if test.find('failure') is not None:result['candidate_negative_failures'].append(test.attrib['name'])
    result['junit_sha256']=digest(junit)
    result['status']='PASS' if process.returncode==0 and result['tests']>0 and result['assertions']>0 and not any(result[k] for k in ['failures','errors','skipped']) else 'FAIL'
    return result


def verify(value,evaluation):
    root,state=workspace(value,evaluation)
    if check_assets()!=state['adapter_freeze']:
        raise ValueError('Adapter freeze changed')
    if inventory(root/'app',source=True)!=state['source_files'] or inventory(root/'app/reviewer')!=state['reviewer_files']:
        raise ValueError('Clean candidate/reviewer assertions changed before verification')
    label='clean-'+str(1+len(list((root/'evidence').glob('clean-*.xml'))))
    result=execute(root,state,label)
    if evaluation=='BE-009':
        categories={f'test_negative_{x}' for x in ['unauthenticated','unauthorized','ownership','invalid','malicious','sensitive_fields']}
        if not categories <= set(result['candidate_negative_tests']):result['status']='INCOMPLETE'
    if evaluation=='BE-006' and result['status']=='PASS':
        command=[state['php'],'-n','reviewer/common/concurrency.php']
        p=subprocess.run(command,cwd=root/'app',env=environment(root),capture_output=True,text=True,timeout=45)
        (root/'evidence/concurrency.txt').write_text(p.stdout+p.stderr)
        result['concurrency']={'command':command,'exit_code':p.returncode,'log_sha256':digest(root/'evidence/concurrency.txt')}
        if p.returncode!=0:result['status']='FAIL'
    if inventory(root/'app',source=True)!=state['source_files'] or inventory(root/'app/reviewer')!=state['reviewer_files']:
        raise ValueError('Candidate/reviewer source mutated during verification')
    (root/'evidence/clean-result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def fault(value,evaluation,fault_id):
    root,state=workspace(value,evaluation)
    if check_assets()!=state['adapter_freeze']:raise ValueError('Adapter freeze changed')
    if inventory(root/'app/reviewer')!=state['reviewer_files']:raise ValueError('Reviewer assertions changed')
    if fault_id not in [f['id'] for f in json.loads((ASSETS/evaluation/'fixture.json').read_text())['fault_variants']]:
        raise ValueError('Unknown fault')
    baseline=json.loads((root/'evidence/clean-result.json').read_text())
    if baseline['status']!='PASS':raise ValueError('Fault sensitivity requires passing clean baseline')
    if inventory(root/'app',source=True)!=state['source_files']:raise ValueError('Clean source changed')
    # Create a wholly separate marked disposable variant; never modify clean source.
    variant=Path(tempfile.mkdtemp(prefix='laravel-adapter-',dir='/private/tmp'))
    try:
        shutil.copytree(root/'app',variant/'app');(variant/'evidence').mkdir()
        variant_state=dict(state,root=str(variant));(variant/MARKER).write_text(json.dumps(variant_state))
        definition=json.loads((ASSETS/evaluation/'faults'/f'{fault_id}.json').read_text())
        for change in definition['changes']:
            path=Path(change['path'])
            if path.is_absolute() or '..' in path.parts or path.parts[0]!='app':raise ValueError('Invalid mutation target')
            p=variant/'app'/path;text=p.read_text()
            if text.count(change['old'])!=change['expected_occurrences']:raise ValueError('Mutation binding does not match candidate; independent rebind required')
            p.write_text(text.replace(change['old'],change['new']))
        result=execute(variant,variant_state,fault_id,fault_id)
        result['clean_candidate_hash']=state['candidate_hash']
        target=definition['required_failure_prefix']
        detected=(result['exit_code']==1 and result['failures']>0 and result['errors']==0 and result['skipped']==0 and any(n.startswith(target) for n in result['failed_tests']))
        if evaluation=='BE-009':
            required='test_negative_ownership' if fault_id.endswith('F1') else 'test_negative_sensitive_fields'
            detected=detected and required in result['candidate_negative_failures']
        result['sensitivity']='PASS' if detected else 'FAIL'
        result['mutant_source_hash']=tree_hash(inventory(variant/'app',source=True))
        result['tests_unchanged']=inventory(variant/'app/reviewer')==inventory(root/'app/reviewer') and inventory(variant/'app/tests')==inventory(root/'app/tests')
        result['clean_unchanged']=inventory(root/'app',source=True)==state['source_files']
        if not result['tests_unchanged'] or not result['clean_unchanged']:result['sensitivity']='FAIL'
        for p in (variant/'evidence').iterdir():shutil.copyfile(p,root/'evidence'/p.name)
        (root/'evidence'/f'{fault_id}-result.json').write_text(json.dumps(result,indent=2)+'\n')
        return result
    finally:
        shutil.rmtree(variant)


def cleanup(value,evaluation=None):
    root,state=workspace(value,evaluation)
    if (root/'pgdata/postmaster.pid').exists():raise ValueError('PostgreSQL cluster must be stopped before cleanup')
    shutil.rmtree(root)
    return {'cleanup':'PASS','removed':str(root)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['setup','verify','fault','cleanup','check-freeze'])
    parser.add_argument('--evaluation',choices=IDS)
    parser.add_argument('--workspace');parser.add_argument('--vendor');parser.add_argument('--php',default='/opt/homebrew/opt/php@8.3/bin/php')
    parser.add_argument('--candidate');parser.add_argument('--fault-id')
    args=parser.parse_args()
    try:
        if args.action=='check-freeze':result={'freeze':check_assets(),'status':'PASS'}
        elif args.action=='setup':
            if not args.evaluation or not args.vendor:raise ValueError('setup requires --evaluation and --vendor')
            result={'workspace':str(setup(args.evaluation,args.vendor,args.php,args.candidate))}
        elif args.action=='verify':result=verify(args.workspace,args.evaluation)
        elif args.action=='fault':result=fault(args.workspace,args.evaluation,args.fault_id)
        else:result=cleanup(args.workspace,args.evaluation)
        print(json.dumps(result,indent=2))
        if result.get('status') in ['FAIL','INCOMPLETE'] and args.action!='fault' or result.get('sensitivity')=='FAIL':return 1
        return 0
    except (OSError,ValueError,KeyError,subprocess.TimeoutExpired,ET.ParseError) as exc:
        print(json.dumps({'status':'INCOMPLETE','error':str(exc)}),file=sys.stderr);return 2


if __name__=='__main__':
    sys.exit(main())
