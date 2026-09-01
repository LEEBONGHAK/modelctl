# modelctl Project Progress

Last updated: 2026-09-01

## Project goal

`modelctl` is a universal command-line control plane for AI models and coding agents. The long-term goal is to become the **uv of AI coding agents**: one small CLI for selecting providers and models, managing credentials and reusable configuration, and launching multiple coding-agent CLIs consistently.

Development principle:

1. Deliver a working end-to-end workflow first.
2. Add regression, cross-platform, packaging, release, and security gates.
3. Refactor abstractions only after real integrations expose common requirements.

## Branch and release state

- Canonical release branch: `main`
- Ongoing development branch: `refac`
- Latest ready and published version: `0.2.0`
- Active development version: `0.3.0`
- Manifest status: `draft`
- Active feature branch: `feat/v0.3.0-plugin-diagnostics`
- Active pull request: #40
- PyPI publication: disabled
- Completion criteria: [`RELEASE_CRITERIA.md`](RELEASE_CRITERIA.md)

The v0.2.0 tag and immutable GitHub Release were created from exact `main` commit `9da3f46fc2fe817c2643437d48f42dd078f26482` after clean audit, Ruff, tests, builds, installed-wheel smoke checks, and checksums passed.

## Completed v0.3.0 increments

### Named profiles — PR #36

- save, list, show, use, and delete named configuration snapshots
- validate provider/model and launcher selection before one atomic configuration write
- preserve unrelated settings and exclude all credentials from profiles

### Versioned launcher plugin SDK — PR #37

- public immutable `LaunchRequest`
- explicit `LauncherCapabilities`
- stable `LauncherMetadata`
- public `LauncherPlugin` protocol
- launcher contract version `1.0` with major-version compatibility validation

### Installed launcher discovery — PR #39

- discover only installed `modelctl.launchers` Python entry points
- preserve built-ins and reject built-in ID collisions before loading external code
- reject duplicate external launcher IDs deterministically
- isolate import, initialization, metadata, and contract failures
- adapt valid plugins into the existing core launcher runtime
- verify real installed entry-point discovery in isolated packaging smoke tests

PR #38 contains the same discovery implementation history but was closed unmerged after the connected GitHub draft-to-ready transition failed because of an upstream GraphQL schema incompatibility. PR #39 is the actual merged implementation path.

## Current v0.3.0 increment: plugin diagnostics and compatibility hardening

PR #40 extends the working plugin path rather than introducing a second plugin runtime.

### Doctor diagnostics

`modelctl doctor` now evaluates each installed external launcher and reports:

- package distribution origin
- plugin ID
- SDK contract compatibility
- launcher executable availability
- duplicate entry-point conflicts
- import, initialization, metadata, and contract failures
- availability probe failures

A broken plugin unrelated to the current launcher remains isolated and reports `WARN`. If the currently selected launcher itself failed discovery, the plugin diagnostic is promoted to `ERROR` alongside the unknown-launcher error.

### Compatibility hardening

Regression coverage verifies that discovered plugins use the same capability-driven runtime as built-ins:

- provider-aware recommendation
- preview-first remediation
- strict compatibility checks
- immutable `LaunchRequest` construction
- native argument forwarding through `extra_args`
- refusal to apply unavailable recommended launchers

## Stable v0.2.0 workflows

### OpenRouter through Aider

```bash
modelctl auth login openrouter
modelctl models sync openrouter
modelctl use --provider openrouter --model anthropic/claude-sonnet-4
modelctl launchers remediate --apply
modelctl config set compatibility-policy strict
modelctl doctor
modelctl run
```

### Native providers

- Anthropic catalog through Claude Code
- Google Gemini catalog through Gemini CLI
- OpenAI native catalog through Codex CLI

Provider catalog credentials remain separate from launcher authentication and are never injected from keyring storage into launcher subprocess environments.

## Remaining v0.3.0 sequence

1. Validate real profile usage and add portability only where a concrete need is demonstrated.
2. Introduce static type-check enforcement at the SDK, profile, and plugin boundaries.
3. Review the complete v0.3.0 documentation and release criteria.
4. Complete a dedicated readiness review before promotion to `main`.

Explicit non-goals remain provider plugins, automatic plugin installation, remote registries, arbitrary filesystem plugin paths, credential export, and PyPI publication during feature development.

## Validation commands

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
python scripts/release_validation.py
python scripts/release_validation.py --print-status
```
