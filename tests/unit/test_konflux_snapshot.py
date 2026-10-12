"""Test the actual Konflux snapshot extraction step without a cluster."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PIPELINE = ROOT / ".tekton/integration-tests/pipelines/byok-integration-test.yaml"
IMAGE = "quay.io/example/byok@sha256:" + "a" * 64
REVISION = "b" * 40


class SnapshotTests(unittest.TestCase):
    """Ensure CI tests the exact built image and source, never a fallback."""

    def extract(self, components: list) -> tuple[subprocess.CompletedProcess, dict]:
        """Execute the extraction script from the Pipeline with temporary results."""
        self.assertTrue(PIPELINE.is_file(), "Konflux integration pipeline is missing")
        pipeline = yaml.safe_load(PIPELINE.read_text())
        script = pipeline["spec"]["tasks"][0]["taskSpec"]["steps"][0]["script"]
        with tempfile.TemporaryDirectory() as directory:
            paths = {
                name: Path(directory) / name
                for name in ("tool-image", "revision", "repo-url")
            }
            for name, path in paths.items():
                script = script.replace(f"$(step.results.{name}.path)", str(path))
            result = subprocess.run(
                ["bash", "-c", script],
                env={**os.environ, "SNAPSHOT": json.dumps({"components": components})},
                capture_output=True,
                text=True,
                check=False,
            )
            return result, {
                name: path.read_text() for name, path in paths.items() if path.exists()
            }

    def component(self, image: str = IMAGE, revision: str = REVISION) -> dict:
        """Return a snapshot component with immutable image and source references."""
        return {
            "name": "lightspeed-rag-tool",
            "containerImage": image,
            "source": {
                "git": {
                    "revision": revision,
                    "url": "https://github.com/example/rag.git",
                }
            },
        }

    def test_exact_image_and_revision_are_selected(self) -> None:
        """Select the BYOK component even when other components are present."""
        result, outputs = self.extract([{"name": "other"}, self.component()])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(outputs["tool-image"], IMAGE)
        self.assertEqual(outputs["revision"], REVISION)
        self.assertEqual(outputs["repo-url"], "https://github.com/example/rag.git")

    def test_missing_component_fails(self) -> None:
        """Reject snapshots without the product under test."""
        result, _ = self.extract([])
        self.assertNotEqual(result.returncode, 0)

    def test_duplicate_components_fail(self) -> None:
        """Reject ambiguous snapshots instead of silently picking an image."""
        result, _ = self.extract([self.component(), self.component()])
        self.assertNotEqual(result.returncode, 0)

    def test_mutable_image_fails(self) -> None:
        """Reject latest or a tag instead of an immutable snapshot digest."""
        result, _ = self.extract([self.component(image="quay.io/example/byok:latest")])
        self.assertNotEqual(result.returncode, 0)

    def test_missing_revision_fails(self) -> None:
        """Reject a missing source revision rather than testing main."""
        result, _ = self.extract([self.component(revision="")])
        self.assertNotEqual(result.returncode, 0)


class ConsumerImageTests(unittest.TestCase):
    """Use a digest-pinned released OLS consumer rather than a transient dev image."""

    def test_scenario_selects_released_service_image(self) -> None:
        """Keep the OLS consumer pin in the released Red Hat repository."""
        path = ROOT / ".tekton/integration-tests/byok-integration-test-scenario.yaml"
        scenario = yaml.safe_load(path.read_text())
        parameters = {
            param["name"]: param["value"] for param in scenario["spec"]["params"]
        }
        self.assertRegex(
            parameters["ols-service-image"],
            r"^registry\.redhat\.io/openshift-lightspeed/"
            r"lightspeed-service-api-rhel9@sha256:[a-f0-9]{64}$",
        )


class OpenAICredentialTests(unittest.TestCase):
    """Use the existing OLS tenant Secret and token key."""

    def test_pipeline_defaults_to_shared_openai_secret(self) -> None:
        """Reuse the tenant's openai Secret unless explicitly overridden."""
        pipeline = yaml.safe_load(PIPELINE.read_text())
        parameters = {param["name"]: param for param in pipeline["spec"]["params"]}
        self.assertEqual(parameters["openai-secret"]["default"], "openai")

    def test_scenario_selects_shared_openai_secret(self) -> None:
        """Register the test using the same Secret as existing OLS integration tests."""
        path = ROOT / ".tekton/integration-tests/byok-integration-test-scenario.yaml"
        scenario = yaml.safe_load(path.read_text())
        parameters = {
            param["name"]: param["value"] for param in scenario["spec"]["params"]
        }
        self.assertEqual(parameters["openai-secret"], "openai")

    def test_vm_runner_reads_token_key(self) -> None:
        """Read the mounted token key rather than require a new Secret schema."""
        path = ROOT / ".tekton/integration-tests/scripts/run-in-vm.sh"
        runner = path.read_text()
        self.assertIn("[[ -r /var/run/openai/token ]]", runner)
        self.assertIn(
            'cp /var/run/openai/token "$LOCAL_WORK/credentials/openai-api-key"', runner
        )
        self.assertNotIn("/var/run/openai/openai-api-key", runner)


class BootstrapFailureTests(unittest.TestCase):
    """Require a standardized failure result even before the VM runner starts."""

    def bootstrap(self, runner: str | None) -> tuple[subprocess.CompletedProcess, dict]:
        """Run the actual bootstrap with offline package/checkout stand-ins."""
        pipeline = yaml.safe_load(PIPELINE.read_text())
        script = pipeline["spec"]["tasks"][1]["taskSpec"]["steps"][0]["script"]
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            commands = work / "bin"
            commands.mkdir()
            for name in ("dnf", "git"):
                command = commands / name
                command.write_text("#!/bin/sh\nexit 0\n")
                command.chmod(0o700)
            if runner is not None:
                path = work / "repo/.tekton/integration-tests/scripts/run-in-vm.sh"
                path.parent.mkdir(parents=True)
                path.write_text(runner)
            result_path = work / "result.json"
            result = subprocess.run(
                ["bash", "-c", script],
                cwd=work,
                env={
                    **os.environ,
                    "PATH": f"{commands}:{os.environ['PATH']}",
                    "REPO_URL": "https://github.com/example/rag.git",
                    "REPO_REV": REVISION,
                    "RESULTS_TEST_OUTPUT_PATH": str(result_path),
                },
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertTrue(result_path.is_file(), "Bootstrap omitted TEST_OUTPUT")
            return result, json.loads(result_path.read_text())

    def test_missing_runner_reports_failure(self) -> None:
        """Report failure when the checked-out source has no runnable test payload."""
        result, output = self.bootstrap(None)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output["result"], "FAILURE")

    def test_runner_initialization_failure_reports_failure(self) -> None:
        """Preserve failure before the runner can install its own trap."""
        result, output = self.bootstrap("exit 42\n")
        self.assertEqual(result.returncode, 42)
        self.assertEqual(output["result"], "FAILURE")


if __name__ == "__main__":
    unittest.main()
