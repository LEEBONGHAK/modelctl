# modelctl Project Progress

Last updated: 2026-08-03

## Project goal

`modelctl` is a universal command-line control plane for AI models and coding agents. The long-term goal is to become the **uv of AI coding agents**: one small CLI for selecting providers and models, managing credentials and configuration, and launching multiple coding-agent CLIs consistently.

The current development principle is:

1. Deliver a working end-to-end workflow first.
2. Add tests and CI gates around that workflow.
3. Refactor abstractions only after real integrations expose the common requirements.

## Current end-to-end workflow

The following workflow is implemented on the `refac` branch:

```bash
modelctl auth login openrouter
modelctl models sync openrouter
modelctl use
modelctl launchers list
modelctl launchers use claude
modelctl run
```

The selected provider, model, and launcher are persisted in:

```text
~/.config/modelctl/config.json
```

The local model database defaults to:

```text
~/.local/share/modelctl/modelctl.db
```

## Implemented features

### Provider and model selection

- Provider discovery and registry
- OpenRouter model synchronization
- Persistent model repository
- Interactive provider/model selection through `modelctl use`
- Favorite model display handling
- Persistent `provider` and `default_model` configuration

### Credentials and configuration

- Credential service with keyring support
- File-based credential fallback
- `modelctl auth` commands
- `modelctl config show`
- `modelctl config set provider <value>`
- `modelctl config set model <value>`
- `modelctl config set launcher <value>`

### Coding-agent launchers

| Launcher ID | CLI | Model invocation |
| --- | --- | --- |
| `claude` | Claude Code | `claude --model <model>` |
| `gemini` | Gemini CLI | `gemini --model <model>` |
| `codex` | Codex CLI | `codex --model <model>` |
| `aider` | Aider | `aider --model <model>` |

All launchers support forwarding native arguments after `modelctl run`.

Aider receives provider context. OpenRouter model IDs are translated from:

```text
anthropic/claude-sonnet-4
```

to:

```text
openrouter/anthropic/claude-sonnet-4
```

### Launcher management

- `modelctl launchers list`
- Rich table showing launcher ID, display name, active state, and local installation state
- `modelctl launchers use <launcher-id>`
- Validation for unknown launcher IDs

### Quality gates

- uv workspace installation in GitHub Actions
- Ruff correctness checks
- pytest regression suite
- Separate `CI` and `Test` workflows
- Both workflows pass on the latest merged launcher-management changes

## Completed pull requests

| PR | Summary | Result |
| --- | --- | --- |
| #1 | Make top-level `use` and `run` commands executable; repair container and configuration wiring | Merged |
| #2 | Stabilize workspace installation, lint, and test collection | Merged |
| #3 | Complete Claude Code execution and native argument forwarding | Merged |
| #4 | Add Gemini CLI launcher and repair runtime configuration commands | Merged |
| #5 | Add Codex CLI launcher | Merged |
| #6 | Add provider-aware Aider launcher | Merged |
| #7 | Add launcher listing and selection CLI | Merged |

## Architecture snapshot

The repository is organized as a uv workspace:

```text
apps/modelctl/       Typer CLI application
packages/core/       configuration, providers, repositories, services, launchers
packages/sdk/        public SDK package foundation
tests/               integration and regression tests
```

The runtime dependency flow is currently:

```text
Typer command
  -> application Container
  -> service
  -> provider / repository / launcher registry
  -> external CLI or API
```

## Known limitations and deferred refactoring

The following items are intentionally deferred until more working integrations exist:

- Formal launcher capability metadata
- Provider/model/launcher compatibility validation
- Plugin-based launcher discovery
- Typed execution target or launch request value objects
- Full static type-check enforcement across the repository
- Profile management implementation
- Release packaging and cross-platform installation validation

These are not blockers for the current working workflow, but they are candidates for later refactoring milestones.

## Next priorities

1. Add a `modelctl doctor` command that validates configuration, credentials, database access, and launcher installation.
2. Improve provider/model/launcher compatibility feedback before execution.
3. Add non-interactive model selection for scripts and CI.
4. Add cross-platform tests for macOS, Linux, and Windows.
5. Prepare the first installable development release.

## Validation commands

```bash
uv sync --all-packages
uv run ruff check .
uv run pytest
```
