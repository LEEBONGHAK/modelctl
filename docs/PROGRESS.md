# modelctl Project Progress

Last updated: 2026-08-03

## Project goal

`modelctl` is a universal command-line control plane for AI models and coding agents. The long-term goal is to become the **uv of AI coding agents**: one small CLI for selecting providers and models, managing credentials and configuration, and launching multiple coding-agent CLIs consistently.

Development principle:

1. Deliver a working end-to-end workflow first.
2. Add regression, cross-platform, packaging, release, and security gates.
3. Refactor abstractions only after real integrations expose common requirements.

## Branch and release state

- Release branch: `main`
- Ongoing development branch: `refac`
- Completed release: `0.1.0` on `main`
- Coordinated development version: `0.2.0` on `refac`
- Manifest: `release.toml`
- Status: `draft`
- Channel: development release
- PyPI: disabled
- Completion criteria: [`RELEASE_CRITERIA.md`](RELEASE_CRITERIA.md)
- Notable changes: [`CHANGELOG.md`](../CHANGELOG.md)

Draft status prevents publication while v0.2.0 is under development. After an explicit readiness review, a reviewed pull request merged into `main`, or a trusted direct `main` push, creates the version tag and GitHub Release only after the release workflow independently passes dependency audit, Ruff, the complete pytest suite, distribution builds, installed-wheel smoke tests, and checksum generation.

## Current end-to-end workflow

```bash
modelctl auth login openrouter
modelctl models sync openrouter
modelctl use
modelctl launchers list
modelctl launchers recommend
modelctl launchers recommend --apply
modelctl launchers use aider
modelctl doctor
modelctl run
```

Non-interactive selection:

```bash
modelctl use \
  --provider openrouter \
  --model anthropic/claude-sonnet-4
```

Local state defaults:

```text
~/.config/modelctl/config.json
~/.config/modelctl/credentials.json   # explicit plaintext fallback only
~/.local/share/modelctl/modelctl.db
```

## Implemented features

### Provider, model, credentials, and configuration

- Provider discovery and registry
- OpenRouter model synchronization with credential validation and bounded HTTP timeouts
- Persistent model repository and provider-scoped lookup
- Interactive and non-interactive provider/model selection
- Validation of registered providers and synchronized models
- Favorite-model support
- Environment-variable and operating-system keyring lookup
- Keyring-first credential storage with no silent plaintext downgrade
- Explicit `--allow-plaintext-fallback`
- Provider-ID and empty-token validation
- Atomic configuration and fallback-credential writes
- Symbolic-link rejection for protected files
- POSIX private directory/file permissions (`0700` / `0600`)
- Shared credential service for authentication, diagnostics, and synchronization

### Coding-agent launchers

| Launcher ID | CLI | Native provider | Model invocation |
| --- | --- | --- | --- |
| `claude` | Claude Code | Anthropic | `claude --model <model>` |
| `gemini` | Gemini CLI | Google | `gemini --model <model>` |
| `codex` | Codex CLI | OpenAI | `codex --model <model>` |
| `aider` | Aider | Multiple providers | `aider --model <model>` |

All launchers forward native arguments as subprocess argument lists without shell execution. Aider translates OpenRouter model IDs to `openrouter/<provider>/<model>`.

### Management, diagnostics, and compatibility

- `modelctl launchers list`
- `modelctl launchers recommend [--apply]`
- `modelctl launchers use <launcher-id>`
- Installation-state and active-launcher display
- Provider-aware recommendation of Aider for OpenRouter and native launchers for supported native providers
- Read-only recommendation inspection and explicit apply that refuses unavailable launchers
- `modelctl doctor`
- Configuration, provider, credential, model, launcher, compatibility, and database checks
- Non-blocking native-provider mismatch warnings

### Packaging and release

- Coordinated wheel and source-distribution builds for `modelctl`, `modelctl-core`, and `modelctl-sdk`
- Workspace source overrides disabled for release builds
- Fresh-environment installed-wheel import and CLI smoke tests
- Coordinated package, manifest, changelog, documentation, and tag validation
- Machine-readable readiness status in `release.toml`
- Validation that manually tagged commits belong to `main`
- Release workflow-owned dependency audit, lint, complete tests, build, smoke test, and checksum gates
- Automatic tag creation only from successful trusted `main` changes marked `ready`
- Trusted merged-PR validation against the exact `main` merge commit
- Immutable GitHub Release creation with distributions and `SHA256SUMS`
- Existing tags and release assets are never overwritten
- PyPI publication intentionally disabled

