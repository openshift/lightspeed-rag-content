"""Test VM cleanup reporting without SSH, cluster credentials, or containers."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / ".tekton/integration-tests/scripts/run-in-vm.sh"


class VMCleanupTests(unittest.TestCase):
    """Distinguish product failure, artifact loss, and failed credential cleanup."""

    def finish(
        self, ssh_status: int, rsync_status: int
    ) -> tuple[subprocess.CompletedProcess, dict]:
        """Execute the runner's actual EXIT handler with offline SSH/rsync stand-ins."""
        function = (
            "finish() {"
            + RUNNER.read_text()
            .split("finish() {", 1)[1]
            .split("\ntrap finish EXIT", 1)[0]
        )
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            commands = work / "bin"
            commands.mkdir()
            for name, status in (("ssh", ssh_status), ("rsync", rsync_status)):
                command = commands / name
                command.write_text(f"#!/bin/sh\nexit {status}\n")
                command.chmod(0o700)
            result_path = work / "result.json"
            script = (
                "set -euo pipefail\nSSH_ARGS=()\n"
                + function
                + "\ntrap finish EXIT\nexit 0\n"
            )
            result = subprocess.run(
                ["bash", "-c", script],
                env={
                    **os.environ,
                    "PATH": f"{commands}:{os.environ['PATH']}",
                    "LOCAL_WORK": str(work / "local"),
                    "REMOTE_DIR": "/safe/test-work",
                    "IS_LOCALHOST": "false",
                    "SSH_HOST": "offline-test",
                    "RESULTS_TEST_OUTPUT_PATH": str(result_path),
                },
                capture_output=True,
                text=True,
                check=False,
            )
            return result, json.loads(result_path.read_text())

    def test_success_with_confirmed_cleanup_passes(self) -> None:
        """Report success when artifacts and credential cleanup both complete."""
        result, output = self.finish(ssh_status=0, rsync_status=0)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output["result"], "SUCCESS")
        self.assertEqual(output["warnings"], 0)

    def test_unconfirmed_credential_cleanup_fails(self) -> None:
        """Fail rather than report clean success when remote secrets remain."""
        result, output = self.finish(ssh_status=1, rsync_status=0)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output["result"], "FAILURE")
        self.assertGreater(output["warnings"], 0)
        self.assertIn("credential cleanup", result.stderr)

    def test_artifact_retrieval_failure_warns(self) -> None:
        """Preserve product success but expose missing retained artifacts."""
        result, output = self.finish(ssh_status=0, rsync_status=1)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output["result"], "SUCCESS")
        self.assertGreater(output["warnings"], 0)
        self.assertIn("artifacts", result.stderr)


if __name__ == "__main__":
    unittest.main()
