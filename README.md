# modelctl

[English](README.md) | [한국어](README.ko.md)

**The universal AI model and coding-agent control plane.**

`modelctl` provides one CLI for selecting AI providers and models, managing local credentials and defaults, diagnosing the environment, and launching coding-agent CLIs consistently.

> Current development version: `0.1.0`. The release manifest is marked ready and the validated `refac` release workflow creates the immutable tag and GitHub Release after all gates pass.

## What works today

- OpenRouter credential storage and model synchronization
- Interactive and non-interactive provider/model selection
- Persistent provider, model, and launcher defaults
- Claude Code, Gemini CLI, Codex CLI, and Aider launchers
- Native argument forwarding without shell execution
- Launcher discovery, installation status, and selection
- `modelctl doctor` diagnostics and compatibility feedback
- Operating-system keyring storage with explicit plaintext fallback
- Linux, macOS, and Windows tests on Python 3.13
- Locked dependency audit, Ruff, package builds, and installed-wheel smoke tests
- Validated GitHub Release artifacts with SHA-256 checksums

See [`docs/PROGRESS.md`](docs/PROGRESS.md) for project status and [`docs/pull-requests/README.md`](docs/pull-requests/README.md) for bilingual PR history.

## Development installation

The repository is a Python 3.13+ uv workspace.

```bash
git clone https://github.com/LEEBONGHAK/modelctl.git
cd modelctl
git switch refac
uv sync --all-packages --locked
uv run modelctl --help
```

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
modelctl launchers use aider
```

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
python scripts/release_validation.py --tag v0.1.0
```

A trusted `refac` push with `status = "ready"` must independently pass:

- coordinated package, manifest, changelog, and documentation validation
- locked dependency audit
- Ruff and the complete pytest suite
- distribution builds and installed-wheel smoke tests
- checksum generation

Only then does the workflow create `v<version>` at that exact commit and publish one immutable GitHub Release. Existing tags and release assets are never overwritten.

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

- Stricter compatibility policies and automatic remediation
- Launcher capability and execution-request refactoring
- Profile management only after a complete workflow and tests exist
- A separately reviewed PyPI publication milestone
