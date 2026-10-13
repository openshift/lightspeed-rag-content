"""Test the BYOK runtime contract and grounded-answer validation."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tests/integration-konflux/validate_response.py"


class RuntimeEnvironmentTests(unittest.TestCase):
    """Check that build commands use the customer's runtime interpreter."""

    def test_installation_and_validation_use_runtime_python(self) -> None:
        """Reject system-Python installation and validation."""
        containerfile = (ROOT / "byok/Containerfile.tool").read_text()
        self.assertNotIn("/usr/bin/python3.12", containerfile)
        self.assertIn("python3.12 -m pip install", containerfile)
        self.assertIn(
            'python3.12 -m pip install --no-cache-dir -e ".[cpu]"', containerfile
        )

    def test_local_install_has_project_readme(self) -> None:
        """Make the readme declared by pyproject available for editable installation."""
        containerfile = (ROOT / "byok/Containerfile.tool").read_text()
        metadata_copy = containerfile.split("RUN python3.12 -m pip install")[0]
        self.assertIn("README.md", metadata_copy)

    def test_nltk_cache_comes_from_installed_module(self) -> None:
        """Reject a hard-coded system site-packages directory."""
        containerfile = (ROOT / "byok/Containerfile.tool").read_text()
        self.assertNotIn("/usr/local/lib/python3.12/site-packages", containerfile)
        self.assertIn("llama_index.core.__file__", containerfile)


class GroundedAnswerTests(unittest.TestCase):
    """Reject answers that do not prove retrieval from the fictional corpus."""

    def validate(self, response: dict) -> subprocess.CompletedProcess:
        """Run the production response validator on a temporary API response."""
        self.assertTrue(VALIDATOR.is_file(), "Grounded-answer validator is missing")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "response.json"
            path.write_text(json.dumps(response))
            return subprocess.run(
                [sys.executable, str(VALIDATOR), str(path)],
                check=False,
                capture_output=True,
                text=True,
            )

    def test_answer_fact_with_matching_citation_passes(self) -> None:
        """Accept the answer-only recovery token with its source citation."""
        result = self.validate(
            {
                "response": "Use the recovery phrase ORBITAL-MANGO-731 to recover the relay.",
                "referenced_documents": [
                    {
                        "doc_title": "Zyranex T7 OpenShift Runbook",
                        "doc_url": "https://docs.quorbitex.example.com/openshift/zyranex-t7",
                    }
                ],
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_question_echo_fails(self) -> None:
        """Reject fictional names echoed from the question without the answer fact."""
        result = self.validate(
            {
                "response": "The Zyranex T7 on OpenShift reports ZRX-4401.",
                "referenced_documents": [],
            }
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("answer-only", result.stderr)

    def test_fact_only_in_citation_fails(self) -> None:
        """Require the recovery token in the answer, not elsewhere in the JSON."""
        result = self.validate(
            {
                "response": "I do not know the recovery phrase.",
                "referenced_documents": [{"doc_title": "ORBITAL-MANGO-731"}],
            }
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("answer-only", result.stderr)

    def test_answer_without_matching_citation_fails(self) -> None:
        """Require both title and URL on the same source document."""
        for documents in (
            [],
            [{"doc_title": "Zyranex T7 OpenShift Runbook", "doc_url": "wrong"}],
            [
                {
                    "doc_title": "wrong",
                    "doc_url": "https://docs.quorbitex.example.com/openshift/zyranex-t7",
                }
            ],
        ):
            with self.subTest(documents=documents):
                result = self.validate(
                    {
                        "response": "Use ORBITAL-MANGO-731.",
                        "referenced_documents": documents,
                    }
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("citation", result.stderr)

    def test_malformed_response_fails(self) -> None:
        """Reject an incomplete API response without a traceback."""
        result = self.validate({"response": None, "referenced_documents": None})
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
