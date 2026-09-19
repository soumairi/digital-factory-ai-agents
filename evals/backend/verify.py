#!/usr/bin/env python3
"""Read-only structural and evidence gate. Does not execute untrusted commands.

Usage: python3 evals/backend/verify.py MANIFEST EVIDENCE_ROOT
No schema packages required. Implements precisely the JSON Schema keywords used
by the shipped schema; unsupported validation keywords fail closed.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATES = {'PASS', 'FAIL', 'PARTIAL', 'NOT RUN', 'NOT APPLICABLE'}


def validate(value, schema, path='$'):
    supported = {'$schema', 'title', 'type', 'properties', 'required',
                 'additionalProperties', 'items', 'enum', 'const', 'minLength',
                 'minimum', 'maximum', 'pattern'}
    if set(schema) - supported:
        raise ValueError(f'{path}: unsupported schema keywords')
    types = schema.get('type', [])
    types = [types] if isinstance(types, str) else types
    matches = {'null': value is None, 'object': isinstance(value, dict),
               'array': isinstance(value, list), 'string': isinstance(value, str),
               'boolean': type(value) is bool, 'integer': type(value) is int,
               'number': type(value) in (int, float)}
    if types and not any(matches[t] for t in types):
        raise ValueError(f'{path}: invalid type')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(f'{path}: invalid enum')
    if 'const' in schema and value != schema['const']:
        raise ValueError(f'{path}: invalid constant')
    if isinstance(value, str):
        if len(value.strip()) < schema.get('minLength', 0):
            raise ValueError(f'{path}: empty string')
        if 'pattern' in schema and re.search(schema['pattern'], value) is None:
            raise ValueError(f'{path}: invalid pattern')
    if type(value) in (int, float):
        if not float('-inf') < value < float('inf'):
            raise ValueError(f'{path}: non-finite number')
        if value < schema.get('minimum', value) or value > schema.get('maximum', value):
            raise ValueError(f'{path}: out of range')
    if isinstance(value, dict):
        if set(schema.get('required', [])) - value.keys():
            raise ValueError(f'{path}: missing required fields')
        properties = schema.get('properties', {})
        if schema.get('additionalProperties') is False and value.keys() - properties.keys():
            raise ValueError(f'{path}: unknown fields')
        for k, v in value.items():
            if k in properties:
                validate(v, properties[k], path + '.' + k)
    if isinstance(value, list):
        for i, v in enumerate(value):
            validate(v, schema['items'], f'{path}[{i}]')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(manifest, evidence_root):
    validate(manifest, json.loads((HERE / 'schema/evidence-manifest.schema.json').read_text()))
    m = manifest
    fixture_file = HERE / 'fixtures' / (m['evaluation_id'] + '.json')
    fixture = json.loads(fixture_file.read_text())
    missing, failures = [], list(m['hard_failures'])
    root = Path(evidence_root).resolve()

    def need(condition, reason):
        if not condition:
            missing.append(reason)

    def artifact(ref):
        if ref is None:
            return False
        path = Path(ref['path'])
        if path.is_absolute() or '..' in path.parts:
            return False
        target = (root / path).resolve()
        return target.is_relative_to(root) and target.is_file() and digest(target) == ref['sha256']

    implementer, reviewer = m['implementer_context'], m['reviewer_context']
    independent = implementer['id'] != reviewer['id']
    need(independent, 'L1 separate implementation/reviewer execution context')
    need(implementer['role'] == 'Backend Implementer' and reviewer['role'] == 'Evaluation Reviewer', 'Correct role assignments')
    need(artifact(implementer['execution_record']) and artifact(reviewer['execution_record']), 'Execution-context provenance')
    need(implementer['execution_record'] != reviewer['execution_record'], 'Separate context records')
    need(artifact(m['foundation_snapshot']), 'Foundation snapshot evidence')
    need(m['fixture_version'] == fixture['fixture_version'] and m['fixture_hash'] == digest(fixture_file), 'Exact reviewer fixture version/hash')
    freeze = m['fixture_freeze']
    need(artifact(freeze['assertions_artifact']) and freeze['assertions_artifact']['sha256'] == freeze['assertions_hash'], 'Frozen executable assertions artifact')
    need(freeze['owner_context'] == reviewer['id'] and freeze['before_implementation'] and artifact(freeze['record']), 'Reviewer assertion ownership frozen before implementation')
    candidate = m['candidate_artifact']
    need(bool(m['candidate_revision']) and artifact(candidate) and candidate['sha256'] == m['candidate_hash'] if candidate else False, 'Frozen candidate revision/hash evidence')
    required = {t['id'] for t in fixture['required_tests']}
    tests = {t['id']: t for t in m['tests_executed']}
    criteria = {t['id']: t for t in m['criteria']}
    if len(tests) != len(m['tests_executed']) or len(criteria) != len(m['criteria']):
        raise ValueError('Duplicate test/criterion IDs')
    need(required <= tests.keys(), 'All original required tests executed')
    need(required == criteria.keys(), 'All original criteria represented exactly')
    for t in m['tests_executed']:
        if t['result'] == 'FAIL':
            failures.append('Clean test failed: ' + t['id'])
        need(t['result'] == 'PASS' and t['assertions'] > 0 and t['errors'] == 0 and t['skipped'] == 0 and bool(t['command']) and t['context_id'] == reviewer['id'] and t['candidate_hash'] == m['candidate_hash'] and t['tests_hash'] == freeze['assertions_hash'] and artifact(t['evidence']), 'Independent clean test: ' + t['id'])
    for criterion in m['criteria']:
        if criterion['result'] == 'FAIL':
            failures.append('Criterion failed: ' + criterion['id'])
        need(criterion['result'] == 'PASS' and artifact(criterion['evidence']), 'Criterion evidence: ' + criterion['id'])
    if m['test_result'] == 'FAIL' or m['clean_rerun'] == 'FAIL':
        failures.append('Clean baseline/rerun failed')
    need(m['test_result'] == 'PASS' and m['clean_rerun'] == 'PASS' and artifact(m['clean_rerun_evidence']), 'Passing clean baseline and post-mutation rerun')
    expected_faults = {f['id'] for f in fixture['fault_variants'] if f['required']}
    faults = {f['id']: f for f in m['fault_variants']}
    if len(faults) != len(m['fault_variants']) or faults.keys() - {f['id'] for f in fixture['fault_variants']}:
        raise ValueError('Duplicate/unknown fault IDs')
    need(expected_faults <= faults.keys(), 'All required fault variants')
    for f in m['fault_variants']:
        if f['actual_detection'] == 'PASS':
            failures.append('Fault escaped detection: ' + f['id'])
        if not f['clean_unchanged'] or not f['disposable_copy']:
            failures.append('Unsafe fault isolation: ' + f['id'])
        target_test = next(v['target_test'] for v in fixture['fault_variants'] if v['id'] == f['id'])
        detected = f['actual_detection'] == 'FAIL' and f['assertion_failures'] > 0 and f['errors'] == 0 and target_test in f['detected_test_ids']
        expected_result = 'PASS' if detected else ('FAIL' if f['actual_detection'] == 'PASS' else 'PARTIAL')
        if f['result'] != expected_result:
            raise ValueError('Inconsistent fault detection result: ' + f['id'])
        need(detected and f['context_id'] == reviewer['id'] and f['candidate_hash'] == m['candidate_hash'] and f['mutant_hash'] != m['candidate_hash'] and artifact(f['mutant_artifact']) and f['mutant_artifact']['sha256'] == f['mutant_hash'] and f['tests_hash'] == freeze['assertions_hash'] and artifact(f['evidence']), 'Independent fault detection: ' + f['id'])
    if fixture['security_review_required'] and not m['security_review_required']:
        raise ValueError('Cannot waive fixture security review requirement')
    if m['security_review_required']:
        sec = m['security_context']
        if m['security_review_result'] == 'FAIL':
            failures.append('Security review failed')
        need(sec is not None and sec['role'] == 'Security Reviewer' and sec['id'] != implementer['id'] and artifact(sec['execution_record']) and sec['execution_record'] != implementer['execution_record'] and m['security_review_result'] == 'PASS' and artifact(m['security_evidence']) and m['security_candidate_hash'] == m['candidate_hash'], 'Independent required Security review')
    if m['metrics']['scope_violations']:
        failures.append('Scope violation')
    need(m['metrics']['process_violations'] == 0, 'Unresolved process violations')
    if m['human_correction'] != (m['metrics']['human_code_corrections'] > 0 or m['metrics']['architecture_corrections']['human'] > 0):
        raise ValueError('Human correction disagrees with correction metrics')
    weights = {'Functional correctness': 20, 'Architecture compliance': 15,
               'Security': 25, 'Tests': 15, 'Scope discipline': 10,
               'Documentation': 5, 'Maintainability': 10}
    dimensions = {d['dimension']: d for d in m['score_dimensions']}
    if len(dimensions) != len(m['score_dimensions']):
        raise ValueError('Duplicate scoring dimensions')
    need(dimensions.keys() == weights.keys() and all(artifact(d['evidence']) for d in dimensions.values()), 'Seven original score dimensions with evidence')
    if dimensions.keys() == weights.keys():
        total = sum(weights[k] * dimensions[k]['rating'] / 4 for k in weights)
        if m['score'] != total:
            raise ValueError('Score disagrees with original weighted ratings')
    if m['score'] is not None and m['score'] < 70:
        failures.append('Original weighted score below70')
    need(m['score'] is not None, 'Original Foundation score')
    if m['adapted_scenario'] and not m['adaptation_description'].strip():
        raise ValueError('Adaptation must be explained')
    if not m['adapted_scenario'] and m['adapted_scenario_result'] != 'NOT APPLICABLE':
        raise ValueError('No adapted scenario exists')
    # All nine catalog cases apply to the initial suite; no self-waived N/A.
    if m['status'] == 'NOT APPLICABLE':
        raise ValueError('Catalog cases cannot be waived as NOT APPLICABLE')
    if not m['original_case_executed'] and not m['adapted_scenario'] and m['tests_executed']:
        raise ValueError('Tests supplied without any executed scenario')
    if m['adapted_scenario'] and m['adapted_scenario_result'] != 'NOT RUN' and not artifact(m['adapted_scenario_evidence']):
        raise ValueError('Adapted result needs separate reviewer evidence')
    if m['adapted_scenario_result'] == 'PASS' and (missing or failures):
        raise ValueError('Adapted PASS cannot bypass evidence/independence gates')
    if failures:
        expected = 'FAIL'
    elif not m['original_case_executed'] or not any(artifact(t['evidence']) for t in m['tests_executed']):
        expected = 'NOT RUN'
    elif missing:
        expected = 'PARTIAL'
    else:
        expected = 'PASS'
    if m['status'] != expected or m['original_case_result'] != expected:
        raise ValueError('Original-case status must be ' + expected)
    if expected == 'PARTIAL':
        recorded = {v['requirement'] for v in m['missing_requirements']}
        if not set(missing) <= recorded:
            raise ValueError('PARTIAL must list every missing requirement, reason and required action: ' + '; '.join(missing))
    if expected == 'PASS' and m['missing_requirements']:
        raise ValueError('PASS cannot contain missing requirements')
    if expected == 'PASS' and (m['metrics']['independent_reviewer_findings'] is None or m['security_review_required'] and m['metrics']['security_findings'] is None):
        raise ValueError('PASS requires completed reviewer finding counts')
    return {'status': expected, 'missing_requirements': missing, 'failures': failures,
            'assurance': 'Local evidence checks only; context provenance and assertions still require reviewer/human authentication.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('evidence_root', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(json.loads(args.manifest.read_text()), args.evidence_root), indent=2))
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(1, 'Invalid evidence manifest: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
