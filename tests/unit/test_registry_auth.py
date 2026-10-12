"""Test registry credential wiring and merging with synthetic auth entries."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PIPELINE = ROOT / ".tekton/integration-tests/pipelines/byok-integration-test.yaml"
RUNNER = ROOT / ".tekton/integration-tests/scripts/run-in-vm.sh"


class RegistrySecretTests(unittest.TestCase):
    """Reuse the existing tenant pull credentials rather than a new Secret."""

    def test_pipeline_mounts_existing_registry_secrets(self) -> None:
        """Mount Quay and Red Hat credentials read-only into the runner."""
        pipeline = yaml.safe_load(PIPELINE.read_text())
        task = pipeline["spec"]["tasks"][1]
        volumes = {volume["name"]: volume for volume in task["taskSpec"]["volumes"]}
        mounts = {
            mount["name"]: mount
            for mount in task["taskSpec"]["steps"][0]["volumeMounts"]
        }
        for name, secret in (
            ("quay-auth", "openshift-lightspeed"),
            ("redhat-auth", "registry-redhat-io"),
        ):
            with self.subTest(secret=secret):
                self.assertIn(name, volumes)
                self.assertEqual(volumes[name]["secret"]["secretName"], secret)
                self.assertEqual(mounts[name]["mountPath"], f"/var/run/{name}")
                self.assertTrue(mounts[name]["readOnly"])

    def test_registry_secret_parameter_is_removed(self) -> None:
        """Remove the obsolete parameter from every level of configuration."""
        scenario = (
            ROOT / ".tekton/integration-tests/byok-integration-test-scenario.yaml"
        )
        self.assertNotIn("registry-secret", PIPELINE.read_text())
        self.assertNotIn("registry-secret", scenario.read_text())

    def test_runner_merges_both_mounted_configs(self) -> None:
        """Build the transferred auth file from both existing Secret mounts."""
        runner = RUNNER.read_text()
        self.assertIn('merge_registry_auth "$LOCAL_WORK/credentials/auth.json"', runner)
        self.assertIn("/var/run/quay-auth/.dockerconfigjson", runner)
        self.assertIn("/var/run/redhat-auth/.dockerconfigjson", runner)
        self.assertNotIn("/var/run/registry-auth/", runner)


class RegistryAuthMergeTests(unittest.TestCase):
    """Exercise the actual runner's jq merge using disposable dummy credentials."""

    def merge(self, configs: list) -> tuple[subprocess.CompletedProcess, dict, int]:
        """Run the merge function and inspect its output and file permissions."""
        runner = RUNNER.read_text()
        marker = "merge_registry_auth() {"
        self.assertIn(marker, runner, "Registry auth merge function is missing")
        function = marker + runner.split(marker, 1)[1].split("\n}\n", 1)[0] + "\n}\n"
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            inputs = []
            for index, config in enumerate(configs):
                path = work / f"config-{index}.json"
                path.write_text(json.dumps(config))
                inputs.append(str(path))
            output = work / "auth.json"
            output.write_text("{}")
            output.chmod(0o644)
            script = "set -euo pipefail\n" + function + '\nmerge_registry_auth "$@"\n'
            result = subprocess.run(
                ["bash", "-c", script, "merge-test", str(output), *inputs],
                capture_output=True,
                text=True,
                check=False,
            )
            payload = json.loads(output.read_text()) if result.returncode == 0 else {}
            return result, payload, output.stat().st_mode & 0o777

    def test_merge_preserves_both_registries_privately(self) -> None:
        """Preserve all auth entries, restrict permissions, and omit output to logs."""
        configs = [
            {"auths": {"quay.io": {"auth": "dummy-quay"}}},
            {"auths": {"registry.redhat.io": {"auth": "dummy-redhat"}}},
        ]
        result, output, mode = self.merge(configs)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            output["auths"], {**configs[0]["auths"], **configs[1]["auths"]}
        )
        self.assertEqual(mode, 0o600)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("dummy-quay", result.stderr)
        self.assertNotIn("dummy-redhat", result.stderr)

    def test_missing_or_empty_auth_entries_fail(self) -> None:
        """Reject malformed credential configs instead of silently losing a registry."""
        for invalid in ({}, {"auths": {}}, {"auths": []}):
            with self.subTest(config=invalid):
                result, _, _ = self.merge(
                    [{"auths": {"quay.io": {"auth": "dummy-quay"}}}, invalid]
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("dummy-quay", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
