"""Exercise workflow filesystem permissions in rootful and rootless Podman modes."""

import os
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / "tests/integration-konflux/pipeline-konflux.sh"


class WorkflowPermissionTests(unittest.TestCase):
    """Use real chmod with stand-ins for Podman namespaces and privileged chown."""

    def check_permissions(self, rootless: bool) -> None:
        """Run the actual credential and index setup without containers or secrets."""
        source = WORKFLOW.read_text()
        credentials = source.split('mkdir -p "$WORK_DIR/output"', 1)[1].split(
            "\nAUTH_ARGS=()", 1
        )[0]
        credentials = 'mkdir -p "$WORK_DIR/output"' + credentials
        index_permissions = next(
            line
            for line in source.splitlines()
            if "chmod" in line and '"$WORK_DIR/index"' in line
        )
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            corpus = work / "corpus"
            corpus.mkdir()
            (corpus / "manual.md").write_text("Offline corpus")
            commands = work / "bin"
            commands.mkdir()
            podman = commands / "podman"
            podman.write_text(
                '#!/bin/bash\nprintf "%s\\n" "$*" >> "$COMMAND_LOG"\n'
                '[[ "$1" == unshare ]] || exit 1\n'
                '[[ "$ROOTLESS" == true ]] || {\n'
                'echo "please use unshare with rootless" >&2; exit 125; }\n'
                'shift\nexec "$@"\n'
            )
            podman.chmod(0o700)
            chown = commands / "chown"
            chown.write_text(
                '#!/bin/bash\nprintf "chown %s\\n" "$*" >> "$COMMAND_LOG"\n'
            )
            chown.chmod(0o700)
            log = work / "commands.log"
            result = subprocess.run(
                [
                    "bash",
                    "-c",
                    "set -euo pipefail\numask 077\n"
                    + credentials
                    + '\nprintf index > "$WORK_DIR/index/data"\n'
                    + index_permissions,
                ],
                env={
                    **os.environ,
                    "PATH": f"{commands}:{os.environ['PATH']}",
                    "ROOTLESS": str(rootless).lower(),
                    "COMMAND_LOG": str(log),
                    "WORK_DIR": str(work / "workflow"),
                    "SCRIPT_DIR": str(work),
                    "OPENAI_API_KEY": "offline-test-token",
                },
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            credential = work / "workflow/credentials/openai-api-key"
            self.assertEqual(credential.stat().st_mode & 0o777, 0o400)
            self.assertEqual(credential.read_text(), "offline-test-token")
            self.assertEqual(
                (work / "workflow/index/data").stat().st_mode & 0o444, 0o444
            )
            self.assertIn(f"chown 1001:0 {credential}", log.read_text())
            self.assertNotIn("offline-test-token", result.stdout + result.stderr)

    def test_rootful_permissions_fall_back_to_host_commands(self) -> None:
        """Do not abort when rootful Podman rejects unshare."""
        self.check_permissions(rootless=False)

    def test_rootless_permissions_use_podman_namespace(self) -> None:
        """Keep namespace-relative ownership and permissions for rootless Podman."""
        self.check_permissions(rootless=True)


class WorkflowNetworkTests(unittest.TestCase):
    """Keep nested Podman networking aligned with the working VM reference."""

    def test_inner_runs_use_host_network(self) -> None:
        """Avoid netavark bridge setup inside the privileged infrastructure runner."""
        commands = [
            shlex.split(line)
            for line in WORKFLOW.read_text().replace("\\\n", "").splitlines()
            if line.startswith("podman run ")
        ]
        self.assertEqual(len(commands), 2)
        for command in commands:
            with self.subTest(command=command):
                self.assertIn("--network=host", command)


if __name__ == "__main__":
    unittest.main()
