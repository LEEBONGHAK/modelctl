# modelctl

[English](README.md) | [한국어](README.ko.md)

**The universal AI model and coding-agent control plane.**

`modelctl` provides one CLI for selecting AI providers and models, managing local credentials and defaults, diagnosing the environment, and launching coding-agent CLIs consistently.

> Current completed development version: `0.1.0`. Version `0.2.0` is now in draft development on `refac`; `main` remains the canonical release branch.

## What works today

- OpenRouter credential storage and model synchronization
- Interactive and non-interactive provider/model selection
- Persistent provider, model, and launcher defaults
- Claude Code, Gemini CLI, Codex CLI, and Aider launchers
- Native argument forwarding without shell execution
- Launcher discovery, installation status, and selection
- Provider-aware launcher recommendations with an explicit safe apply step
- `modelctl doctor` diagnostics and compatibility feedback
- Operating-system keyring storage with explicit plaintext fallback
- Linux, macOS, and Windows tests on Python 3.13
- Locked dependency audit, Ruff, package builds, and installed-wheel smoke tests
- Validated GitHub Release artifacts with SHA-256 checksums

See [`docs/PROGRESS.md`](docs/PROGRESS.md) for project status and [`docs/pull-requests/README.md`](docs/pull-requests/README.md) for bilingual PR history.

## Installation from the repository

The repository is a Python 3.13+ uv workspace. Use `main` for the completed release state:

```bash
git clone https://github.com/LEEBONGHAK/modelctl.git
cd modelctl
git switch main
uv sync --all-packages --locked
uv run modelctl --help
```

Contributors developing the next version should branch from `refac`.

## Quick start

### 1. Store an OpenRouter credential

```bash
modelctl auth login openrouter
```

The operating-system keyring is the default. `modelctl` does not silently downgrade to plaintext storage. Explicitly accept the local-file risk only when a keyring is unavailable:

```bash
modelctl auth login openrouter --allow-plaintext-fallback
```

The fallback file is private to the current user on POSIX systems but remains unencrypted plaintext. An environment variable such as `MODELCTL_OPENROUTER` is also supported.

### 2. Synchronize and select a model

```bash
modelctl models sync openrouter
modelctl use
```

For scripts and CI:

```bash
modelctl use \
  --provider openrouter \
  --model anthropic/claude-sonnet-4
```

Direct selections are validated against the provider registry and synchronized local catalog.

### 3. Select a launcher

```bash
modelctl launchers list
modelctl launchers recommend
modelctl launchers recommend --apply
modelctl launchers use aider
```

`recommend` uses the selected provider and model to propose the safest supported launcher. It does not change configuration unless `--apply` is supplied, and apply refuses a launcher that is unavailable on `PATH`.

| ID | Coding agent | Native provider | Base command |
| --- | --- | --- | --- |
| `claude` | Claude Code | Anthropic | `claude --model <model>` |
| `gemini` | Gemini CLI | Google | `gemini --model <model>` |
| `codex` | Codex CLI | OpenAI | `codex --model <model>` |
| `aider` | Aider | Multiple providers | `aider --model <model>` |

### 4. Diagnose and run

```bash
modelctl doctor
modelctl run
```

Arguments after `run` are forwarded as an argument list:

```bash
modelctl run --continue
modelctl run --sandbox workspace-write
modelctl run --no-auto-commits
```

## OpenRouter compatibility

Claude Code, Gemini CLI, and Codex CLI are native clients for their own providers. `modelctl` warns, without blocking, when another provider's model is passed to one of them.

Aider is the current automatic OpenRouter integration:

```bash
modelctl launchers use aider
modelctl config set provider openrouter
modelctl config set model anthropic/claude-sonnet-4
modelctl run
```

Result:

```bash
aider --model openrouter/anthropic/claude-sonnet-4
```

## Configuration and local data

```bash
modelctl config show
modelctl config set provider openrouter
modelctl config set model anthropic/claude-sonnet-4
modelctl config set launcher aider
```

Default paths:

```text
~/.config/modelctl/config.json
~/.config/modelctl/credentials.json   # explicit fallback only
~/.local/share/modelctl/modelctl.db
```

Protected local writes are atomic. POSIX directories and files are hardened to `0700` and `0600`, and symbolic-link paths are rejected.

## Development and security checks

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
```

GitHub Actions additionally runs the complete pytest suite on Ubuntu, macOS, and Windows, builds all distributions, installs the wheels in an isolated environment, and verifies the installed CLI.

## Release readiness

Release decisions are declared in [`release.toml`](release.toml), notable changes in [`CHANGELOG.md`](CHANGELOG.md), and the full completion checklist in [`docs/RELEASE_CRITERIA.md`](docs/RELEASE_CRITERIA.md).

```bash
python scripts/release_validation.py
python scripts/release_validation.py --print-status
python scripts/release_validation.py --tag v0.2.0
```

The current `0.2.0` manifest is `draft`, so it cannot publish a release. Once it is explicitly marked `ready`, a trusted `main` push or a reviewed pull request merged into `main` must independently pass:

- coordinated package, manifest, changelog, and documentation validation
- locked dependency audit
- Ruff and the complete pytest suite
- distribution builds and installed-wheel smoke tests
- checksum generation

Only then does the workflow create `v<version>` at that exact `main` commit and publish one immutable GitHub Release. Existing tags and release assets are never overwritten.

**PyPI publication is intentionally disabled.** No workflow publishes packages to PyPI. See [`docs/RELEASING.md`](docs/RELEASING.md).

## Project structure

```text
apps/modelctl/       Typer CLI application
packages/core/       runtime services, credentials, providers, repositories, launchers
packages/sdk/        SDK foundation
scripts/             release validation helpers
tests/               regression, integration, packaging, and security tests
docs/                project, release, security, and PR documentation
```

## Security

See [`SECURITY.md`](SECURITY.md) for credential behavior, reporting guidance, supported versions, and known limitations. Automated checks reduce known risk but do not replace an independent penetration test or formal audit.

## Near-term roadmap

- Expand provider-aware recommendations into stricter compatibility policies and automatic remediation
- Launcher capability and execution-request refactoring
- Profile management only after a complete workflow and tests exist
- A separately reviewed PyPI publication milestone
