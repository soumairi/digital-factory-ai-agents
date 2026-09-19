#!/usr/bin/env python3
"""Read-only consistency verification; does not assert independent clearance."""
import hashlib,json,xml.etree.ElementTree as ET
from pathlib import Path
c=Path(__file__).resolve().parents[1]
r=c.parents[2]
def read(p):return json.loads((c/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=read('final/eval-results.json');assert a['planned_cases']==a['executed_cases']==len(a['cases'])==9
for key,status in [('passed_cases','PASS'),('failed_cases','FAIL'),('partial_cases','PARTIAL'),('not_run_cases','NOT RUN')]:assert a[key]==sum(v['status']==status for v in a['cases'])
for case in a['cases']:
 assert read('cases/'+case['id']+'/evidence.json')==case
 assert (r/case['specification']).is_file()
 assert case['candidate_revision']==a['candidate_revision']
 assert len(list((c/'cases'/case['id']).glob('*.md')))==5
 for word in ['Functional Correctness','Architecture Compliance','Security-by-Default','Automated Testing','Scope Discipline','Documentation','Maintainability','Process/Governance']:
  assert word in (c/'cases'/case['id']/'score.md').read_text()
manifest=read('candidate/source-sha256.json')
assert all(sha(c/'candidate/final'/p)==v for p,v in manifest.items())
assert a['candidate_revision']=='sha256:'+hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert sha(c/'candidate/final/tests/Feature/CampaignTest.php')==(c/'campaign/assertions-before-implementation.sha256').read_text().split()[0]
assert all(sha(r/p)==v for p,v in read('campaign/foundation-sha256.json').items())
j=ET.parse(c/'evidence/final-junit.xml').getroot().find('testsuite')
assert int(j.attrib['tests'])==57 and int(j.attrib['assertions'])==951
assert all(int(j.attrib[k])==0 for k in ['failures','errors','skipped'])
f=read('evidence/fault-results.json');assert len(f)==8 and all(x['detected'] for x in f)
for fault in f:
 t=(c/fault['log']).read_text();assert 'FAILURES!' in t and 'Errors:' not in t
 assert not fault['independent_evaluator']
assert a['scores']['suite_score'] is None and a['recommendation']=='SANDBOX READY'
# Exclude this verifier's output while stdout is redirected to it.
for p in c.rglob('*.json'):
 if p != c/'evidence/artifact-verification.json': json.loads(p.read_text())
print(json.dumps({'status':'PASS','cases':9,'json_files_valid':len(list(c.rglob('*.json'))),'final_tests':57,'assertions':951,'faults_detected':8,'source_and_foundation_checksums':'MATCH','frozen_assertions':'UNCHANGED','independent_clearance':False},indent=2))
