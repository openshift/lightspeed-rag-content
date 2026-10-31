"""Regression tests for the BYOK unused-dependency audit exclusion patterns.

Deptry anchors its default exclusion patterns at the start of the
repository-relative path, so ``venv`` and ``setup.py`` defaults never match
under the ``byok/`` scan prefix used by ``make check-unused-deps``. The
``extend_exclude`` patterns in ``pyproject.toml`` must keep imports inside
``byok/venv/`` and ``byok/setup.py`` from masking an unused dependency.
"""

import shutil
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

try:
    import tomlkit

    HAS_TOMLKIT = True
except ImportError:  # pragma: no cover - tomlkit ships with the test env
    HAS_TOMLKIT = False

DEPTRY_COMMAND = ["uvx", "deptry==0.24.0"]


class CheckUnusedDepsExclusionTests(unittest.TestCase):
    """Reproduce the audit against disposable repositories."""

    @classmethod
    def setUpClass(cls) -> None:
        """Build the disposable repository template once for all tests."""
        cls.repo = None

    def setUp(self) -> None:
        """Skip when the pinned tooling is unavailable."""
        if not shutil.which("uv"):
            self.skipTest("uv is not installed")
        if not HAS_TOMLKIT:
            self.skipTest("tomlkit is not installed")

    def make_repo(self, *masked_paths: str, dependency: str = "requests") -> Path:
        """Create a repository whose only dependency import is masked."""
        config = tomllib.loads((ROOT / "pyproject.toml").read_text())
        deptry_config = config["tool"]["deptry"]
        pyproject = tomlkit.document()
        project = tomlkit.table()
        project["name"] = "audit-probe"
        project["version"] = "0.0.0"
        project["dependencies"] = [dependency]
        pyproject["project"] = project
        pyproject["tool"] = {"deptry": deptry_config}

        repo = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, repo, ignore_errors=True)
        (repo / "pyproject.toml").write_text(tomlkit.dumps(pyproject))
        (repo / "byok").mkdir()
        (repo / "byok/tool.py").write_text("# production code without imports\n")
        for masked in masked_paths:
            path = repo / masked
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("import requests\n")
        return repo

    def run_deptry(self, repo: Path) -> subprocess.CompletedProcess:
        """Run the pinned deptry command exactly as the Makefile does."""
        return subprocess.run(
            [*DEPTRY_COMMAND, "byok"],
            cwd=repo,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_import_in_byok_venv_does_not_mask_unused_dep(self) -> None:
        """Report DEP002 when the only import lives in byok/venv/."""
        repo = self.make_repo("byok/venv/probe.py")
        result = self.run_deptry(repo)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DEP002", result.stdout + result.stderr)

    def test_import_in_byok_setup_py_does_not_mask_unused_dep(self) -> None:
        """Report DEP002 when the only import lives in byok/setup.py."""
        repo = self.make_repo("byok/setup.py")
        result = self.run_deptry(repo)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DEP002", result.stdout + result.stderr)

    def test_stdlib_backport_dependency_does_not_report_dep005(self) -> None:
        """Keep the audit DEP002-only; DEP005 stays disabled (see README)."""
        repo = self.make_repo(dependency="typing")
        (repo / "byok/tool.py").write_text("import typing\n")
        result = self.run_deptry(repo)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_used_dependency_still_passes(self) -> None:
        """Keep the audit green when the dependency is genuinely used."""
        repo = self.make_repo()
        (repo / "byok/tool.py").write_text("import requests\n")
        result = self.run_deptry(repo)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
