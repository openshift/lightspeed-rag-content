# Unit coverage and Codecov (OLS-4830)

`unit-test-coverage-pull-request.yaml` and `unit-test-coverage-push.yaml` are
standalone Pipelines-as-Code PipelineRuns. They run independently of the image
build, for every PR targeting `main` and every push to `main`, respectively.
No image build or IntegrationTestScenario is required. They are not labeled as
build pipelines and do not produce application snapshots.

The public source repository is checked out at the event's exact revision,
using sparse checkout to avoid downloading the committed embedding model.
The existing `make test-coverage` target runs only `tests/unit`, with the same
lightweight dependencies as `make test-unit`. It does not install the embedding
stack, run cluster E2E tests, or enable opt-in container resolver tests.
`.coveragerc` covers Python source in `scripts` and `byok`, excluding test files,
and writes portable relative paths to `coverage.xml`. Coverage does not measure
shell scripts executed by the Python tests.

## Secret setup

Create a repository-specific Codecov upload token for
`openshift/lightspeed-rag-content`. In Konflux namespace
`crt-nshift-lightspeed-tenant`, create an Opaque secret:

- Name: **`ols-codecov-token-lightspeed-rag-content`**
- Key: **`CODECOV_TOKEN`**
- Value: the repository's Codecov upload token

The PipelineRuns use the existing `build-pipeline-lightspeed-rag-tool` service
account. The token is injected only into the upload step, not checkout or unit
tests. It is required: a missing secret/key prevents the upload step from
starting. Do not commit the token or reuse the lightspeed-service token.

As with any token-bearing PR pipeline, only run it for trusted/approved PRs.
Step-scoped injection is not a security boundary against malicious source:
the PR controls the uploader and shares files with the upload step. Retain
PaC's untrusted-contributor approval controls; review pipeline/uploader changes
before approving a run. No GitHub checkout credentials are needed for this
public repository.

## Upload policy and validation

`scripts/codecov.sh` follows lightspeed-service's pinned Codecov CLI (11.3.1),
bounded retry/timeout, and clearly logged soft-fail upload policy. A unit-test
failure blocks the pipeline; a Codecov service/upload failure does not.
`.codecov.yml` mirrors lightspeed-service's non-blocking status/comment policy.
The pipeline supplies the source SHA, PR source branch and number, or `main`
for baseline uploads, plus the explicit `openshift/lightspeed-rag-content` slug.
The legacy Prow-style environment variable names are the uploader's interface;
this does not run in Prow. `make test-coverage` never uploads locally.

After the first main push, confirm the baseline in Codecov. Then open a PR
and confirm an upload for its head SHA and a PR coverage delta/comment. Ensure
the Codecov GitHub integration is enabled for this repository. Local validation
cannot establish these acceptance criteria or prove tenant admission/network
policy permits the PipelineRuns; the first Konflux run must verify those.

Both manifests intentionally run on all changes to keep the PR check and main
baseline consistent. Their task specifications are identical; keep them in
sync when changing execution steps. The UBI Python image supplies Python 3.12,
Git, make, and pip. The test step installs uv and a SHA-256-verified static jq
1.8.1 binary (amd64/arm64) into `/workspace/tools/bin` without root. jq is
required by the unit tests that exercise shell snapshot/auth/cleanup handlers.
Code coverage and upload tooling are also installed separately from the
application's runtime dependencies.
