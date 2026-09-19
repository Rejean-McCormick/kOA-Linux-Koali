import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'ci/scripts'))
from gate_scope import partition, is_qemu

def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), ROOT/'ci/scripts'/name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class GateTests(unittest.TestCase):
    def test_real_inventory_splits_without_loss(self):
        for name in ('run-security.py','run-offline.py','run-system-tests.py'):
            mod = load(name)
            policy = ROOT/mod.DEFAULT_POLICY if mod.DEFAULT_POLICY else None
            commands, required, _, _ = mod._build_commands(ROOT, policy)
            all_cmd, _, _ = partition(ROOT, commands, required, 'all')
            local, _, omitted = partition(ROOT, commands, required, 'local')
            qemu, _, _ = partition(ROOT, commands, required, 'qemu')
            self.assertTrue(local)
            self.assertTrue(qemu)
            self.assertFalse(any(is_qemu(cmd) for cmd in local))
            self.assertTrue(all(is_qemu(cmd) for cmd in qemu))
            self.assertCountEqual(all_cmd, local+qemu)
            self.assertEqual(omitted, qemu)

    def test_failed_document_check_and_missing_vm_do_not_stop_source_tests(self):
        for name in ('run-security.py','run-offline.py','run-system-tests.py'):
            mod = load(name)
            commands = [[sys.executable, 'docs/check.py'], [sys.executable,'-m','pytest','tests/security/test_secret_absence.py','tests/system/test_qemu_boot.py'], [sys.executable,'after.py']]
            called=[]
            def run(argv, **kwargs):
                called.append(argv)
                return subprocess.CompletedProcess(argv, 1 if 'docs/check.py' in argv else 0)
            with tempfile.TemporaryDirectory() as tmp, patch.object(mod,'_build_commands',return_value=(commands,[],{},None)), patch.object(mod,'_git',return_value=None), patch.object(mod,'_qemu_runtime_environment',return_value=({},['image absent'])), patch.object(mod.subprocess,'run',side_effect=run), patch.object(sys,'argv',[name,'--repo-root',str(ROOT),'--evidence-dir',tmp]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(mod.main(), 1)
                report=json.loads((Path(tmp)/f'{mod.SUITE_ID}-gate-report.json').read_text())
            self.assertEqual(len(called),3)
            self.assertTrue(any('test_secret_absence.py' in ' '.join(cmd) for cmd in called))
            self.assertEqual(report['outcome'],'failed')
            self.assertTrue(any(r['outcome']=='blocked' for r in report['commands']))

    def test_snapshot_only_is_excluded_from_normative_docs(self):
        spec=importlib.util.spec_from_file_location('contract_first',ROOT/'docs/tools/_contract_first.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ('CODE_SNAPSHOT_MANIFEST.md','real-contract.md'):
                (root/name).write_text('no metadata')
            with patch.object(mod,'ROOT',root):
                self.assertEqual([p.name for p in mod.source_files('*.md')],['real-contract.md'])
                self.assertIsNone(mod.metadata(root/'real-contract.md'))

if __name__ == '__main__': unittest.main()
