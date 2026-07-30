# ADR-0001: Plugin Architecture

```
                modelctl

                    │

             Plugin Loader

        ┌───────────┴───────────┐

    Launcher Plugin      Provider Plugin
```

## monorepo structure

```
modelctl/

├── packages/
│
│   ├── modelctl-core/
│   │
│   ├── modelctl-cli/
│   │
│   ├── modelctl-provider-openrouter/
│   │
│   ├── modelctl-launcher-claude/
│   │
│   ├── modelctl-provider-openai/
│   │
│   └── modelctl-provider-ollama/
│
├── docs/
│
├── scripts/
│
├── examples/
│
└── pyproject.toml
```

