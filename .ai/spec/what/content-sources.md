# Content Sources

This spec defines the rules for acquiring, processing, and organizing input content before it enters the embedding pipeline.

## Behavioral Rules -- OCP Product Documentation

1. The source is the `openshift/openshift-docs` GitHub repository. Each OCP version is cloned from its corresponding `enterprise-{version}` branch (e.g., `enterprise-4.18`).

2. AsciiDoc source files are converted to plaintext using the `asciidoctor` CLI with a custom Ruby text converter extension. Per-version attribute files provide version-specific AsciiDoc substitution values.

3. The topic map file (`_topic_maps/_topic_map.yml`) with the distro filter `openshift-enterprise` determines which AsciiDoc files to convert. Only files referenced in the topic map for the `openshift-enterprise` distribution are included.

4. Converted plaintext files are stored in `ocp-product-docs-plaintext/{version}/` with the directory hierarchy from the source repository preserved.

5. Files listed in the exclusion configuration must be removed after conversion. The exclusion list is a newline-delimited file of relative paths within the version directory.

6. All currently supported OCP versions must have a corresponding directory. Each directory name is a version string (e.g., `4.16`, `4.17`, `4.18`, `4.19`, `4.20`, `4.21`, `4.22`).

7. The plaintext docs and runbooks are committed to the repository and kept up to date. Content acquisition scripts exist for refreshing them, but the committed content is what the production build uses.

## Behavioral Rules -- Runbooks

8. The source is the `openshift/runbooks` GitHub repository, `master` branch, restricted to the `alerts/` directory only.

9. Acquisition uses sparse checkout with blob filtering (`--filter=blob:none`) to avoid cloning the full repository history.

10. Only Markdown (`.md`) files are retained. `README.md` files, empty directories, and `deprecated/` directories are removed after checkout.

11. Runbooks are stored in `runbooks/alerts/` with operator-specific subdirectories preserved (e.g., `runbooks/alerts/cluster-etcd-operator/`).

## Behavioral Rules -- OKP (Errata) Content

12. OKP files are Markdown documents with TOML frontmatter delimited by `+++` markers.

13. OKP files are filtered by project name via case-insensitive substring matching against the `portal_product_names` list in the TOML metadata's `extra` section. A project name like "OpenStack" matches any product name containing that substring (e.g., "Red Hat OpenStack Platform").

14. OKP files must have both a non-empty `reference_url` in `extra` and a non-empty `title` in the TOML metadata to be included. Files missing either field are skipped with a warning.

## Behavioral Rules -- Document Metadata

15. Every document processed for embedding must carry at minimum two metadata fields: `docs_url` (source URL) and `title` (document title). The lsc library additionally includes `url_reachable` (boolean indicating URL validity) to support the `unreachable_action` filtering rules below. The plaintext pipeline does not include `url_reachable` in metadata.

16. `title` is extracted from the first line of the document file, stripping any leading `# ` Markdown heading prefix. For OKP files, `title` comes from the TOML frontmatter instead.

17. `docs_url` is derived from the file path using content-type-specific URL construction rules:
    - **OCP docs**: `https://docs.openshift.com/container-platform/{version}/{relative_path}.html` -- the `.txt` extension is replaced with `.html`, and the embeddings root directory prefix is stripped.
    - **Runbooks**: `https://github.com/openshift/runbooks/blob/master/alerts/{relative_path}` -- the runbooks root directory prefix is stripped.
    - **BYOK content**: Defaults to the file path. If YAML frontmatter with a `url` field is present, that URL is used instead.
    - **OKP content**: The `reference_url` from the TOML frontmatter `extra` section.

18. URL reachability is validated via HTTP GET with retries. The lsc library's `MetadataProcessor` uses configurable retries (default 3) with a 30-second timeout. The plaintext pipeline's `ping_url` uses a single attempt with a 30-second timeout. Validation is skipped during hermetic builds in both pipelines.

19. In the lsc library, unreachable URLs can be handled three ways, controlled by the `unreachable_action` parameter:
    - `warn` -- log a warning and include the document in the index (default).
    - `fail` -- raise an error and abort.
    - `drop` -- exclude the document from the index.
    The plaintext pipeline always uses the `warn` behavior -- it logs unreachable URLs and counts them but never drops or fails.

20. In the lsc library, an ignore list allows specific document titles to bypass URL validation. Documents with titles in the ignore list are included in the index regardless of their `url_reachable` status.

## Configuration Surface

- `config/exclude.conf` -- newline-delimited list of relative file paths to exclude from OCP docs after conversion.
- `ocp-product-docs-plaintext/{version}/` directories -- each directory name is an OCP version string. Adding or removing directories changes which versions are indexed.
- `scripts/asciidoctor-text/{version}/attributes.yaml` (and `lsc/scripts/asciidoctor-text/{version}/attributes.yaml`) -- per-version AsciiDoc attribute files providing version-specific substitution values.
- `--hermetic-build` / `-hb` CLI flag -- disables URL reachability validation.
- `--folder` / `-f` CLI flag -- specifies the input document directory.
- `--runbooks` / `-r` CLI flag -- specifies the runbooks directory.

## Constraints

1. AsciiDoc conversion requires `asciidoctor` and `ruby` to be installed on the system. These are not Python dependencies and must be available in the build environment.

2. Content acquisition scripts require network access to clone from GitHub. The production container build uses pre-committed content and does not run these scripts -- they are developer/maintenance tools.

3. The OCP documentation repository is large. Single-branch cloning (`--single-branch`) is required to keep clone times manageable.

4. Runbook acquisition uses sparse checkout to avoid downloading irrelevant content from the runbooks repository.
