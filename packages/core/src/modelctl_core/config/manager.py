import json
from pathlib import Path


class ConfigManager:
    def __init__(self, path: Path | None = None):
        self.path = path or Path.home() / ".config" / "modelctl" / "config.json"

    def load(self) -> dict[str, object]:
        if not self.path.exists():
            return {}

        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, data: dict[str, object]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def update(self, **values: str) -> None:
        config = self.load()
        config.update(values)
        self.save(config)

    def update_model(self, provider: str, model: str) -> None:
        self.update(provider=provider, default_model=model)
