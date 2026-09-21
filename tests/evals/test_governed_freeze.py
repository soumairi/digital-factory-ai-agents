"""Freeze governance only: synthetic files, no Backend campaign/application execution."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('freeze', ROOT/'evals/backend/freeze.py')
F = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(F)


class GovernedFreezeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for d in F.DIRECTORIES: (self.root/d).mkdir(parents=True, exist_ok=True)
        for p in F.FILES: self.write(p, '0.6.1' if p == 'VERSION' else 'policy')
        self.paths = {
            'adapter': 'evals/backend/adapters/laravel/application.php',
            'fixture': 'evals/backend/fixtures/BE-001.json',
            'verifier': 'evals/backend/verify.py',
            'fault': 'evals/backend/adapters/laravel/BE-001/faults/F1.json',
            'manifest': 'evals/backend/adapters/laravel/manifest.json',
            'rule': 'docs/14-backend-evaluation-protocol.md',
            'spec': 'evals/backend/BE-001-simple-crud.md',
            'expected': 'evals/backend/adapters/laravel/BE-001/expected-results.json',
        }
        for p in self.paths.values(): self.write(p, 'governed')
        self.write(F.SNAPSHOT, json.dumps(F.build(self.root)))
        self.pin = F.validate(self.root)

    def write(self, p, text):
        target = self.root/p; target.parent.mkdir(parents=True, exist_ok=True); target.write_text(text)

    def unchanged(self): self.assertEqual(self.pin, F.validate(self.root, self.pin))

    def test_pycache_creation_is_not_mutation(self):
        self.write('evals/backend/adapters/laravel/__pycache__/runner.cpython-314.pyc', 'runtime')
        self.unchanged()

    def test_standalone_pyc_is_not_mutation(self):
        self.write('evals/backend/adapters/laravel/runner.pyc', 'runtime'); self.unchanged()

    def test_temporary_output_is_not_mutation(self):
        self.write('evals/backend/adapters/laravel/tmp/test-output.log', 'output'); self.unchanged()

    def test_external_generated_evidence_is_not_mutation(self):
        self.write('validation/new-test-output/results.json', '{}'); self.unchanged()

    def test_other_narrow_runtime_artifacts(self):
        for p in ['.DS_Store', '.coverage', '.pytest_cache/v/cache/nodeids']:
            self.write('evals/backend/' + p, 'runtime')
        self.unchanged()

    def mutation(self, kind):
        self.write(self.paths[kind], 'changed')
        with self.assertRaises(ValueError): F.validate(self.root, self.pin)

    def test_adapter_mutation(self): self.mutation('adapter')
    def test_fixture_mutation(self): self.mutation('fixture')
    def test_verifier_mutation(self): self.mutation('verifier')
    def test_fault_mutation(self): self.mutation('fault')
    def test_manifest_mutation(self): self.mutation('manifest')
    def test_foundation_rule_mutation(self): self.mutation('rule')
    def test_spec_mutation(self): self.mutation('spec')
    def test_expected_results_mutation(self): self.mutation('expected')

    def test_no_source_hidden_in_runtime_directories(self):
        for suffix in ['.py', '.sh', '.json', '.md', '.php']:
            with self.subTest(suffix=suffix):
                p='evals/backend/adapters/laravel/__pycache__/hidden'+suffix
                self.write(p, 'new governed code')
                with self.assertRaises(ValueError): F.validate(self.root)
                (self.root/p).unlink()

    def test_runtime_directory_is_not_a_blanket_exclusion(self):
        for folder in ['tmp', 'coverage', '.pytest_cache', '__pycache__']:
            with self.subTest(folder=folder):
                path = 'evals/backend/' + folder + '/fixture.json'
                self.write(path, '{}')
                with self.assertRaises(ValueError): F.validate(self.root)
                (self.root/path).unlink()

    def test_symlinked_parent_is_rejected(self):
        folder=self.root/'evals/backend/adapters/linked'
        folder.symlink_to(self.root/'shared', target_is_directory=True)
        with self.assertRaises(ValueError): F.validate(self.root)

    def test_deleted_governed_file(self):
        (self.root/self.paths['fixture']).unlink()
        with self.assertRaises(ValueError): F.validate(self.root)

    def test_inventory_rewrite_cannot_override_campaign_pin(self):
        self.write(self.paths['adapter'], 'changed')
        self.write(F.SNAPSHOT, json.dumps(F.build(self.root)))
        with self.assertRaises(ValueError): F.validate(self.root, self.pin)

    def test_omitted_asset_is_rejected(self):
        snapshot=json.loads((self.root/F.SNAPSHOT).read_text());snapshot['assets'].pop()
        self.write(F.SNAPSHOT, json.dumps(snapshot))
        with self.assertRaises(ValueError): F.validate(self.root)

    def test_symlink_disguised_as_runtime_is_rejected(self):
        (self.root/'evals/backend/hidden.pyc').symlink_to(self.root/'VERSION')
        with self.assertRaises(ValueError): F.validate(self.root)

    def test_real_repository_inventory(self):
        self.assertEqual(64, len(F.validate(ROOT)))


if __name__ == '__main__': unittest.main()
