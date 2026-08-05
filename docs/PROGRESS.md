# modelctl Project Progress

Last updated: 2026-08-05

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
- Active feature branch: `feat/v0.3.0-named-profiles`
- Active pull request: #36
- PyPI publication: disabled
- Completion criteria: [`RELEASE_CRITERIA.md`](RELEASE_CRITERIA.md)

The v0.2.0 tag and immutable GitHub Release were created from exact `main` commit `9da3f46fc2fe817c2643437d48f42dd078f26482` after clean audit, Ruff, 138 tests, builds, installed-wheel smoke checks, and checksums passed.

## Current v0.3.0 increment: named profiles

PR #36 introduces the first v0.3.0 end-to-end workflow:

```bash
modelctl profiles save work
modelctl profiles list
modelctl profiles show work
modelctl profiles use work
modelctl profiles delete work
```

A profile snapshots:

- provider
- default model
- launcher
- compatibility policy

### Behavior completed

- Names are trimmed, normalized to lowercase, and validated consistently.
- Saving captures the current effective defaults, including backward-compatible launcher and policy defaults.
- Listing is deterministic and sorted by profile name.
- Applying validates the provider/model and launcher before any configuration mutation.
- Applying performs one atomic configuration write and preserves unrelated settings and profiles.
- Deleting the final profile removes the empty profile container.
- Unknown names, malformed snapshots, missing fields, and unexpected fields fail explicitly.
- Credentials, environment secrets, and launcher-managed authentication data are not part of the schema.
- Existing `config`, `use`, `doctor`, `launchers`, and `run` workflows remain compatible.

### Validation completed

- Coordinated workspace, CLI, core, SDK, manifest, and lockfile at `0.3.0`.
- Release state remains `draft` and non-publishing.
- Primary CI passed dependency audit, Ruff, and provider contract suites.
- All 150 tests passed on Ubuntu, macOS, and Windows with Python 3.13.
- All wheel and source distributions built successfully.
- Built wheels installed together in an isolated environment.
- Installed package imports, `modelctl version`, and `modelctl --help` passed.

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
- OpenAI catalog through Codex CLI

Provider catalog credentials remain separate from launcher authentication and are never injected from keyring storage into launcher subprocess environments.

## Remaining v0.3.0 sequence

1. Validate real profile usage and add portability only where a concrete need is demonstrated.
2. Define the minimum versioned launcher plugin contract in `modelctl-sdk`.
3. Discover installed launcher entry points while preserving built-ins and rejecting duplicate IDs.
4. Add plugin diagnostics, compatibility hardening, and installed-wheel plugin fixtures.
5. Introduce static type-check enforcement at the SDK, profile, and plugin boundaries.
6. Complete a dedicated readiness review before promotion to `main`.

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
