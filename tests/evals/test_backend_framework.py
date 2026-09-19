"""Framework gate tests only: synthetic evidence is not a backend evaluation run."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('backend_verify', ROOT / 'evals/backend/verify.py')
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


class FrameworkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.number = 0

    def artifact(self, text='synthetic framework unit-test artifact'):
        self.number += 1
        p = self.root / str(self.number)
        p.write_text(text + str(self.number))
        return {'path': p.name, 'sha256': V.digest(p)}

    def manifest(self, evaluation='BE-001'):
        fixture_file = V.HERE / 'fixtures' / (evaluation + '.json')
        f = json.loads(fixture_file.read_text())
        candidate, assertions = self.artifact(), self.artifact()
        m = dict(campaign_id='UNIT-TEST-NOT-A-CAMPAIGN', evaluation_id=evaluation,
                 foundation_version='0.6.0', foundation_snapshot=self.artifact(),
                 implementer_context={'id': 'I', 'role': 'Backend Implementer', 'execution_record': self.artifact()},
                 reviewer_context={'id': 'R', 'role': 'Evaluation Reviewer', 'execution_record': self.artifact()},
                 security_context={'id': 'S', 'role': 'Security Reviewer', 'execution_record': self.artifact()},
                 candidate_revision='synthetic-test-revision', candidate_hash=candidate['sha256'], candidate_artifact=candidate,
                 fixture_version=f['fixture_version'], fixture_hash=V.digest(fixture_file),
                 fixture_freeze={'owner_context': 'R', 'before_implementation': True, 'assertions_hash': assertions['sha256'], 'assertions_artifact': assertions, 'record': self.artifact()},
                 tests_executed=[], test_result='PASS', criteria=[], fault_variants=[], clean_rerun='PASS', clean_rerun_evidence=self.artifact(),
                 security_review_required=True, security_review_result='PASS', security_evidence=self.artifact(), security_candidate_hash=candidate['sha256'],
                 human_correction=False, remediation_cycles=0, status='PASS', original_case_executed=True, adapted_scenario=False,
                 original_case_result='PASS', adapted_scenario_result='NOT APPLICABLE', adaptation_description='', adapted_scenario_evidence=None, missing_requirements=[], not_applicable_rationale='', hard_failures=[], score=80, score_dimensions=[{'dimension':name,'rating':4 if name=='Functional correctness' else 3,'evidence':self.artifact()} for name in ['Functional correctness','Architecture compliance','Security','Tests','Scope discipline','Documentation','Maintainability']],
                 metrics={'initial_implementation_outcome':'PASS', 'ai_self_corrections':0, 'independent_reviewer_findings':0, 'security_findings':0, 'human_code_corrections':0, 'architecture_corrections':{'ai':0,'human':0}, 'scope_violations':0,'process_violations':0})
        for check in f['required_tests']:
            evidence = self.artifact()
            m['tests_executed'].append({'id':check['id'], 'result':'PASS', 'assertions':5, 'errors':0, 'skipped':0, 'command':['synthetic-unit-test-only'], 'context_id':'R', 'candidate_hash':candidate['sha256'], 'tests_hash':assertions['sha256'], 'evidence':evidence})
            m['criteria'].append({'id':check['id'], 'result':'PASS', 'evidence':evidence})
        for fault in f['fault_variants']:
            mutant = self.artifact()
            m['fault_variants'].append({'id':fault['id'], 'expected_detection':'FAIL', 'actual_detection':'FAIL', 'result':'PASS', 'detected_test_ids':[fault['target_test']], 'assertion_failures':1, 'errors':0, 'context_id':'R', 'candidate_hash':candidate['sha256'], 'mutant_hash':mutant['sha256'], 'mutant_artifact':mutant, 'tests_hash':assertions['sha256'], 'disposable_copy':True, 'clean_unchanged':True, 'evidence':self.artifact()})
        return m

    def check(self, m):
        return V.verify(m, self.root)

    def test_all_nine_original_contracts(self):
        fields = ['initial_application_state','required_inputs','expected_outputs','forbidden_outputs','expected_side_effects','forbidden_side_effects','required_security_behavior','required_tests','independent_verification_checks','input_regressions','fault_variants']
        ids = {f'BE-{i:03}' for i in range(1,10)}
        self.assertEqual(ids, {p.stem for p in (V.HERE/'fixtures').glob('*.json')})
        faults = set()
        for evaluation in sorted(ids):
            with self.subTest(evaluation=evaluation):
                f = json.loads((V.HERE/'fixtures'/f'{evaluation}.json').read_text())
                self.assertTrue((ROOT/f['specification']).is_file())
                for key in fields: self.assertTrue(f[key], key)
                test_ids = {t['id'] for t in f['required_tests']}
                for fault in f['fault_variants']:
                    self.assertNotIn(fault['id'], faults)
                    faults.add(fault['id'])
                    self.assertIn(fault['target_test'], test_ids)
                    self.assertEqual('FAIL', fault['expected_fault_result'])
                    self.assertEqual('PASS', fault['expected_clean_result'])
                self.assertEqual('PASS', self.check(self.manifest(evaluation))['status'])

    def test_every_schema_field_is_required(self):
        m = self.manifest()
        for key in m:
            with self.subTest(key=key):
                missing = copy.deepcopy(m); del missing[key]
                with self.assertRaises(ValueError): self.check(missing)

    def test_unsupported_states_and_types_rejected(self):
        for value in ['INCOMPLETE','N/A','DONE',True,None]:
            m=self.manifest();m['status']=value
            with self.assertRaises(ValueError):self.check(m)
        for value in [True,-1,1.5]:
            m=self.manifest();m['remediation_cycles']=value
            with self.assertRaises(ValueError):self.check(m)

    def test_self_review_cannot_pass_and_partial_needs_actions(self):
        m=self.manifest();m['reviewer_context']['id']='I';m['fixture_freeze']['owner_context']='I'
        for t in m['tests_executed']+m['fault_variants']:t['context_id']='I'
        with self.assertRaisesRegex(ValueError,'PARTIAL'):self.check(m)
        m['status']=m['original_case_result']='PARTIAL'
        with self.assertRaisesRegex(ValueError,'every missing requirement'):self.check(m)
        m['missing_requirements']=[{'requirement':'L1 separate implementation/reviewer execution context','reason':'Same execution context','required_action':'Assign separate reviewer and rerun frozen evidence.'}]
        self.assertEqual('PARTIAL',self.check(m)['status'])
        m['missing_requirements'][0]['required_action']='   '
        with self.assertRaises(ValueError):self.check(m)

    def test_each_required_evidence_gate_blocks_pass(self):
        mutations=[lambda m:m['tests_executed'].clear(),lambda m:m['criteria'].clear(),lambda m:m['fault_variants'].clear(),lambda m:m['fixture_freeze'].update(before_implementation=False),lambda m:m.update(clean_rerun='NOT RUN'),lambda m:m.update(score=None),lambda m:m['tests_executed'][0].update(skipped=1),lambda m:m['tests_executed'][0].update(errors=1),lambda m:m['tests_executed'][0].update(assertions=0),lambda m:m['tests_executed'][0].update(candidate_hash='a'*64),lambda m:m['fixture_freeze'].update(assertions_hash='b'*64),lambda m:m['security_context'].update(id='I'),lambda m:m.update(security_candidate_hash='c'*64),lambda m:m.update(security_review_result='NOT RUN')]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                m=self.manifest();mutate(m)
                with self.assertRaises(ValueError):self.check(m)

    def test_escaped_mutant_fails_even_with_green_clean_tests(self):
        m=self.manifest();m['fault_variants'][0].update(actual_detection='PASS',result='FAIL',assertion_failures=0)
        m['status']=m['original_case_result']='FAIL'
        result=self.check(m)
        self.assertEqual('FAIL',result['status'])
        self.assertIn('Fault escaped detection',result['failures'][0])

    def test_infrastructure_error_is_not_fault_detection(self):
        m=self.manifest();m['fault_variants'][0].update(errors=1,result='PARTIAL')
        with self.assertRaisesRegex(ValueError,'PARTIAL'):self.check(m)

    def test_unsafe_mutation_and_hard_fail_override_score(self):
        for key in ['disposable_copy','clean_unchanged']:
            m=self.manifest();m['fault_variants'][0][key]=False;m['status']=m['original_case_result']='FAIL'
            self.assertEqual('FAIL',self.check(m)['status'])
        for finding in ['Critical vulnerability','Unresolved High','False authorization','Production access','Real customer data','Secret leakage','Fabricated evidence']:
            m=self.manifest();m['hard_failures']=[finding];m['status']=m['original_case_result']='FAIL'
            self.assertEqual('FAIL',self.check(m)['status'])

    def test_adapted_result_never_promotes_unexecuted_original(self):
        m=self.manifest();m.update(original_case_executed=False,adapted_scenario=True,adaptation_description='Different fixture scenario',adapted_scenario_evidence=self.artifact(),adapted_scenario_result='PASS',original_case_result='NOT RUN',status='NOT RUN')
        self.assertEqual('NOT RUN',self.check(m)['status'])
        m['status']=m['original_case_result']='PASS'
        with self.assertRaisesRegex(ValueError,'NOT RUN'):self.check(m)

    def test_hash_tamper_and_path_escape(self):
        for path in ['../escape','/etc/passwd']:
            m=self.manifest();m['candidate_artifact']['path']=path
            with self.assertRaises(ValueError):self.check(m)
        m=self.manifest();(self.root/m['candidate_artifact']['path']).write_text('tampered')
        with self.assertRaisesRegex(ValueError,'PARTIAL'):self.check(m)

    def test_cannot_waive_required_security_or_catalog_case(self):
        m=self.manifest();m['security_review_required']=False
        with self.assertRaisesRegex(ValueError,'Cannot waive'):self.check(m)
        m=self.manifest();m['status']='NOT APPLICABLE'
        with self.assertRaisesRegex(ValueError,'cannot be waived'):self.check(m)

    def test_duplicate_ids_and_unknown_fields_fail_closed(self):
        m=self.manifest();m['tests_executed'].append(m['tests_executed'][0])
        with self.assertRaises(ValueError):self.check(m)
        m=self.manifest();m['fake_clearance']=True
        with self.assertRaises(ValueError):self.check(m)


    def test_unrelated_failure_and_changed_assertions_do_not_detect_fault(self):
        m=self.manifest();m['fault_variants'][0]['detected_test_ids']=['unrelated-test']
        with self.assertRaisesRegex(ValueError,'Inconsistent fault'):self.check(m)
        m=self.manifest();m['fault_variants'][0]['tests_hash']='d'*64
        with self.assertRaisesRegex(ValueError,'PARTIAL'):self.check(m)

    def test_no_useful_evidence_is_not_partial_and_weights_cannot_change(self):
        m=self.manifest();m['tests_executed']=[];m['status']=m['original_case_result']='PARTIAL'
        with self.assertRaisesRegex(ValueError,'NOT RUN'):self.check(m)
        m=self.manifest();m['score']=100
        with self.assertRaisesRegex(ValueError,'weighted ratings'):self.check(m)

    def test_human_vs_ai_corrections(self):
        m=self.manifest();m['metrics']['ai_self_corrections']=2;m['remediation_cycles']=2
        self.assertEqual('PASS',self.check(m)['status'])
        m['metrics']['human_code_corrections']=1
        with self.assertRaises(ValueError):self.check(m)
        m['human_correction']=True
        self.assertEqual('PASS',self.check(m)['status'])


if __name__ == '__main__':
    unittest.main()
