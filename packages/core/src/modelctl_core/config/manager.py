import json
from pathlib import Path

from modelctl_core.security.private_files import (
    atomic_write_private_text,
    read_private_text,
)


class ConfigManager:
    def __init__(self, path: Path | None = None):
        self.path = path or Path.home() / ".config" / "modelctl" / "config.json"

    def load(self) -> dict[str, object]:
        if not self.path.exists():
            return {}

        data = json.loads(read_private_text(self.path))
        if not isinstance(data, dict):
            raise ValueError(f"Invalid configuration format: {self.path}")
        return data

    def save(self, data: dict[str, object]) -> None:
        atomic_write_private_text(
            self.path,
            json.dumps(data, indent=2) + "\n",
        )

    def update(self, **values: str) -> None:
        config = self.load()
        config.update(values)
        self.save(config)

    def update_model(self, provider: str, model: str) -> None:
        self.update(provider=provider, default_model=model)
