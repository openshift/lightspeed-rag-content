"""Exercise dependency bumps using isolated project files."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/bump_dep.py"


class BumpDependencyTests(unittest.TestCase):
    """Verify direct dependency and override constraint updates."""

    def write_project(self, directory: Path, dependencies: str) -> Path:
        """Write a minimal project table with the requested direct dependencies."""
        path = directory / "pyproject.toml"
        path.write_text(
            "[project]\n"
            'name = "sample-project"\n'
            'version = "0.1.0"\n'
            "dependencies = [\n"
            f"{dependencies}\n"
            "]\n",
            encoding="utf-8",
        )
        return path

    def bump(
        self, directory: Path, package: str, version: str
    ) -> subprocess.CompletedProcess:
        """Run the helper with the temporary project as its working directory."""
        return subprocess.run(
            [sys.executable, str(SCRIPT), package, version],
            cwd=directory,
            capture_output=True,
            check=False,
            text=True,
        )

    def test_bare_direct_dependency_uses_pep503_name_equivalence(self) -> None:
        """Turn a bare dependency into a lower bound without changing its spelling."""
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            path = self.write_project(
                directory, '    "Widget_Name", # keep this comment'
            )

            result = self.bump(directory, "widget.name", "2.0.0")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(
                '    "Widget_Name>=2.0.0", # keep this comment', path.read_text()
            )
            self.assertFalse((directory / "requirements.overrides.txt").exists())

    def test_compound_lower_and_upper_bounds_preserve_upper_bound(self) -> None:
        """Replace only the >= floor while keeping the existing < constraint."""
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            path = self.write_project(directory, '    "Http_Client>=1.0,<4",')

            result = self.bump(directory, "http.client", "2.5.0")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('    "Http_Client>=2.5.0,<4",', path.read_text())

    def test_incompatible_operators_become_requested_lower_bounds(self) -> None:
        """Replace operators other than >= instead of leaving them unchanged."""
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            path = self.write_project(
                directory,
                '    "Exact_Pin==1.0",\n    "Upper_Bound<4",',
            )

            exact = self.bump(directory, "exact.pin", "2.0.0")
            upper = self.bump(directory, "upper-bound", "3.0.0")

            self.assertEqual(exact.returncode, 0, exact.stderr)
            self.assertEqual(upper.returncode, 0, upper.stderr)
            self.assertIn('    "Exact_Pin>=2.0.0",', path.read_text())
            self.assertIn('    "Upper_Bound>=3.0.0",', path.read_text())

    def test_override_update_preserves_casing_and_comment(self) -> None:
        """Update a canonical-name match in overrides while retaining its comment."""
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.write_project(directory, '    "another-package",')
            overrides = directory / "requirements.overrides.txt"
            overrides.write_text(
                "# preserve this heading\nLegacy_Name==1.0 # preserve this note\n",
                encoding="utf-8",
            )

            result = self.bump(directory, "legacy.name", "2.0.0")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                overrides.read_text(),
                "# preserve this heading\nLegacy_Name>=2.0.0 # preserve this note\n",
            )

    def test_override_append_adds_a_missing_constraint(self) -> None:
        """Append a new override without discarding existing content."""
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.write_project(directory, '    "another-package",')
            overrides = directory / "requirements.overrides.txt"
            overrides.write_text("# keep\nexisting>=1.0", encoding="utf-8")

            result = self.bump(directory, "New_Package", "3.0.0")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                overrides.read_text(),
                "# keep\nexisting>=1.0\nNew_Package>=3.0.0\n",
            )

    def test_optional_dependency_is_bumped_in_pyproject(self) -> None:
        """Update optional dependencies instead of appending an unrelated override."""
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            path = directory / "pyproject.toml"
            path.write_text(
                "[project.optional-dependencies]\n"
                "cpu = [\n"
                '    "Optional_Package==1.0",\n'
                "]\n\n"
                "[project]\n"
                'name = "sample-project"\n'
                'version = "0.1.0"\n'
                "dependencies = []\n",
                encoding="utf-8",
            )

            result = self.bump(directory, "optional-package", "2.0.0")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(
                '    "Optional_Package>=2.0.0",',
                path.read_text(encoding="utf-8"),
            )
            self.assertFalse((directory / "requirements.overrides.txt").exists())

    def test_optional_direct_url_is_refused_without_modification(self) -> None:
        """Reject a direct URL in an optional group rather than adding an override."""
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            path = directory / "pyproject.toml"
            path.write_text(
                "[project.optional-dependencies]\n"
                "cpu = [\n"
                '    "Torch @ https://example.test/torch.whl",\n'
                "]\n\n"
                "[project]\n"
                'name = "sample-project"\n'
                'version = "0.1.0"\n'
                "dependencies = []\n",
                encoding="utf-8",
            )
            before = path.read_text(encoding="utf-8")

            result = self.bump(directory, "torch", "2.0.0")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("direct-URL", result.stderr)
            self.assertEqual(path.read_text(encoding="utf-8"), before)
            self.assertFalse((directory / "requirements.overrides.txt").exists())

    def test_direct_url_requirement_is_refused_without_modification(self) -> None:
        """Reject URL dependencies instead of replacing their source reference."""
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            path = self.write_project(
                directory,
                '    "Direct_Package @ https://example.test/direct.whl",',
            )
            before = path.read_text()

            result = self.bump(directory, "direct.package", "2.0.0")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("direct-URL", result.stderr)
            self.assertEqual(path.read_text(), before)
            self.assertFalse((directory / "requirements.overrides.txt").exists())


if __name__ == "__main__":
    unittest.main()
