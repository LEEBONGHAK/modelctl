# modelctl

[English](README.md) | [한국어](README.ko.md)

**The universal AI model and coding-agent control plane.**

`modelctl` provides one CLI for selecting AI providers and models, managing local credentials and defaults, diagnosing compatibility, and launching coding-agent CLIs consistently.

> Current ready development version: `0.2.0`. `main` is the canonical release branch. PyPI publication remains disabled.

## v0.2.0 highlights

- OpenRouter, Anthropic, Google Gemini, and OpenAI model catalogs
- Claude Code, Gemini CLI, Codex CLI, and Aider launchers
- Interactive and non-interactive provider/model selection
- Provider-aware launcher recommendations
- Preview-first compatibility remediation with explicit safe apply
- Persisted `warn` or `strict` compatibility policies and per-run overrides
- Native launcher argument forwarding without shell execution
- Keyring-first credential storage with explicit plaintext fallback
- Provider credentials kept separate from launcher authentication
- Provider API contract tests, 137 cross-platform tests, package builds, and installed-wheel smoke tests
- Locked `cryptography 50.0.0` and dependency audit without an advisory exclusion
- Validated immutable GitHub Release artifacts with SHA-256 checksums

See [`docs/PROGRESS.md`](docs/PROGRESS.md) for project status and [`docs/pull-requests/README.md`](docs/pull-requests/README.md) for bilingual engineering history.

## Installation from the repository

The repository is a Python 3.13+ uv workspace.

```bash
git clone https://github.com/LEEBONGHAK/modelctl.git
cd modelctl
git switch main
uv sync --all-packages --locked
uv run modelctl --help
```

## Provider workflows

### OpenRouter through Aider

```bash
modelctl auth login openrouter
modelctl models sync openrouter
modelctl use --provider openrouter --model anthropic/claude-sonnet-4
modelctl launchers remediate
modelctl launchers remediate --apply
modelctl config set compatibility-policy strict
modelctl run
```

Aider translates the selected model to:

```text
openrouter/anthropic/claude-sonnet-4
```

### Anthropic through Claude Code

```bash
modelctl auth login anthropic
modelctl models sync anthropic
modelctl use --provider anthropic --model claude-opus-4-6
modelctl launchers recommend
modelctl config set compatibility-policy strict
modelctl run
```

`ANTHROPIC_API_KEY` can replace stored modelctl credentials for catalog synchronization.

### Google Gemini through Gemini CLI

```bash
modelctl auth login google
modelctl models sync google
modelctl use --provider google --model gemini-3.5-flash
modelctl launchers recommend
modelctl config set compatibility-policy strict
modelctl run
```

Environment precedence is `MODELCTL_GOOGLE`, `GOOGLE_API_KEY`, then `GEMINI_API_KEY`.

### OpenAI through Codex CLI

```bash
modelctl auth login openai
modelctl models sync openai
modelctl use --provider openai --model gpt-5.6
modelctl launchers recommend
modelctl config set compatibility-policy strict
modelctl run
```

`OPENAI_API_KEY` can replace stored modelctl credentials for catalog synchronization.

Provider credentials managed by modelctl are used for catalog synchronization only. They are not copied from keyring storage into launcher subprocess environments; each coding-agent CLI owns its supported authentication flow.

## Launcher management

```bash
modelctl launchers list
modelctl launchers recommend
modelctl launchers recommend --apply
modelctl launchers remediate
modelctl launchers remediate --apply
modelctl launchers use aider
```

| ID | Coding agent | Native provider | Base invocation |
| --- | --- | --- | --- |
| `claude` | Claude Code | Anthropic | `claude --model <model>` |
| `gemini` | Gemini CLI | Google | `gemini --model <model>` |
| `codex` | Codex CLI | OpenAI | `codex --model <model>` |
| `aider` | Aider | Translated providers | `aider --model <model>` |

`recommend` proposes a capability-compatible launcher. `remediate` creates a change plan only when the active launcher has a known mismatch.

Both commands are read-only by default. Their `--apply` variants change only the selected launcher and refuse unavailable recommendations before configuration mutation. They never install software, change the provider or model, or start a launcher.

## Compatibility and execution

The persisted policy defaults to backward-compatible `warn` behavior.

```bash
modelctl config set compatibility-policy warn
modelctl config set compatibility-policy strict
modelctl doctor
modelctl run
```

Override it for one execution:

```bash
modelctl run --strict-compatibility
modelctl run --warn-compatibility
```

Unknown arguments after `run` are forwarded unchanged to the selected launcher:

```bash
modelctl run --continue
modelctl run --sandbox workspace-write
modelctl run --strict-compatibility --sandbox workspace-write
modelctl run --no-auto-commits
```

Use `--` when a launcher argument conflicts with a modelctl-owned option.

## Credentials and local data

The default login flow stores credentials in the operating-system keyring. It never silently downgrades to plaintext storage.

```bash
modelctl auth login openrouter --allow-plaintext-fallback
```

The explicitly approved fallback is unencrypted plaintext. Protected paths use atomic writes, reject symbolic links, and use `0700` directories and `0600` files on POSIX systems.

```text
~/.config/modelctl/config.json
~/.config/modelctl/credentials.json   # explicit fallback only
~/.local/share/modelctl/modelctl.db
```

## Development and validation

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
python scripts/release_validation.py --tag v0.2.0
```

GitHub Actions independently runs provider contract tests, the complete pytest suite on Ubuntu, macOS, and Windows, all distribution builds, isolated installed-wheel validation, release metadata checks, and checksum generation.

## Release policy

Release decisions are declared in [`release.toml`](release.toml), changes in [`CHANGELOG.md`](CHANGELOG.md), and the completion checklist in [`docs/RELEASE_CRITERIA.md`](docs/RELEASE_CRITERIA.md).

The `0.2.0` manifest is `ready`. A reviewed pull request targeting `main` must still pass every dry-run gate. After merge, the release workflow checks out the exact `main` merge commit and repeats all gates before creating immutable tag `v0.2.0` and one GitHub Release.

Existing tags and release assets are never overwritten. **No workflow publishes packages to PyPI.** See [`docs/RELEASING.md`](docs/RELEASING.md).

## Project structure

```text
apps/modelctl/       Typer CLI application
packages/core/       runtime services, credentials, providers, repositories, launchers
packages/sdk/        SDK foundation
scripts/             release validation helpers
tests/               regression, integration, packaging, and security tests
docs/                provider, project, release, security, and PR documentation
```

## Security

See [`SECURITY.md`](SECURITY.md) for credential behavior, reporting guidance, dependency security, release trust boundaries, and known limitations.

## Post-v0.2.0 roadmap

- Extract shared provider HTTP helpers only where proven integrations have identical requirements
- Extend remediation only with safe, reversible, previewable actions
- Add tested profile management and plugin-based launcher discovery
- Introduce static type-check enforcement as a separate quality milestone
- Review PyPI Trusted Publishing separately
