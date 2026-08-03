# modelctl Project Progress

Last updated: 2026-08-03

## Project goal

`modelctl` is a universal command-line control plane for AI models and coding agents. The long-term goal is to become the **uv of AI coding agents**: one small CLI for selecting providers and models, managing credentials and configuration, and launching multiple coding-agent CLIs consistently.

Development principle:

1. Deliver a working end-to-end workflow first.
2. Add regression, cross-platform, packaging, release, and security gates.
3. Refactor abstractions only after real integrations expose common requirements.

## Current end-to-end workflow

```bash
modelctl auth login openrouter
modelctl models sync openrouter
modelctl use
modelctl launchers list
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

### Provider and model selection

- Provider discovery and registry
- OpenRouter model synchronization with credential validation and bounded HTTP timeouts
- Persistent model repository and provider-scoped lookup
- Interactive and non-interactive provider/model selection
- Validation of registered providers and synchronized models
- Favorite-model support

### Credentials and local configuration

- Environment-variable and operating-system keyring lookup
- Keyring-first credential storage
- No silent downgrade from keyring failure to plaintext
- Explicit `--allow-plaintext-fallback` compatibility option
- Provider-ID and empty-token validation
- Atomic configuration and fallback-credential writes
- Symbolic-link rejection for protected files
- POSIX private directory/file permissions (`0700` / `0600`)
- Shared credential service used by authentication, diagnostics, and model synchronization

### Coding-agent launchers

| Launcher ID | CLI | Native provider | Model invocation |
| --- | --- | --- | --- |
| `claude` | Claude Code | Anthropic | `claude --model <model>` |
| `gemini` | Gemini CLI | Google | `gemini --model <model>` |
| `codex` | Codex CLI | OpenAI | `codex --model <model>` |
| `aider` | Aider | Multiple providers | `aider --model <model>` |

All launchers forward native arguments as subprocess argument lists without shell execution. Aider translates OpenRouter model IDs to the required `openrouter/<provider>/<model>` form.

### Launcher management, diagnostics, and compatibility

- `modelctl launchers list`
- `modelctl launchers use <launcher-id>`
- Installation-state and active-launcher display
- `modelctl doctor`
- Configuration, provider, credential, model, launcher, compatibility, and database checks
- Non-blocking native-provider mismatch warnings

### Packaging and release validation

- Coordinated wheel and source-distribution builds for `modelctl`, `modelctl-core`, and `modelctl-sdk`
- Workspace source overrides disabled for release-oriented builds
- Fresh-environment installed-wheel import and CLI smoke tests
- Coordinated package-version and `v*` tag validation
- Validation that tagged commits belong to `refac`
- SHA-256 checksum generation
- New GitHub Release creation for validated completed-version tags
- Refusal to overwrite an existing GitHub Release
- PyPI publication intentionally disabled

### Documentation

- English README and complete Korean `README.ko.md`
- Bilingual release guide and security policy
- Per-PR English/Korean engineering records under `docs/pull-requests/`

### Quality and security gates

- Locked uv workspace installation
- Ruff checks and `uv audit --locked` on Ubuntu
- Complete pytest suite on Ubuntu, macOS, and Windows with Python 3.13
- Package build and installed-wheel smoke workflow
- Release dry-run workflow
- Full commit-SHA pinning for external GitHub Actions
- Least-privilege workflow permissions
- Security regression coverage for private files, credential fallback, untrusted release tags, and credential-backed model synchronization

## Completed pull requests

| PR | Summary | Result |
| --- | --- | --- |
| #1 | Make top-level `use` and `run` executable; repair container and configuration wiring | Merged |
| #2 | Stabilize workspace installation, lint, and test collection | Merged |
| #3 | Complete Claude Code execution and native argument forwarding | Merged |
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

## Architecture snapshot

```text
apps/modelctl/       Typer CLI application
packages/core/       configuration, credentials, providers, repositories, services, launchers
packages/sdk/        public SDK package foundation
scripts/             release and repository validation helpers
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

## Removed obsolete code

- Duplicate placeholder `doctor()` registration removed after the real diagnostic command became authoritative.
- Unused, entirely unimplemented `ProfileService` stub removed. Profile support may be reintroduced when its actual requirements are implemented and tested.

## Known limitations and deferred work

- No PyPI publication
- No tagged development release yet
- Strict compatibility enforcement and automatic remediation are not implemented
- Plugin-based launcher discovery is deferred
- Execution-target and launch-request value objects are not yet formalized
- Full static type-check enforcement is not yet a quality gate
- Local plaintext credential fallback remains unencrypted and should be used only when explicitly accepted
- The security review is source- and test-based, not an independent penetration test

## Next priorities

1. Define completion criteria for the first development version and create its validated tag when met.
2. Add stricter compatibility policies after additional provider integrations exist.
3. Refactor launcher capabilities and execution requests around proven requirements.
4. Reintroduce profile management only with a complete user workflow and tests.
5. Plan a separate reviewed PyPI publication milestone when package ownership and Trusted Publishing are ready.

## Validation commands

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
uv build packages/core --out-dir dist --no-sources
uv build packages/sdk --out-dir dist --no-sources
uv build apps/modelctl --out-dir dist --no-sources
python scripts/release_validation.py --tag v0.1.0
```
