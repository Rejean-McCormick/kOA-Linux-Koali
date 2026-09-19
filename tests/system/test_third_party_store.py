"""Isolated tests: no network, package installs or GUI required."""
import importlib.util
import io
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('third_party_store', ROOT / 'host/store/third-party-store.py')
store = importlib.util.module_from_spec(spec)
spec.loader.exec_module(store)


class ThirdPartyStoreTests(unittest.TestCase):
    def test_catalog_is_read_only(self):
        with patch.object(store, 'run') as run, patch('sys.stdout', new=io.StringIO()):
            self.assertEqual(store.main(['catalog']), 0)
            run.assert_not_called()

    def test_cancel_does_not_install(self):
        with patch.object(store, 'run', return_value=subprocess.CompletedProcess([], 1, '')):
            self.assertEqual(store.selection(), [])

    def test_selection_rejects_unlisted_ids(self):
        with patch.object(store, 'run', return_value=subprocess.CompletedProcess([], 0, 'untrusted.App')):
            with self.assertRaises(ValueError):
                store.selection()

    def test_existing_system_or_user_app_is_skipped(self):
        with patch.object(store, 'installed', return_value=True), patch.object(store, 'run') as run:
            result = store.install_apps(['org.mozilla.firefox'], io.StringIO())
            self.assertEqual(result[0][1], 'déjà installé')
            run.assert_not_called()

    def test_partial_failure_continues_and_uses_user_scope(self):
        ids = [store.CATALOG[0][0], store.CATALOG[1][0]]
        with patch.object(store, 'installed', side_effect=[False, False, True]), patch.object(store, 'run', side_effect=[subprocess.CompletedProcess([], 1), subprocess.CompletedProcess([], 0)]) as run:
            result = store.install_apps(ids, io.StringIO())
            self.assertEqual([row[1] for row in result], ['échec', 'installé'])
            for call in run.call_args_list:
                argv = call.args[0]
                self.assertIn('--user', argv)
                self.assertNotIn('--system', argv)
                self.assertEqual(argv[-2], store.REMOTE)

    def test_untrusted_remote_is_rejected(self):
        with patch.object(store, 'run', return_value=subprocess.CompletedProcess([], 0, store.REMOTE + '\thttps://example.org/repo\n')) as run:
            with self.assertRaises(RuntimeError):
                store.configure_remote(io.StringIO())
            self.assertEqual(run.call_count, 1)

    def test_existing_official_remote_is_reused(self):
        with patch.object(store, 'run', return_value=subprocess.CompletedProcess([], 0, store.REMOTE + '\thttps://dl.flathub.org/repo/\n')) as run:
            store.configure_remote(io.StringIO())
            self.assertEqual(run.call_count, 1)

    def test_remote_failure_stops(self):
        with patch.object(store, 'run', side_effect=[subprocess.CompletedProcess([], 0, ''), subprocess.CompletedProcess([], 1)]):
            with self.assertRaises(RuntimeError):
                store.configure_remote(io.StringIO())


if __name__ == '__main__':
    unittest.main()
