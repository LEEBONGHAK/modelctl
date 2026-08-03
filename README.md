# modelctl

**The universal AI model and coding-agent control plane.**

`modelctl` aims to become the **uv of AI coding agents**: one CLI for selecting AI providers and models, managing local configuration, and launching coding agents consistently.

> Development status: active, pre-release. The working implementation currently lives on the `refac` branch.

## What works today

- OpenRouter credential and model workflow
- Interactive provider/model selection with `modelctl use`
- Persistent provider, model, and launcher configuration
- Claude Code, Gemini CLI, Codex CLI, and Aider launchers
- Native launcher argument forwarding
- Launcher discovery, installation status, and selection
- Local environment diagnostics with `modelctl doctor`
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

```bash
modelctl auth login openrouter
modelctl models sync openrouter
modelctl use
```

### 2. Select a coding-agent launcher

```bash
modelctl launchers list
modelctl launchers use claude
```

Supported launcher IDs:

| ID | Coding agent | Base command |
| --- | --- | --- |
| `claude` | Claude Code | `claude --model <model>` |
| `gemini` | Gemini CLI | `gemini --model <model>` |
| `codex` | Codex CLI | `codex --model <model>` |
| `aider` | Aider | `aider --model <model>` |

### 3. Diagnose the local setup

```bash
modelctl doctor
```

The command checks:

- configuration file availability
- selected provider and model
- provider credential availability
- selected launcher registration and installation
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

- Provider/model/launcher compatibility feedback
- Non-interactive model selection
- Cross-platform CI
- First development release
