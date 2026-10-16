"""Verify targeted dependency freezes without running the resolver container."""

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/konflux_resolve.py"


def load_module():
    """Import the resolver as a standalone module."""
    spec = importlib.util.spec_from_file_location("konflux_resolve", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FreezeTestCase(unittest.TestCase):
    """Run tests from a temporary directory with the resolver loaded."""

    def setUp(self) -> None:
        """Load the resolver and change into a temporary directory."""
        self.module = load_module()
        self.addCleanup(os.chdir, os.getcwd())
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        os.chdir(temporary.name)


class CollectCommittedPinsTests(FreezeTestCase):
    """Extract name==version pins from committed requirement files."""

    def test_reads_pins_across_hash_files(self) -> None:
        """Combine wheel and source pins while skipping the bumped package."""
        Path("requirements.hashes.wheel.txt").write_text(
            "--index-url https://rhoai.example/simple/\n"
            "torch==2.11.0 \\\n"
            "    --hash=sha256:aaaaaaaa\n"
            "urllib3==2.7.0 \\\n"
            "    --hash=sha256:bbbbbbbb\n",
            encoding="utf-8",
        )
        Path("requirements.hashes.source.txt").write_text(
            "--index-url https://pypi.org/simple\n"
            "banks==2.5.1 \\\n"
            "    --hash=sha256:cccccccc\n",
            encoding="utf-8",
        )

        pins = self.module.collect_committed_pins(
            [
                "requirements.hashes.wheel.txt",
                "requirements.hashes.source.txt",
                "requirements.hashes.wheel.pypi.txt",
            ],
            "urllib3",
        )

        self.assertEqual(pins, {"torch": "2.11.0", "banks": "2.5.1"})

    def test_skips_missing_files(self) -> None:
        """Treat absent files as empty instead of failing."""
        pins = self.module.collect_committed_pins(["missing.txt"], "urllib3")
        self.assertEqual(pins, {})


class RestoreBuildDepPinsTests(FreezeTestCase):
    """Rewrite freshly compiled build pins back to committed versions."""

    def test_reverts_old_pins_and_keeps_new_packages(self) -> None:
        """Restore committed versions while preserving annotations and additions."""
        Path("requirements-build.txt").write_text(
            "# committed pins\n"
            "pluggy==1.6.0\n"
            "    # via hatchling\n"
            "tomlkit==0.15.1\n"
            "    # via hatchling\n",
            encoding="utf-8",
        )
        pins = self.module.collect_committed_pins(["requirements-build.txt"], "urllib3")
        Path("requirements-build.txt").write_text(
            "# freshly compiled pins\n"
            "hatch-vcs==0.5.0\n"
            "    # via urllib3\n"
            "pluggy==1.7.0\n"
            "    # via hatchling\n"
            "tomlkit==0.15.2\n"
            "    # via hatchling\n",
            encoding="utf-8",
        )

        restored = self.module.restore_build_dep_pins("requirements-build.txt", pins)

        content = Path("requirements-build.txt").read_text(encoding="utf-8")
        self.assertEqual(restored, 2)
        self.assertIn("hatch-vcs==0.5.0\n    # via urllib3\n", content)
        self.assertIn("pluggy==1.6.0\n    # via hatchling\n", content)
        self.assertIn("tomlkit==0.15.1\n    # via hatchling\n", content)


class UvResolveFreezeTests(FreezeTestCase):
    """Pass a constraints wall to the containerized uv compile."""

    def test_freeze_writes_constraints_and_cleans_up(self) -> None:
        """Freeze committed pins except the dependency being bumped."""
        Path("requirements.hashes.wheel.txt").write_text(
            "--index-url https://rhoai.example/simple/\n"
            "torch==2.11.0 \\\n"
            "    --hash=sha256:aaaaaaaa\n"
            "urllib3==2.7.0 \\\n"
            "    --hash=sha256:bbbbbbbb\n",
            encoding="utf-8",
        )
        Path("requirements.hashes.source.txt").write_text(
            "banks==2.5.1 \\\n" "    --hash=sha256:cccccccc\n",
            encoding="utf-8",
        )
        captured: dict[str, str] = {}

        def fake_run(cmd, **_kwargs):
            """Read the constraints during the mocked compile."""
            path = cmd[cmd.index("--constraints") + 1]
            captured["constraints"] = Path(path).read_text(encoding="utf-8")
            return mock.Mock(stdout="")

        with (
            mock.patch.object(self.module, "_container_runtime", return_value="podman"),
            mock.patch.object(self.module.subprocess, "run", side_effect=fake_run),
        ):
            resolved = self.module.uv_resolve(
                "3.12", "https://rhoai.example/simple/", "", freeze_except="urllib3"
            )

        self.assertEqual(resolved, {})
        self.assertEqual(captured["constraints"], "banks==2.5.1\ntorch==2.11.0\n")
        self.assertFalse(Path("_tmp_freeze_constraints.txt").exists())

    def test_without_freeze_omits_constraints(self) -> None:
        """Omit the constraints file for a full dependency refresh."""
        with (
            mock.patch.object(self.module, "_container_runtime", return_value="podman"),
            mock.patch.object(
                self.module.subprocess, "run", return_value=mock.Mock(stdout="")
            ) as run,
        ):
            self.module.uv_resolve("3.12", "https://rhoai.example/simple/", "")

        cmd = run.call_args[0][0]
        self.assertNotIn("--constraints", cmd)


if __name__ == "__main__":
    unittest.main()
