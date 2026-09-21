"""Safety/contract tests for the adapter runner, not a Backend evaluation campaign."""
import importlib.util
import json
import shutil
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
SPEC=importlib.util.spec_from_file_location('laravel_adapter_runner',ROOT/'evals/backend/adapters/laravel/runner.py')
R=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(R)

class RunnerTests(unittest.TestCase):
    def test_all_original_fixtures_and_faults_bound(self):
        ids=[]
        for evaluation in R.IDS:
            d=R.ASSETS/evaluation
            source=json.loads((ROOT/'evals/backend/fixtures'/f'{evaluation}.json').read_text())
            self.assertEqual(source,json.loads((d/'fixture.json').read_text()))
            for fault in source['fault_variants']:
                f=json.loads((d/'faults'/f'{fault["id"]}.json').read_text())
                ids.append(f['id']);self.assertTrue(f['changes']);self.assertTrue(f['required_failure_prefix'])
                for change in f['changes']:
                    text=(R.ASSETS/'calibration/application'/change['path']).read_text()
                    self.assertEqual(change['expected_occurrences'],text.count(change['old']))
                self.assertEqual(fault['target_test'],f['target_test'])
            for name in ['setup.sh','verify.sh','cleanup.sh','expected-results.json']:
                self.assertTrue((d/name).is_file())
        self.assertEqual(19,len(ids));self.assertEqual(len(ids),len(set(ids)))

    def test_environment_does_not_inherit_credentials(self):
        with patch.dict('os.environ',{'DB_URL':'DO_NOT_INHERIT','AWS_SECRET_ACCESS_KEY':'DO_NOT_INHERIT','APP_ENV':'production'}):
            env=R.environment(Path('/private/tmp/example'))
            self.assertEqual('',env['DB_URL']);self.assertEqual(':memory:',env['DB_DATABASE'])
            self.assertNotIn('AWS_SECRET_ACCESS_KEY',env);self.assertEqual('testing',env['APP_ENV'])

    def test_cleanup_refuses_unmarked_or_arbitrary_targets(self):
        with tempfile.TemporaryDirectory(prefix='laravel-adapter-',dir='/private/tmp') as name:
            with self.assertRaises(FileNotFoundError):R.cleanup(name)
            self.assertTrue(Path(name).exists())
        with self.assertRaises(ValueError):R.cleanup('/private/tmp')
        with self.assertRaises(ValueError):R.cleanup(str(ROOT))

    def test_cleanup_refuses_symlink_and_mismatched_marker(self):
        with tempfile.TemporaryDirectory(prefix='laravel-adapter-',dir='/private/tmp') as name:
            p=Path(name);link=p.parent/(p.name+'-link');link.symlink_to(p,target_is_directory=True)
            try:
                with self.assertRaises(ValueError):R.cleanup(str(link))
            finally:link.unlink()
            (p/R.MARKER).write_text(json.dumps({'root':'wrong','created_by':'laravel-reviewer-adapter-1.0.0'}))
            with self.assertRaises(ValueError):R.cleanup(name)

    def test_inventory_rejects_symlinks_and_captures_source_changes(self):
        with tempfile.TemporaryDirectory() as name:
            p=Path(name);(p/'app').mkdir();f=p/'app/a.php';f.write_text('one');a=R.inventory(p,source=True)
            f.write_text('two');self.assertNotEqual(a,R.inventory(p,source=True))
            (p/'link').symlink_to(f)
            with self.assertRaises(ValueError):R.inventory(p)

    def test_result_parser_does_not_accept_skips_as_clean_success(self):
        # Exercise actual JUnit interpretation with a mocked PHP process only.
        with tempfile.TemporaryDirectory(prefix='laravel-adapter-',dir='/private/tmp') as name:
            root=Path(name);(root/'app').mkdir();(root/'evidence').mkdir()
            (root/'evidence/clean.xml').write_text('<testsuites><testsuite tests="1" assertions="0" failures="0" errors="0" skipped="1"><testcase name="skipped"/></testsuite></testsuites>')
            class Result: returncode=0;stdout='';stderr=''
            with patch.object(R.subprocess,'run',return_value=Result()):
                result=R.execute(root,{'php':'/synthetic/php'},'clean')
            self.assertEqual('FAIL',result['status'])

    def test_external_review_output_preserves_exact_asset_inventory(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name);assets=root/'evals/backend/adapters/laravel';assets.mkdir(parents=True)
            snapshot=json.loads((ROOT/'evals/backend/governed-inventory.json').read_text())
            for entry in snapshot['assets']:
                target=root/entry['path'];target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/entry['path'],target)
            shutil.copyfile(ROOT/'evals/backend/governed-inventory.json',root/'evals/backend/governed-inventory.json')
            owned=assets/'runner.py'
            with patch.object(R,'ASSETS',assets):
                before=R.check_assets()
                output=root/'validation/adapter-reviews/REVIEW-TEST';output.mkdir(parents=True)
                for filename in ['independent-review.md','independent-review.json']:
                    (output/filename).write_text('separate review')
                self.assertEqual(before,R.check_assets())
                # No filename exemption: an internal report is still rejected.
                internal=assets/'independent-review.json';internal.write_text('{}')
                with self.assertRaises(ValueError):R.check_assets()
                internal.unlink()
                owned.write_text('changed evaluator')
                with self.assertRaises(ValueError):R.check_assets()
                owned.unlink()
                with self.assertRaises(ValueError):R.check_assets()

    def test_asset_freeze_matches_inventory(self):
        self.assertEqual(64,len(R.check_assets()))

if __name__=='__main__':unittest.main()
