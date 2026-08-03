# modelctl

[English](README.md) | [한국어](README.ko.md)

**The universal AI model and coding-agent control plane.**

`modelctl` aims to become the **uv of AI coding agents**: one CLI for selecting AI providers and models, managing local configuration, and launching coding agents consistently.

> Development status: active, pre-release. The working implementation currently lives on the `refac` branch.

## What works today

- OpenRouter credential and model synchronization
- Interactive and non-interactive provider/model selection with `modelctl use`
- Persistent provider, model, and launcher configuration
- Claude Code, Gemini CLI, Codex CLI, and Aider launchers
- Native launcher argument forwarding without shell execution
- Launcher discovery, installation status, and selection
- Local environment diagnostics with `modelctl doctor`
- Non-blocking provider/model/launcher compatibility feedback
- Secure credential storage through the operating-system keyring
- Explicit, user-private plaintext fallback when a keyring is unavailable
- Ruff and locked-dependency audit validation on Linux
- pytest validation on Linux, macOS, and Windows with Python 3.13
- Wheel and source-distribution builds for CLI, core, and SDK packages
- Installed-wheel smoke tests and validated GitHub Release artifacts

For implementation history and roadmap, see [`docs/PROGRESS.md`](docs/PROGRESS.md). For per-PR bilingual records, see [`docs/pull-requests/README.md`](docs/pull-requests/README.md).

## Development installation

The repository is a uv workspace and requires Python 3.13 or later.

```bash
git clone https://github.com/LEEBONGHAK/modelctl.git
cd modelctl
git switch refac
uv sync --all-packages --locked
uv run modelctl --help
```

## Quick start

### 1. Store a provider credential

```bash
modelctl auth login openrouter
```

Credentials are stored in the operating-system keyring by default. `modelctl` does not silently downgrade to plaintext storage when the keyring is unavailable.

Only when you explicitly accept the risk may you use the protected local-file fallback:

```bash
modelctl auth login openrouter --allow-plaintext-fallback
```

The fallback file is restricted to the current user on POSIX systems, but it is still **unencrypted plaintext**. Prefer the keyring or an environment variable such as `MODELCTL_OPENROUTER`.

### 2. Synchronize and select a model

```bash
modelctl models sync openrouter
modelctl use
```

Non-interactive selection for scripts and CI:

```bash
modelctl use \
  --provider openrouter \
  --model anthropic/claude-sonnet-4
```

`--provider` and `--model` must be supplied together. Direct selections are validated against the provider registry and synchronized local model catalog.

### 3. Select a coding-agent launcher

```bash
modelctl launchers list
modelctl launchers use claude
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

Arguments after `run` are forwarded as an argument list to the native launcher:

```bash
modelctl run --continue
modelctl run --sandbox workspace-write
modelctl run --no-auto-commits
```

## Compatibility feedback

Claude Code, Gemini CLI, and Codex CLI are native clients for Anthropic, Google, and OpenAI respectively. When a model from another provider is passed to one of those launchers, `modelctl` displays a non-blocking warning before execution and through `modelctl doctor`.

For automatic OpenRouter model-name translation, select Aider:

```bash
modelctl launchers use aider
modelctl config set provider openrouter
modelctl config set model anthropic/claude-sonnet-4
modelctl run
```

Resulting command:

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
~/.config/modelctl/credentials.json   # only for explicit fallback
~/.local/share/modelctl/modelctl.db
```

Configuration and fallback credential writes are atomic. On POSIX systems, private directories and files are hardened to `0700` and `0600`. Symbolic-link targets are rejected for protected files.

## Development and security checks

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
```

GitHub Actions performs:

- Ruff and locked-dependency auditing on Ubuntu
- Complete pytest suite on Ubuntu, macOS, and Windows with Python 3.13
- Distribution build and installed-wheel smoke validation
- Release-tag, artifact, and checksum validation
- Immutable full-commit pinning for external GitHub Actions

## Package and release validation

```bash
uv build packages/core --out-dir dist --no-sources
uv build packages/sdk --out-dir dist --no-sources
uv build apps/modelctl --out-dir dist --no-sources
python scripts/release_validation.py --tag v0.1.0
```

A completed version may be tagged manually after all three package versions match and the release commit is contained in `refac`. A valid `v*` tag creates a GitHub Release with verified distributions and `SHA256SUMS`.

**PyPI publishing is intentionally disabled.** No workflow job currently publishes packages to PyPI. See [`docs/RELEASING.md`](docs/RELEASING.md).

## Project structure

```text
apps/modelctl/       Typer CLI application
packages/core/       runtime services, providers, repositories, and launchers
packages/sdk/        SDK package foundation
scripts/             repository validation and release helpers
tests/               regression, integration, and security tests
docs/                project, release, security, and PR documentation
```

## Security

See [`SECURITY.md`](SECURITY.md) for credential-storage behavior, reporting guidance, supported versions, and known limitations. Security tests and dependency audits reduce known risk but do not replace an independent penetration test or formal security assessment.

## Near-term roadmap

- Complete and tag the first development release
- Stricter compatibility policies and automatic remediation
- Launcher capability and execution-request refactoring
- Profile management after the core configuration workflow is stable
