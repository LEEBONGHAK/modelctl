# Publishing v0.1.0 to PyPI

This repository publishes the coordinated `modelctl`, `modelctl-core`, and
`modelctl-sdk` distributions from the immutable `v0.1.0` tag.

## One-time PyPI setup

1. Sign in to PyPI and create an account-wide API token. An account-wide token
   is required for the first upload because the three projects may not exist on
   PyPI yet. After the projects exist, replace it with project-scoped tokens or
   migrate the workflow to Trusted Publishing.
2. In the GitHub repository, create an environment named `pypi`.
3. Add an environment secret named `PYPI_API_TOKEN` containing the complete
   token value, including the `pypi-` prefix.
4. Configure required reviewers on the `pypi` environment so publication needs
   an explicit approval.

## Publish v0.1.0

1. Merge the reviewed PyPI workflow into `main`.
2. Open **Actions → Publish to PyPI → Run workflow**.
3. Keep `tag` set to `v0.1.0`.
4. Enter `publish-v0.1.0` as the confirmation value.
5. Approve the protected `pypi` environment when the validation job succeeds.

The workflow checks out the existing immutable tag, reruns release validation,
dependency audit, lint, the complete test suite, builds all six distributions,
checks their metadata, and only then uploads them to PyPI.

## Expected projects

- `modelctl==0.1.0`
- `modelctl-core==0.1.0`
- `modelctl-sdk==0.1.0`

## Verification

```bash
python -m venv .pypi-smoke
. .pypi-smoke/bin/activate
python -m pip install --upgrade pip
python -m pip install modelctl==0.1.0
modelctl version
modelctl --help
python -c "import modelctl_cli, modelctl_core, modelctl_sdk"
```

PyPI files are immutable. If a published file is wrong, do not attempt to
replace it; publish a new patch version instead.
