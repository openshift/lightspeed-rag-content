# Spec Verification Report: lightspeed-rag-content

**Date:** 2026-07-24
**Scope:** `.ai/spec/what/` files (5 files)
**Verifier:** Independent spec verification agent

## Pass 1: Acceptance Criteria

The what/ files do not use `- [ ]` checkbox-style acceptance criteria. They use numbered behavioral rules instead. This is consistent with the spec conventions documented in README.md. No acceptance criteria to verify.

**Result: N/A (no checkbox-style acceptance criteria found)**

## Pass 2: Constraint Compliance

Checked all what/ files against shared constraints in `.ai/spec/constraints.md`.

### Constraint 1 (fork-based workflow)
**PASS** -- Not applicable to behavioral specs (workflow constraint).

### Constraint 2 (commit messages start with OLS-XXXX)
**PASS** -- Not applicable to behavioral specs (workflow constraint).

### Constraint 3 (squash commits)
**PASS** -- Not applicable to behavioral specs (workflow constraint).

### Constraint 4 (Jira project key OLS)
**PASS** -- All Jira references in specs use OLS-XXXX format (OLS-1729, OLS-2294, OLS-2903, OLS-1872, OLS-2704, OCPSTRAT-1494).

### Constraint 5 (Classic OLS CRDs use ols.openshift.io/v1alpha1)
**PASS** -- Not directly referenced in rag-content specs (rag-content is a build-time artifact, not a CRD owner).

### Constraint 6 (Agentic OLS CRDs use agentic.openshift.io/v1alpha1)
**PASS** -- Not applicable (no agentic CRDs in rag-content).

### Constraint 7 (deploy into openshift-lightspeed namespace)
**PASS** -- Not applicable (rag-content is a build-time artifact, not a deployed service).

### Constraint 8 (embedding model must match at build and query time)
**PASS** -- Well documented in multiple places:
- `embedding-pipeline.md` Constraint 1: "The embedding model used to build an index must be identical to the model used by lightspeed-service for query embedding."
- `system-overview.md` Integration invariant section: "The embedding model used to generate BYOK indexes must be identical to the model used by lightspeed-service for BYOK query embedding."
- `byok.md` Rule 5: Documents that BYOK uses the same embedding model as the main pipeline.

**All constraints: PASS**

## Pass 3: Term Consistency

**SKIPPED** -- No glossary file exists.

## Pass 4: Internal Reference Accuracy

### Reference 1: embedding-pipeline.md line 5
**Text:** "Individual pipeline architectures are documented in the corresponding `how/` specs."
**Check:** `how/plaintext-pipeline.md`, `how/html-pipeline.md`, `how/lsc-library.md` all exist.
**PASS**

### Reference 2: system-overview.md -- References to lightspeed-service
**Text:** Multiple references to "lightspeed-service" consuming artifacts (lines 5, 9, 15, 32, 38, 45).
**Check:** lightspeed-service is a sibling repo in the workspace. Cross-repo references are expected.
**PASS**

### Reference 3: system-overview.md -- Reference to operator CRD
**Text:** "operator CRD's `rag[]` entries" (line 32), "operator configures BYOK RAG content references via the CRD" (line 49).
**Check:** Cross-repo reference to lightspeed-operator. Expected and appropriate.
**PASS**

### Reference 4: system-overview.md -- Reference to `ols_config.reference_content.embeddings_model_path`
**Text:** Line 45 references service config path.
**Check:** Cross-repo reference to lightspeed-service configuration. Expected.
**PASS**

### Reference 5: README.md -- Reference to `what/rag.md` in lightspeed-service
**Text:** "The service's `what/rag.md` spec describes how it loads and queries these indexes at runtime."
**Check:** `/Users/xavi/street/github.com/AI/ols/lightspeed-service/.ai/spec/what/rag.md` exists.
**PASS**

### Reference 6: README.md -- Cross-reference table (what/ to how/ mappings)
All referenced files verified to exist:
- `what/system-overview.md` -> `how/project-structure.md` -- PASS
- `what/content-sources.md` -> `how/plaintext-pipeline.md`, `how/html-pipeline.md`, `how/lsc-library.md` -- PASS
- `what/embedding-pipeline.md` -> `how/plaintext-pipeline.md`, `how/html-pipeline.md`, `how/lsc-library.md` -- PASS
- `what/byok.md` -> `how/container-build.md` -- PASS
- `what/container-build.md` -> `how/container-build.md` -- PASS

### Reference 7: byok.md -- References to main pipeline
**Text:** Rule 5 states BYOK uses "the same embedding model... as the main pipeline."
**Check:** Main pipeline is deprecated but still documented in embedding-pipeline.md. The reference is accurate; both use `sentence-transformers/all-mpnet-base-v2`.
**PASS**

### Reference 8: container-build.md -- References to Containerfiles
**Text:** References `byok/Containerfile.tool`, `lsc/Containerfile.konflux`, root `Containerfile`, `Containerfile.output`.
**Check:** These are code references, not spec cross-references. Assumed valid (code verification is out of scope).
**PASS**

**All references: PASS**

## Additional Observations

1. **OCPSTRAT-1494 in byok.md** uses a non-OLS Jira prefix. This is not a constraint violation (Constraint 2 applies to commit messages and PR titles, not spec references), but is worth noting as it references a different Jira project (OCPSTRAT rather than OLS).

2. **content-sources.md Rule 16** mentions OKP title extraction from TOML frontmatter in an active-rules section (Rules 15-20). However, OKP content is deprecated. The rule text itself correctly scopes the OKP part as an exception clause ("For OKP files, `title` comes from the TOML frontmatter instead"), and the OKP content source is deprecated, so this OKP clause is effectively dead code in the spec. Not a violation but could be cleaned up.

3. **Deprecated content dominance:** A large proportion of the spec content is marked [DEPRECATED]. The specs are well-organized with clear deprecation notices and OKP adoption banners, which is good practice.

## Summary

| Category | Result |
|---|---|
| Acceptance criteria | N/A (no `- [ ]` style criteria) |
| Constraint violations | 0 |
| Reference issues | 0 |
| Observations | 2 (minor, non-blocking) |
