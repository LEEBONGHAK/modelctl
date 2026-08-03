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
modelctl config set launcher claude  # claude, gemini, or codex
modelctl run
```

Native launcher arguments are forwarded after `run`:

```bash
modelctl run --continue
modelctl run --sandbox workspace-write
```

You can inspect the persisted defaults with:

```bash
modelctl config show
```
