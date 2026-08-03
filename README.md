# modelctl

The universal AI model and coding agent control plane.

## Vision

modelctl aims to become the uv of AI coding agents.

Manage:

- Claude Code
- Gemini CLI
- Codex CLI
- Aider
- Ollama
- OpenRouter
- OpenAI
- Anthropic

with one command.

## Installation

```bash
pip install modelctl
```

## Quick start

Select a provider and model, choose an installed coding-agent launcher, and run it:

```bash
modelctl use
modelctl launchers list
modelctl launchers use claude
modelctl run
```

Supported launcher IDs are `claude`, `gemini`, `codex`, and `aider`. The launcher table shows which one is active and which CLIs are installed locally.

Native launcher arguments are forwarded after `run`:

```bash
modelctl run --continue
modelctl run --sandbox workspace-write
modelctl run --no-auto-commits
```

Aider automatically receives the configured provider. OpenRouter selections are translated to Aider's required model format:

```bash
modelctl launchers use aider
modelctl config set provider openrouter
modelctl config set model anthropic/claude-sonnet-4
modelctl run
# Runs: aider --model openrouter/anthropic/claude-sonnet-4
```

You can inspect the persisted defaults with:

```bash
modelctl config show
```
