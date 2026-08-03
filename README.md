# modelctl

**The universal AI model and coding-agent control plane.**

`modelctl` aims to become the **uv of AI coding agents**: one CLI for selecting AI providers and models, managing local configuration, and launching coding agents consistently.

> Development status: active, pre-release. The working implementation currently lives on the `refac` branch.

## What works today

- OpenRouter credential and model workflow
- Interactive and non-interactive provider/model selection with `modelctl use`
- Persistent provider, model, and launcher configuration
- Claude Code, Gemini CLI, Codex CLI, and Aider launchers
- Native launcher argument forwarding
- Launcher discovery, installation status, and selection
- Local environment diagnostics with `modelctl doctor`
- Non-blocking provider/model/launcher compatibility feedback
- Ruff and pytest GitHub Actions checks

For the detailed implementation history, architecture snapshot, known limitations, and roadmap, see [`docs/PROGRESS.md`](docs/PROGRESS.md).

## Installation for development

The repository is a uv workspace.

```bash
git clone https://github.com/LEEBONGHAK/modelctl.git
cd modelctl
git switch refac
uv sync --all-packages
```

Run the CLI through uv:

```bash
uv run modelctl --help
```

## Quick start

### 1. Configure a provider and model

Authenticate and synchronize the provider model catalog:

```bash
modelctl auth login openrouter
modelctl models sync openrouter
```

Select interactively:

```bash
modelctl use
```

Select without a prompt for scripts and CI:

```bash
modelctl use \
  --provider openrouter \
  --model anthropic/claude-sonnet-4
```

`--provider` and `--model` must be supplied together. The command validates that the provider is registered and the model exists in the synchronized local catalog before updating the configuration.

### 2. Select a coding-agent launcher

```bash
modelctl launchers list
modelctl launchers use claude
```

Supported launcher IDs:

| ID | Coding agent | Native provider | Base command |
| --- | --- | --- | --- |
| `claude` | Claude Code | Anthropic | `claude --model <model>` |
| `gemini` | Gemini CLI | Google | `gemini --model <model>` |
| `codex` | Codex CLI | OpenAI | `codex --model <model>` |
| `aider` | Aider | Multiple providers | `aider --model <model>` |

### 3. Diagnose the local setup

```bash
modelctl doctor
```

The command checks:

- configuration file availability
- selected provider and model
- provider credential availability
- selected launcher registration and installation
- provider/model/launcher compatibility
- local database connectivity

Warnings do not fail the command, while configuration or runtime errors return a non-zero exit code.

### 4. Run the selected launcher

```bash
modelctl run
```

Arguments after `run` are forwarded to the native launcher:

```bash
modelctl run --continue
modelctl run --sandbox workspace-write
modelctl run --no-auto-commits
```

## Compatibility feedback

Claude Code, Gemini CLI, and Codex CLI are native clients for Anthropic, Google, and OpenAI respectively. When a model selected from another provider is passed to one of those launchers, `modelctl` displays a non-blocking warning before execution and reports the same warning through `modelctl doctor`.

The model is still forwarded unchanged because advanced users may have configured a compatible proxy or custom endpoint outside `modelctl`.

For OpenRouter models, Aider is the currently supported automatic integration:

```bash
modelctl launchers use aider
```

## Aider with OpenRouter

Aider requires OpenRouter model names to use an `openrouter/` prefix. `modelctl` performs this translation automatically.

```bash
modelctl launchers use aider
modelctl config set provider openrouter
modelctl config set model anthropic/claude-sonnet-4
modelctl run
```

The resulting command is:

```bash
aider --model openrouter/anthropic/claude-sonnet-4
```

## Configuration

```bash
modelctl config show
modelctl config set provider openrouter
modelctl config set model anthropic/claude-sonnet-4
modelctl config set launcher aider
```

Default paths:

```text
~/.config/modelctl/config.json
~/.local/share/modelctl/modelctl.db
```

## Development checks

```bash
uv sync --all-packages
uv run ruff check .
uv run pytest
```

## Project structure

```text
apps/modelctl/       Typer CLI application
packages/core/       runtime services, providers, repositories, and launchers
packages/sdk/        SDK package foundation
tests/               regression and integration tests
docs/                project status and design documentation
```

## Near-term roadmap

- Cross-platform CI
- First development release
- Stricter compatibility policies and automatic remediation
- Launcher capability and execution-request refactoring
