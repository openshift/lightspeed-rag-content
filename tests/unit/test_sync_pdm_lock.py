"""Verify PDM lock refresh mode selection without running PDM."""

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/sync_pdm_lock.py"


def load_module():
    """Import the lock helper as a standalone module."""
    spec = importlib.util.spec_from_file_location("sync_pdm_lock", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LockModeTests(unittest.TestCase):
    """Pick a fresh lock for --update-all and a targeted update otherwise."""

    def setUp(self) -> None:
        """Load the helper and run from a temporary directory with overrides."""
        self.module = load_module()
        self.addCleanup(os.chdir, os.getcwd())
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        os.chdir(temporary.name)
        Path("requirements.overrides.txt").write_text(
            "banks>=2.5.1\n", encoding="utf-8"
        )

    def test_update_all_locks_without_reusing_pins(self) -> None:
        """A full refresh re-resolves every package instead of reusing pins."""
        with (
            mock.patch.object(self.module, "run_pdm") as run_pdm,
            mock.patch.object(sys, "argv", ["sync_pdm_lock.py", "--update-all"]),
        ):
            self.module.main()

        calls = run_pdm.call_args_list
        self.assertEqual(len(calls), 1)
        arguments = calls[0].args[0]
        self.assertEqual(arguments[0], "lock")
        self.assertNotIn("--update-reuse", arguments)

    def test_targeted_update_refreshes_requested_and_override_packages(self) -> None:
        """A named bump updates the package plus every override package."""
        with (
            mock.patch.object(self.module, "run_pdm") as run_pdm,
            mock.patch.object(sys, "argv", ["sync_pdm_lock.py", "urllib3"]),
        ):
            self.module.main()

        calls = run_pdm.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].args[0][0], "lock")
        update_arguments = calls[1].args[0]
        self.assertEqual(update_arguments[0], "update")
        self.assertIn("urllib3", update_arguments)
        self.assertIn("banks", update_arguments)

    def test_update_all_rejects_a_package_argument(self) -> None:
        """Combining --update-all with a package name is ambiguous."""
        with mock.patch.object(
            sys, "argv", ["sync_pdm_lock.py", "--update-all", "urllib3"]
        ):
            with self.assertRaises(SystemExit):
                self.module.main()


if __name__ == "__main__":
    unittest.main()
