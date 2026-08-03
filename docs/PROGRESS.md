# modelctl Project Progress

Last updated: 2026-08-03

## Project goal

`modelctl` is a universal command-line control plane for AI models and coding agents. The long-term goal is to become the **uv of AI coding agents**: one small CLI for selecting providers and models, managing credentials and configuration, and launching multiple coding-agent CLIs consistently.

The current development principle is:

1. Deliver a working end-to-end workflow first.
2. Add tests and CI gates around that workflow.
3. Refactor abstractions only after real integrations expose the common requirements.

## Current end-to-end workflow

The following interactive workflow is implemented on the `refac` branch:

```bash
modelctl auth login openrouter
modelctl models sync openrouter
modelctl use
modelctl launchers list
modelctl launchers use aider
modelctl doctor
modelctl run
```

Scripts and CI can select a synchronized provider/model pair without an interactive prompt:

```bash
modelctl use \
  --provider openrouter \
  --model anthropic/claude-sonnet-4
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
- Provider-scoped model lookup
- Interactive provider/model selection through `modelctl use`
- Non-interactive selection through `modelctl use --provider <id> --model <id>`
- Validation that direct selections use a registered provider and synchronized model
- Requirement that `--provider` and `--model` are supplied together
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

### Packaging and installed-artifact validation

- Hatchling wheel and source-distribution builds for `modelctl`, `modelctl-core`, and `modelctl-sdk`
- Standards-oriented builds with workspace source overrides disabled
- Shared `dist/` output for coordinated release artifacts
- Fresh virtual environment installation from built wheels
- Installed import checks for CLI, core, and SDK packages
- Installed `modelctl version` and `modelctl --help` smoke tests
- Distribution artifacts uploaded from GitHub Actions
- CLI version output read from installed distribution metadata instead of a hardcoded command string

### Quality gates

- Locked uv workspace installation in GitHub Actions
- Ruff correctness checks on Ubuntu with Python 3.13
- Complete pytest suite on Ubuntu with Python 3.13
- Complete pytest suite on macOS with Python 3.13
- Complete pytest suite on Windows with Python 3.13
- Matrix fail-fast disabled so every platform reports independently
- Package build and isolated installation smoke workflow on Ubuntu with Python 3.13
- Regression coverage for interactive and non-interactive selection
- Repository-level coverage for provider-scoped model queries
- Regression coverage for installed distribution version lookup

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
| #10 | Add provider/model/launcher compatibility feedback | Merged |
| #11 | Add non-interactive provider and model selection | Merged |
| #12 | Add Linux, macOS, and Windows test matrix | Merged |
| #13 | Build release distributions and smoke-test installed wheels | Merged |

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

- Automated release tagging and package-index publishing
- Strict compatibility enforcement and automatic remediation
- Plugin-based launcher discovery
- Typed execution target or launch request value objects
- Full static type-check enforcement across the repository
- Profile management implementation

These are not blockers for the current working workflow, but they are candidates for later refactoring milestones.

## Next priorities

1. Add release tag validation and publishing automation.
2. Produce the first installable development release.
3. Add stricter compatibility policies after additional provider integrations exist.
4. Refactor launcher capabilities and execution requests around proven requirements.
5. Implement profile management after the core configuration workflow stabilizes.

## Validation commands

```bash
uv sync --all-packages --locked
uv run ruff check .
uv run pytest
uv build packages/core --out-dir dist --no-sources
uv build packages/sdk --out-dir dist --no-sources
uv build apps/modelctl --out-dir dist --no-sources
```