### Documentation and security gates

- English README and complete Korean `README.ko.md`
- Bilingual release guide, completion criteria, and security policy
- Per-PR English/Korean engineering records
- Locked uv workspace installation
- Ruff and `uv audit --locked`
- Complete pytest suite on Ubuntu, macOS, and Windows with Python 3.13
- Full commit-SHA pinning for external GitHub Actions
- Least-privilege workflow permissions
- Security regression coverage for private files, credential fallback, untrusted tags, merged-event trust boundaries, and model synchronization

## Completed pull requests

| PR | Summary | Result |
| --- | --- | --- |
| #1 | Make top-level `use` and `run` executable; repair wiring | Merged |
| #2 | Stabilize workspace installation, lint, and test collection | Merged |
| #3 | Complete Claude Code execution and argument forwarding | Merged |
| #4 | Add Gemini CLI and repair runtime configuration | Merged |
| #5 | Add Codex CLI launcher | Merged |
| #6 | Add provider-aware Aider launcher | Merged |
| #7 | Add launcher listing and selection | Merged |
| #8 | Record project progress and rewrite README | Merged |
| #9 | Add `modelctl doctor` | Merged |
| #10 | Add provider/model/launcher compatibility feedback | Merged |
| #11 | Add non-interactive provider and model selection | Merged |
| #12 | Add Linux, macOS, and Windows test matrix | Merged |
| #13 | Build distributions and smoke-test installed wheels | Merged |
| #14 | Add bilingual records for PRs #1–#13 | Merged |
| #15 | Validate release tags and automate GitHub Release creation | Merged |
| #16 | Harden credentials, local state, workflows, and Korean documentation | Merged |
| #17 | Define v0.1.0 readiness and complete release gates | Merged |
| #18 | Add trusted merged-PR release publication path | Merged |
| #19 | Promote completed v0.1.0 to `main` | Merged |
| #20 | Add an owner-only fully validated release command | Merged |

## Active v0.2.0 development

- First feature branch: `feat/v0.2.0-launcher-recommendation`
- First workflow: inspect a provider-aware recommendation, then opt in with `--apply`
- Version state: coordinated `0.2.0`, `status = "draft"`, PyPI disabled
- Compatibility guarantee: existing launcher execution remains valid without provider context; recommendations require a selected provider and model

## Architecture snapshot

```text
apps/modelctl/       Typer CLI application
packages/core/       configuration, credentials, providers, repositories, services, launchers
packages/sdk/        public SDK package foundation
scripts/             release validation helpers
tests/               regression, integration, packaging, and security tests
docs/                project, release, security, and PR documentation
```

```text
Typer command
  -> application Container
  -> service
  -> credential / provider / repository / launcher registry
  -> external CLI or API
```

## Known limitations and deferred work

- No PyPI publication
- Strict compatibility enforcement and automatic remediation are not implemented
- Plugin-based launcher discovery is deferred
- Execution-target and launch-request value objects are not yet formalized
- Full static type-check enforcement is not yet a quality gate
- Local plaintext credential fallback remains unencrypted and should be used only when explicitly accepted
- The security review is source- and test-based, not an independent penetration test

## Next priorities

1. Validate and merge the provider-aware launcher recommendation workflow.
2. Add stricter compatibility policies after additional provider integrations exist.
3. Refactor launcher capabilities and execution requests around proven requirements.
4. Reintroduce profile management only with a complete user workflow and tests.
5. Plan a separate reviewed PyPI publication milestone when ownership and Trusted Publishing are ready.

## Validation commands

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
uv build packages/core --out-dir dist --no-sources
uv build packages/sdk --out-dir dist --no-sources
uv build apps/modelctl --out-dir dist --no-sources
python scripts/release_validation.py
python scripts/release_validation.py --print-status
python scripts/release_validation.py --tag v0.2.0
```
