"""Validate an OLS answer against facts exclusive to the fictional BYOK corpus."""

import json
import sys
from pathlib import Path

EXPECTED_FACT = "ORBITAL-MANGO-731"
EXPECTED_TITLE = "Zyranex T7 OpenShift Runbook"
EXPECTED_URL = "https://docs.quorbitex.example.com/openshift/zyranex-t7"


def validate_response(response: dict) -> None:
    """Require the answer-only recovery phrase and the matching source citation."""
    answer = response.get("response")
    if not isinstance(answer, str) or EXPECTED_FACT.casefold() not in answer.casefold():
        raise ValueError("Answer is missing the answer-only fictional recovery phrase")
    documents = response.get("referenced_documents")
    if not isinstance(documents, list) or not any(
        isinstance(document, dict)
        and document.get("doc_title") == EXPECTED_TITLE
        and document.get("doc_url") == EXPECTED_URL
        for document in documents
    ):
        raise ValueError("Answer is missing the expected BYOK title/URL citation")


if __name__ == "__main__":
    try:
        payload = json.loads(Path(sys.argv[1]).read_text())
        if not isinstance(payload, dict):
            raise ValueError("Expected an OLS response object")
        validate_response(payload)
    except (ValueError, OSError, IndexError) as error:
        sys.exit(f"BYOK validation failed: {error}")
    print("BYOK answer and citation validated")
