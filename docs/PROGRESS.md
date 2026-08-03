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
modelctl launchers use aider
modelctl doctor
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

| Launcher ID | CLI | Native provider | Model invocation |
| --- | --- | --- | --- |
| `claude` | Claude Code | Anthropic | `claude --model <model>` |
| `gemini` | Gemini CLI | Google | `gemini --model <model>` |
| `codex` | Codex CLI | OpenAI | `codex --model <model>` |
| `aider` | Aider | Multiple providers | `aider --model <model>` |

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

### Diagnostics and compatibility feedback

- `modelctl doctor`
- Configuration, provider, credential, model, launcher, compatibility, and database checks
- Non-zero exit code for required configuration or runtime failures
- Non-blocking warnings for missing credentials, missing launcher installations, and uncertain compatibility
- Native-provider metadata for Claude Code, Gemini CLI, and Codex CLI
- OpenRouter mismatch warning before execution when a native launcher receives a model selected from OpenRouter
- Aider remains the automatic OpenRouter integration and performs the required model-name translation

### Quality gates

- uv workspace installation in GitHub Actions
- Ruff correctness checks
- pytest regression suite
- Separate `CI` and `Test` workflows
- Both workflows pass on the latest merged diagnostic changes

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
| #8 | Record project progress and rewrite the current README workflow | Merged |
| #9 | Add `modelctl doctor` environment and configuration diagnostics | Merged |

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

Launcher compatibility currently uses a small native-provider hint rather than a full capability system. This is intentional: real launcher integrations are being stabilized before a broader execution-target abstraction is introduced.

## Known limitations and deferred refactoring

The following items are intentionally deferred until more working integrations exist:

- Strict compatibility enforcement and automatic remediation
- Plugin-based launcher discovery
- Typed execution target or launch request value objects
- Full static type-check enforcement across the repository
- Profile management implementation
- Release packaging and cross-platform installation validation

These are not blockers for the current working workflow, but they are candidates for later refactoring milestones.

## Next priorities

1. Add non-interactive provider and model selection for scripts and CI.
2. Add cross-platform tests for macOS, Linux, and Windows.
3. Prepare the first installable development release.
4. Add stricter compatibility policies after additional provider integrations exist.
5. Refactor launcher capabilities and execution requests around proven requirements.

## Validation commands

```bash
uv sync --all-packages
uv run ruff check .
uv run pytest
```
